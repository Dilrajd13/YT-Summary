# THIS PROGRAM USES OPENAI API TO SUMMARIZE A TRANSCRIBED AUDIO TEXT
# 1. FIND TRANSCRIPT FILE
# 2. OPEN FILE
# 3. PROMPT GPT TO MAKE A SUMMARY
# 4. STORE SUMMARY IN /data

from openai import OpenAI
from config import get_openai_key

def summary():
    client = OpenAI(api_key=get_openai_key())

    PROMPT = """SUMMARIZE THE VIDEO AND GIVE REASONS THAT HELP DECIDE IF IT IS WORTH WATCHING OR NOT. Give the main idea and all topic covered in bullet points"""

    with open("data/text/transcript.txt", "r", encoding="utf-8") as f:
        transcript_text = f.read()

    response=client.responses.create(
        model="gpt-5-mini",

        input=[
            {"role": "system","content": PROMPT},
            {"role":"user","content": transcript_text}
        ]

    )

    with open("data/sum.txt", "w",encoding="utf-8") as f:

        print(response.output_text, file= f)