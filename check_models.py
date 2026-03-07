
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

print("--- Start Model List ---")
for m in genai.list_models():
    print(f"{m.name}")
print("--- End Model List ---")
