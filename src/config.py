#This Retreives OpenAI API Key and finds the tools (ffmpeg, deno) the program needs
#This is to help prevent my API Key from being leaked.
#make a .env and follow the .env.example on how to use your own key
# 1. A REAL KEY IN .env WINS
# 2. OTHERWISE FALL BACK TO THE OPENAI_API_KEY ENVIRONMENT VARIABLE
# 3. THE PLACEHOLDER FROM .env.example DOES NOT COUNT AS A KEY

import os
import shutil
from pathlib import Path

import imageio_ffmpeg
from dotenv import dotenv_values

ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = ROOT / ".env"
PLACEHOLDER_KEY = "put_your_key_here"


class MissingKeyError(RuntimeError):
    pass


def get_openai_key() -> str:
    #.env is re-read every call so you can paste a key in without restarting the app
    file_key = dotenv_values(ENV_FILE).get("OPENAI_API_KEY") if ENV_FILE.exists() else None

    for key in (file_key, os.getenv("OPENAI_API_KEY")):
        if key and key.strip() and key.strip() != PLACEHOLDER_KEY:
            return key.strip()

    raise MissingKeyError(
        "No OpenAI API key found. Copy .env.example to .env and paste your key, "
        "or set the OPENAI_API_KEY environment variable."
    )


def has_openai_key() -> bool:
    try:
        get_openai_key()
        return True
    except MissingKeyError:
        return False


#ffmpeg comes from the imageio-ffmpeg pip package so nobody has to install it by hand
FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()


def find_deno():
    #yt-dlp needs a JavaScript runtime to read YouTube pages, the deno pip package provides one
    try:
        import deno
        return deno.find_deno_bin()
    except Exception:
        return shutil.which("deno")


DENO_EXE = find_deno()
