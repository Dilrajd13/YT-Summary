#This Retreives OpenAI API Key from .env file 
#This is to help prevent my API Key from being leaked.
#make a .env and follow the .env.example on how to use your own key

import os
from dotenv import load_dotenv
#reads .env -
load_dotenv()  

def get_openai_key() -> str:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError(
            "OPENAI_API_KEY not set. Create a .env file (copy .env.example) and paste your key."
        )
    return key