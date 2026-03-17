from google import genai

from core.config import config

client = genai.Client(api_key=config.gemini_api_key)