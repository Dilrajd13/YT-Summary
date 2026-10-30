# RUNS THE WHOLE PROCESS, SHARED BY THE COMMAND LINE (main.py) AND THE WEBSITE (app.py)
# 1. CHECK THE API KEY BEFORE DOING ANY SLOW WORK
# 2. DOWNLOAD VIDEO AUDIO
# 3. TRANSCRIBE AUDIO
# 4. SUMMARIZE TRANSCRIPTION
# 5. CLEAN UP FILES
# report(event, **data) is called along the way so the caller can show progress

from cleanup import clean_job_folder, new_job_folder
from config import get_openai_key
from download import downloader
from summarize import summary
from transcribe import transcript


def summarize_video(url, report=lambda event, **data: None) -> dict:
    get_openai_key()

    folder = new_job_folder()
    try:
        report("step", step="download")
        audio_path, video = downloader(
            url,
            folder,
            on_info=lambda details: report("video", video=details),
            on_progress=lambda percent: report("progress", percent=percent),
        )

        report("step", step="transcribe")
        text = transcript(audio_path)

        report("step", step="summarize")
        result = summary(text, video["title"])

        return {"video": video, "transcript": text, "summary": result}
    finally:
        clean_job_folder(folder)
