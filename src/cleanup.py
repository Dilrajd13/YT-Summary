#This deletes all files used to make the summary after output to the user

from pathlib import Path

def clean_data_folder():
    files_to_delete = [
        "data/audio/audio.mp3",
        "data/text/transcript.txt",
        "data/sum.txt"
    ]

    for file in files_to_delete:
        path = Path(file)
        if path.exists():
            path.unlink()

