# COMMAND LINE VERSION (for the website run app.py or run.bat instead)
# 1. GET USER INPUT (YTLINK)
# 2. RUN THE PIPELINE (find video, get transcript, summarize, clean up)
# 3. OUTPUT SUMMARY & DISPLAY ERRORS

from pipeline import summarize_video
from summarize import format_summary


def report(event, **data):
    if event == "video":
        print(f"Found: {data['video']['title']}")
    elif event == "method" and data["method"] == "download":
        print("No captions, downloading audio...")
    elif event == "method" and data["method"] == "whisper":
        print(f"Transcribing with Whisper on the {data['device']}...")
    elif event == "method" and data["method"] == "done":
        print(f"Got transcript from {data['source']}")
    elif event == "step" and data["step"] == "summarize":
        print("Summarizing...")


url = input("Enter a valid URL!- ")

try:
    result = summarize_video(url, report)
    print()
    print(format_summary(result["summary"]))
except Exception as e:
    print(f"\nError: {e}")
