# THIS PROGRAM TRANSCIBES AN AUDIO FILE INTO TEXT USING OPENAI WHISPER
# 1.GET AUDIO FILE
# 2.DECODE IT WITH FFMPEG
# 3.USE WHISPER TO TRANSCRIBE AUDIO
# 4.RETURN THE TEXT

import subprocess
import threading

import numpy as np
import whisper

from config import FFMPEG_EXE

MODEL_NAME = "small"
SAMPLE_RATE = 16000

_model = None
_model_lock = threading.Lock()


def load_model():
    #loading takes a few seconds so only do it once
    global _model
    with _model_lock:
        if _model is None:
            _model = whisper.load_model(MODEL_NAME)
    return _model


def load_audio(path):
    #same as whisper.load_audio but uses our bundled ffmpeg instead of needing it on PATH
    cmd = [
        FFMPEG_EXE, "-nostdin", "-threads", "0", "-i", str(path),
        "-f", "s16le", "-ac", "1", "-acodec", "pcm_s16le", "-ar", str(SAMPLE_RATE), "-",
    ]
    try:
        out = subprocess.run(cmd, capture_output=True, check=True).stdout
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to read audio: {e.stderr.decode(errors='ignore')}") from e
    return np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0


def transcript(audio_path) -> str:
    result = load_model().transcribe(load_audio(audio_path), fp16=False)
    return result["text"].strip()
