# COMMAND LINE VERSION (for the website run app.py or run.bat instead)
# 1. GET USER INPUT (YTLINK)
# 2. RUN THE PIPELINE (download, transcribe, summarize, clean up)
# 3. OUTPUT SUMMARY & DISPLAY ERRORS

from pipeline import summarize_video
from summarize import format_summary

STEP_NAMES = {
    "download": "Downloading audio...",
    "transcribe": "Transcribing (this can take a minute)...",
    "summarize": "Summarizing...",
}


def report(event, **data):
    if event == "step":
        print(STEP_NAMES[data["step"]])
    elif event == "video":
        print(f"Found: {data['video']['title']}")


url = input("Enter a valid URL!- ")

try:
    result = summarize_video(url, report)
    print()
    print(format_summary(result["summary"]))
except Exception as e:
    print(f"\nError: {e}")
