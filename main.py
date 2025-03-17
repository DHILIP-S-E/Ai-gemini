from dotenv import load_dotenv
import os

load_dotenv()  # Load API key from .env file
api_key = os.getenv("API_KEY")

if not api_key:
    raise ValueError("API key is missing")
