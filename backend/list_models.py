import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv(".env")

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

print("🔍 Listing available models...\n")

models = genai.list_models()

for m in models:
    print(m.name)

