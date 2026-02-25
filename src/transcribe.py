# THIS PROGRAM TRANSCIBES A mp3 AUDIO FILE INTO .txt USING OPENAI WHISPER
# 1.GET mp3 FILE
# 2.USE WHISPER TO TRANSCRIBE AUDIO
# 3.STORE .txt IN /data

import whisper
from pathlib import Path
import os

#AI Generated- Since i have bundled ffmeg I have to tell whisper where the ffmpeg is at
ROOT = Path(__file__).resolve().parent.parent
FFMPEG_DIR = ROOT / "tools" / "ffmpeg"   # adjust if your folder name differs
# make ffmpeg discoverable for whisper (only for this program run)
os.environ["PATH"] = str(FFMPEG_DIR) + os.pathsep + os.environ.get("PATH", "")
######################################End of AI Code##########################

model = whisper.load_model("small")

def transcript(audio):
    result = model.transcribe(audio, fp16=False)
    with open(ROOT / "data" / "text" / "transcript.txt", "w",encoding="utf-8") as f:
        f.write(result["text"])
    