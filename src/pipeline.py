# RUNS THE WHOLE PROCESS, SHARED BY THE COMMAND LINE (main.py) AND THE WEBSITE (app.py)
# 1. CHECK THE API KEY BEFORE DOING ANY SLOW WORK
# 2. FIND THE VIDEO
# 3. GET THE TRANSCRIPT - YOUTUBE CAPTIONS IF IT HAS THEM, OTHERWISE DOWNLOAD + WHISPER
# 4. SUMMARIZE TRANSCRIPTION
# 5. CLEAN UP FILES
# report(event, **data) is called along the way so the caller can show progress

from cleanup import clean_job_folder, new_job_folder
from config import get_openai_key
from download import download_audio, find_video, get_captions
from summarize import summary
from transcribe import load_model, transcript


def summarize_video(url, report=lambda event, **data: None) -> dict:
    get_openai_key()

    report("step", step="find")
    info, video = find_video(url)
    report("video", video=video)

    report("step", step="transcript")
    text = get_captions(info)
    source = "YouTube captions"

    if not text:
        folder = new_job_folder()
        try:
            report("method", method="download")
            audio_path = download_audio(info, folder, on_progress=lambda percent: report("progress", percent=percent))

            _, device = load_model()
            source = f"Whisper ({device})"
            report("method", method="whisper", device=device)
            text = transcript(audio_path, on_progress=lambda percent: report("progress", percent=percent))
        finally:
            clean_job_folder(folder)

    report("method", method="done", source=source)

    report("step", step="summarize")
    result = summary(text, video["title"])

    return {"video": video, "transcript": text, "transcript_source": source, "summary": result}
