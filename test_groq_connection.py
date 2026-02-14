import os
import sys

# Ensure we can import codealign
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

def test_connection():
    print("--- Groq Connection Test ---")
    
    # 1. Check Environment Variable
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ GROQ_API_KEY is not set in environment variables.")
        api_key = input("👉 Please enter your Groq API Key to test: ").strip()
        if not api_key:
            print("❌ No API Key provided. Exiting.")
            return
        os.environ["GROQ_API_KEY"] = api_key
    else:
        print("✅ GROQ_API_KEY found in environment.")

    # 2. Initialize Client
    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        print("✅ Groq client initialized.")
    except Exception as e:
        print(f"❌ Failed to initialize Groq client: {e}")
        return

    # 3. Test Completion
    print("⏳ Attempting to generate text...")
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Hello! Are you working?",
                }
            ],
            model="llama3-8b-8192",
        )
        print("✅ Connection Successful!")
        print(f"🤖 Response: {chat_completion.choices[0].message.content}")
    except Exception as e:
        print(f"❌ Connection Failed: {e}")

if __name__ == "__main__":
    test_connection()
