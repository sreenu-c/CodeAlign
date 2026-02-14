import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

from dotenv import load_dotenv
load_dotenv()

print("--- Testing CodeAlign LLM Client ---")
# Mask keys for security in logs
groq = os.getenv('GROQ_API_KEY')
gemini = os.getenv('GEMINI_API_KEY')
print(f"GROQ_API_KEY present: {bool(groq)} (Length: {len(groq) if groq else 0})")
print(f"GEMINI_API_KEY present: {bool(gemini)} (Length: {len(gemini) if gemini else 0})")

try:
    from codealign import client
    print("[OK] LLMClient initialized.")
except Exception as e:
    print(f"[FAIL] Failed to import/init client: {e}")
    sys.exit(1)

print("\nAssigning task: 'Say hello'")
try:
    response = client.generate_text(
        system_prompt="You are a helpful assistant.",
        user_prompt="Say hello in one word."
    )
    
    if response:
        print(f"[OK] Success! Response: {response}")
    else:
        print("[FAIL] Failed: Returned None")
        if not groq and not gemini:
             print("Reason: No API keys found in .env file.")
        
except Exception as e:
    print(f"[FAIL] Exception during generation: {e}")
