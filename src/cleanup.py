#This makes a temporary folder for each summary and deletes it after output to the user

import shutil
import tempfile
from pathlib import Path

from config import ROOT

JOBS_DIR = ROOT / "data" / "jobs"


def new_job_folder() -> Path:
    JOBS_DIR.mkdir(parents=True, exist_ok=True)
    return Path(tempfile.mkdtemp(dir=JOBS_DIR))


def clean_job_folder(folder):
    shutil.rmtree(folder, ignore_errors=True)
