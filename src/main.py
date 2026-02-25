# MAIN PROGRAM TO MANAGE USER INPUT / OUTPUT & CLEAN UP FILES AFTER OUTPUT & DISPLAY ERRORS
# 1. GET USER INPUT (YTLINK)
# 2. DOWNLOAD VIDEO AUDIO
# 3. TRANSCRIBE mp3 FILE
# 4. SUMMARIZE TRANSCRIPTION
# 5. OUTPUT SUMMARY
# 5. CLEAN UP FILES (.mp3,transcription,and summary)

from download import downloader
from transcribe import transcript
from pathlib import Path

audioPath="data/audio/audio.mp3"
url=input("Enter a valid URL!")

downloader(url)
transcript(audioPath)
