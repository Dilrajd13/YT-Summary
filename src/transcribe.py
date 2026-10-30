# THIS PROGRAM TRANSCIBES AN AUDIO FILE INTO TEXT USING WHISPER (faster-whisper)
# 1.LOAD THE MODEL ON THE NVIDIA GPU IF THERE IS ONE THAT WORKS, OTHERWISE THE CPU
# 2.USE WHISPER TO TRANSCRIBE AUDIO
# 3.REPORT HOW FAR ALONG IT IS
# 4.RETURN THE TEXT
# Set YT_SUMMARY_DEVICE=cpu to force the CPU (handy for testing) or =gpu to try the GPU on Mac/Linux

import os
import subprocess
import sys
import threading
from pathlib import Path

import numpy as np

from config import FFMPEG_EXE


def add_cuda_dlls():
    #on Windows the NVIDIA pip packages put their DLLs somewhere ctranslate2 doesn't look by default
    try:
        import nvidia.cublas
        import nvidia.cudnn
    except ImportError:
        return False

    for module in (nvidia.cublas, nvidia.cudnn):
        bin_dir = Path(list(module.__path__)[0]) / "bin"
        if bin_dir.exists():
            os.add_dll_directory(str(bin_dir))
            os.environ["PATH"] = str(bin_dir) + os.pathsep + os.environ.get("PATH", "")
    return True


HAS_CUDA_LIBS = sys.platform == "win32" and add_cuda_dlls()

import ctranslate2
from faster_whisper import WhisperModel

MODEL_NAME = "small"
SAMPLE_RATE = 16000

_model = None
_device = None
_model_lock = threading.Lock()


def should_try_gpu():
    setting = os.getenv("YT_SUMMARY_DEVICE", "auto").lower()  # auto, cpu, or gpu
    if setting in ("cpu", "gpu"):
        return setting == "gpu"
    #auto only tries the GPU where it's been tested: Windows with requirements-gpu.txt installed
    return sys.platform == "win32" and HAS_CUDA_LIBS and ctranslate2.get_cuda_device_count() > 0


def pick_model():
    if should_try_gpu():
        try:
            model = WhisperModel(MODEL_NAME, device="cuda", compute_type="float16")
            #the GPU libraries only load on first use, so do a tiny test run to make sure it really works
            list(model.transcribe(np.zeros(SAMPLE_RATE, np.float32))[0])
            return model, "GPU"
        except Exception as e:
            print(f"GPU didn't work ({e}), using the CPU instead")

    return WhisperModel(MODEL_NAME, device="cpu", compute_type="int8", cpu_threads=os.cpu_count() or 4), "CPU"


def load_model():
    #loading takes a few seconds (and downloads the model the first time) so only do it once
    global _model, _device
    with _model_lock:
        if _model is None:
            print("Loading Whisper model...")
            _model, _device = pick_model()
            print(f"Whisper is using the {_device}")
    return _model, _device


def load_audio(path):
    #decode with our bundled ffmpeg into the 16kHz mono audio whisper expects
    cmd = [
        FFMPEG_EXE, "-nostdin", "-threads", "0", "-i", str(path),
        "-f", "s16le", "-ac", "1", "-acodec", "pcm_s16le", "-ar", str(SAMPLE_RATE), "-",
    ]
    try:
        out = subprocess.run(cmd, capture_output=True, check=True).stdout
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to read audio: {e.stderr.decode(errors='ignore')}") from e
    return np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0


def transcript(audio_path, on_progress=None) -> str:
    model, _ = load_model()
    #beam_size=1 checks one guess at a time like the original whisper did, much faster for the same quality
    segments, info = model.transcribe(load_audio(audio_path), beam_size=1)

    parts = []
    for segment in segments:
        parts.append(segment.text.strip())
        if on_progress and info.duration:
            on_progress(min(100, round(segment.end / info.duration * 100)))

    return " ".join(parts)
