import os
from google import genai
from dotenv import load_dotenv
load_dotenv()


gmi_key = os.getenv("GEMINI_KEY")
client = genai.Client(api_key=gmi_key)