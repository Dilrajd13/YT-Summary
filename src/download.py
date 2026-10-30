# THIS PROGRAM DOWNLOADS YOUTUBE VIDEO AUDIO USING YT-dlp #
# 1. RECEIVE YT LINK
# 2. SEARCH VIDEO
# 3. VERIFY IF IT EXISTS/AVAILABLE AND IS SHORT ENOUGH
# 4. DOWNLOAD AUDIO (whisper reads it directly, no mp3 conversion needed)
# 5. STORE IN THE JOB FOLDER

import yt_dlp
from pathlib import Path

from config import DENO_EXE

MAX_SECONDS = 30 * 60  # longer videos take too long to transcribe on CPU


class VideoError(Exception):
    pass


def base_options():
    opts = {"quiet": True, "no_warnings": True, "noprogress": True, "noplaylist": True}
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


def downloader(url, out_dir, on_info=None, on_progress=None):
    """Download the audio of a YouTube video. Returns (audio_path, video_details)."""

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
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # look the video up first so we can reject it before downloading anything
            info = ydl.extract_info(url, download=False)
            details = video_details(info)

            if info.get("is_live"):
                raise VideoError("Live streams can't be summarized.")
            if details["duration"] and details["duration"] > MAX_SECONDS:
                raise VideoError(f"The video is longer than {MAX_SECONDS // 60} minutes.")

            if on_info:
                on_info(details)

            info = ydl.process_ie_result(info, download=True)
    except yt_dlp.utils.DownloadError as e:
        raise VideoError(str(e).removeprefix("ERROR: ")) from e

    return Path(info["requested_downloads"][0]["filepath"]), details
