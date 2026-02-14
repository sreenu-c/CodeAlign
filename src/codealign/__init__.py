import os
import json
import logging
from typing import Optional, Dict, Any, List, Union
from dotenv import load_dotenv

# Import providers
try:
    from groq import Groq
except ImportError:
    Groq = None

try:
    import google.generativeai as genai
except ImportError:
    genai = None

load_dotenv()
logger = logging.getLogger(__name__)

class LLMClient:
    def __init__(self):
        self.groq_key = os.getenv("GROQ_API_KEY")
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        
        self.groq_client = None
        if self.groq_key and Groq:
            try:
                self.groq_client = Groq(api_key=self.groq_key)
            except Exception as e:
                logger.error(f"Failed to init Groq client: {e}")

        if self.gemini_key and genai:
            try:
                genai.configure(api_key=self.gemini_key)
            except Exception as e:
                logger.error(f"Failed to verify Gemini key: {e}")

    def generate_text(self, 
                      system_prompt: str, 
                      user_prompt: str, 
                      json_mode: bool = False,
                      temperature: float = 0.0) -> Optional[str]:
        """
        Tries to generate text using Groq (Primary). Falls back to Gemini (Backup).
        """
        # 1. Try Groq
        if self.groq_client:
            try:
                # Updated to a supported model
                model = "llama-3.3-70b-versatile" 
                kwargs = {
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "model": model,
                    "temperature": temperature,
                }
                if json_mode:
                    kwargs["response_format"] = {"type": "json_object"}
                
                chat_completion = self.groq_client.chat.completions.create(**kwargs)
                return chat_completion.choices[0].message.content
            except Exception as e:
                logger.warning(f"Groq generation failed: {e}. Switching to backup.")
        
        # 2. Try Gemini
        if self.gemini_key and genai:
            try:
                # Updated to gemini-1.5-flash
                model_name = "gemini-1.5-flash"
                generation_config = genai.types.GenerationConfig(
                    temperature=temperature
                )
                model = genai.GenerativeModel(model_name)
                full_prompt = f"System: {system_prompt}\n\nUser: {user_prompt}"
                
                response = model.generate_content(
                    full_prompt,
                    generation_config=generation_config
                )
                return response.text
            except Exception as e:
                logger.error(f"Gemini generation failed: {e}")
        
        logger.error("All LLM providers failed or keys missing.")
        return None

    def get_embedding(self, text: str) -> List[float]:
        """
        Generates embeddings using Gemini.
        """
        if not self.gemini_key or not genai:
            logger.warning("Gemini key missing for embeddings.")
            return []
            
        try:
            result = genai.embed_content(
                model="models/embedding-001",
                content=text,
                task_type="retrieval_document",
                title="Code Submission"
            )
            return result['embedding']
        except Exception as e:
            logger.error(f"Gemini embedding failed: {e}")
            return []

# Singleton instance exposed as codealign.client
client = LLMClient()
