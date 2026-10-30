# THIS PROGRAM USES OPENAI API TO SUMMARIZE A TRANSCRIBED AUDIO TEXT
# 1. GET TRANSCRIPT TEXT
# 2. PROMPT GPT TO MAKE A SUMMARY
# 3. GPT ANSWERS IN A FIXED JSON SHAPE SO THE UI CAN SHOW EACH PART
# 4. RETURN THE SUMMARY

import json

from openai import OpenAI
from config import get_openai_key

MODEL = "gpt-5-mini"

PROMPT = """SUMMARIZE THE VIDEO AND GIVE REASONS THAT HELP DECIDE IF IT IS WORTH WATCHING OR NOT.
Give the main idea, all topics covered, quick actionable takeaways, reasons to watch, reasons to skip,
and a final verdict. Keep each bullet short. Base everything only on the transcript."""

LIST = {"type": "array", "items": {"type": "string"}}

SCHEMA = {
    "type": "object",
    "properties": {
        "verdict": {"type": "string", "enum": ["watch", "maybe", "skip"]},
        "verdict_reason": {"type": "string", "description": "One sentence explaining the verdict."},
        "main_idea": {"type": "string", "description": "The main idea in one or two sentences."},
        "topics": LIST,
        "takeaways": LIST,
        "watch_if": LIST,
        "skip_if": LIST,
    },
    "required": ["verdict", "verdict_reason", "main_idea", "topics", "takeaways", "watch_if", "skip_if"],
    "additionalProperties": False,
}


def summary(transcript_text, title=None) -> dict:
    client = OpenAI(api_key=get_openai_key())

    user_text = f"Video title: {title}\n\nTranscript:\n{transcript_text}" if title else transcript_text

    response = client.responses.create(
        model=MODEL,
        input=[
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": user_text},
        ],
        text={"format": {"type": "json_schema", "name": "video_summary", "schema": SCHEMA, "strict": True}},
    )

    return json.loads(response.output_text)


VERDICT_LABELS = {"watch": "Worth watching", "maybe": "Maybe", "skip": "Skip it"}


def format_summary(s) -> str:
    #plain text version for the command line
    def bullets(items):
        return "\n".join(f"- {item}" for item in items)

    return (
        f"Verdict: {VERDICT_LABELS[s['verdict']]} - {s['verdict_reason']}\n\n"
        f"Main idea\n{s['main_idea']}\n\n"
        f"Topics covered\n{bullets(s['topics'])}\n\n"
        f"Quick takeaways\n{bullets(s['takeaways'])}\n\n"
        f"Watch it if\n{bullets(s['watch_if'])}\n\n"
        f"Skip it if\n{bullets(s['skip_if'])}"
    )
