
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

models_to_test = [
    "gemini-1.5-flash",
    "gemini-1.5-flash-001",
    "gemini-1.5-flash-latest",
    "gemini-pro",
    "models/gemini-1.5-flash"
]

print(f"Testing generation with API key: {api_key[:10]}...")

for m in models_to_test:
    print(f"Testing model: {m}")
    try:
        model = genai.GenerativeModel(m)
        response = model.generate_content("Hello")
        print(f"SUCCESS with {m}")
        break
    except Exception as e:
        print(f"FAILED with {m}: {e}")

print("\nTesting embeddings...")
embedding_models = ["models/text-embedding-004", "models/embedding-001"]
for m in embedding_models:
    try:
        genai.embed_content(model=m, content="Hello", task_type="retrieval_document")
        print(f"SUCCESS embedding with {m}")
        break
    except Exception as e:
        print(f"FAILED embedding with {m}: {e}")
