import google.generativeai as genai
import os
from dotenv import load_dotenv

print("🔥 Test file is running")

print("🔍 Loading environment...")
load_dotenv(".env")

api_key = os.getenv("GEMINI_API_KEY")
print("API Key Loaded:", "YES" if api_key else "NO")

genai.configure(api_key=api_key)

try:
    print("🔍 Calling Gemini API...")
    model = genai.GenerativeModel("models/gemini-2.5-flash")
    response = model.generate_content("Say: Gemini connection successful")

    print("🔍 Response received:")
    print(response.text)

except Exception as e:
    print("❌ Error occurred:")
    print(e)

