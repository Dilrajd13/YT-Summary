# THIS PROGRAM GETS A YOUTUBE VIDEO'S CAPTIONS OR AUDIO USING YT-dlp #
# 1. RECEIVE YT LINK
# 2. SEARCH VIDEO
# 3. VERIFY IF IT EXISTS/AVAILABLE AND IS SHORT ENOUGH
# 4. USE THE VIDEO'S CAPTIONS IF IT HAS ANY (instant, no transcribing needed)
# 5. OTHERWISE DOWNLOAD THE AUDIO SO WHISPER CAN TRANSCRIBE IT

import json

import yt_dlp
from pathlib import Path

from config import DENO_EXE, FFMPEG_EXE

MAX_SECONDS = 30 * 60  # longer videos take too long to transcribe on CPU


class VideoError(Exception):
    pass


def base_options():
    opts = {"quiet": True, "no_warnings": True, "noprogress": True, "noplaylist": True, "ffmpeg_location": FFMPEG_EXE}
    if DENO_EXE:
        opts["js_runtimes"] = {"deno": {"path": DENO_EXE}}
    return opts


def video_details(info):
    return {
        "id": info.get("id"),
        "title": info.get("title"),
        "channel": info.get("channel") or info.get("uploader"),
        "duration": info.get("duration"),
        "thumbnail": info.get("thumbnail"),
        "url": info.get("webpage_url"),
    }


def find_video(url):
    """Look the video up without downloading anything. Returns (info, video_details)."""
    try:
        with yt_dlp.YoutubeDL(base_options()) as ydl:
            info = ydl.extract_info(url, download=False)
    except yt_dlp.utils.DownloadError as e:
        raise VideoError(str(e).removeprefix("ERROR: ")) from e

    details = video_details(info)
    if info.get("is_live"):
        raise VideoError("Live streams can't be summarized.")
    if details["duration"] and details["duration"] > MAX_SECONDS:
        raise VideoError(f"The video is longer than {MAX_SECONDS // 60} minutes.")

    return info, details


def pick_caption_track(info):
    lang = (info.get("language") or "en").split("-")[0]
    manual = {k: v for k, v in (info.get("subtitles") or {}).items() if k != "live_chat"}
    auto = info.get("automatic_captions") or {}

    #captions the creator uploaded come first (en, en-US, or the video's language)
    candidates = [formats for key, formats in manual.items() if key.split("-")[0] in (lang, "en")]
    #then YouTube's auto captions in the video's own language, not the machine-translated copies
    candidates += [auto[key] for key in (f"{lang}-orig", lang) if key in auto]

    for formats in candidates:
        track = next((f for f in formats if f.get("ext") == "json3"), None)
        if track:
            return track["url"]
    return None


def get_captions(info):
    """Returns the video's captions as plain text, or None if it doesn't have usable ones."""
    url = pick_caption_track(info)
    if not url:
        return None

    try:
        with yt_dlp.YoutubeDL(base_options()) as ydl:
            data = json.loads(ydl.urlopen(url).read())
    except Exception:
        return None  # whisper is the backup, so any problem here just means "no captions"

    lines = []
    for event in data.get("events", []):
        text = "".join(seg.get("utf8", "") for seg in event.get("segs") or []).replace("\n", " ").strip()
        if text:
            lines.append(text)

    text = " ".join(lines)
    return text if len(text.split()) >= 20 else None


def download_audio(info, out_dir, on_progress=None):
    """Download the audio of a video found with find_video. Returns the audio file path."""

    def progress_hook(d):
        if on_progress and d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate")
            if total:
                on_progress(round(d["downloaded_bytes"] / total * 100))

    ydl_opts = {
        **base_options(),
        "format": "bestaudio/best",
        "outtmpl": str(Path(out_dir) / "audio.%(ext)s"),
        "progress_hooks": [progress_hook],
    }

    try:
        #look it up again here, YouTube's download links only work for the session that found them
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(info["webpage_url"], download=True)
    except yt_dlp.utils.DownloadError as e:
        raise VideoError(str(e).removeprefix("ERROR: ")) from e

    return Path(info["requested_downloads"][0]["filepath"])
