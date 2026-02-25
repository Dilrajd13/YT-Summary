# THIS PROGRAM DOWNLOADS YOUTUBE VIDEO AUDIO (mp3) USING YT-dlp #
# 1. RECEIVE YT LINK
# 2. SEARCH VIDEO
# 3. VERIFY IF IT EXISTS/AVAILABLE
# 4. DOWNLOAD AUDIO AS mp3 file
# 5. STORE IN /DATA

import yt_dlp
from pathlib import Path

# URLS = 'https://www.youtube.com/watch?v=LNYm40RmRzs'
def downloader(URLS):
    FFMPEG_DIR = "tools/ffmpeg"

    def less_than_a_halfhour(info, *, incomplete):
        """Download only videos shorter than a hour"""
        duration = info.get('duration')
        if duration and duration > 1900:
            return 'The video is longer than a halfhour'

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'data/%(title)s.%(ext)s',
        'match_filter': less_than_a_halfhour,
        "ffmpeg_location": str(FFMPEG_DIR),
    
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }]
    }


    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(URLS)
