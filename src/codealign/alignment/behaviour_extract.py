import json
from typing import List, Dict, Any
from codealign import client

def extract_requirements(problem_text: str) -> List[Dict[str, str]]:
    """
    Extracts key requirements from the problem text using an LLM (Groq/Gemini).
    Returns a list of dicts with keys: 'description', 'type'.
    """
    
    prompt = f"""
    Analyze the following coding problem text and extract a list of specific requirements.
    Classify each as 'functional', 'edge_case', or 'constraint'.
    
    Problem Text:
    {problem_text}
    
    Output JSON format:
    {{
        "requirements": [
            {{"description": "...", "type": "..."}}
        ]
    }}
    """

    system_prompt = "You are a senior technical interviewer extracting requirements from coding problems."

    try:
        response_text = client.generate_text(
            system_prompt=system_prompt,
            user_prompt=prompt,
            json_mode=True
        )
        if not response_text:
            # Fallback mock if LLM fails completely
            print("Warning: LLM generation failed. Using mock requirements.")
            return [
                {"description": "Return 0 for empty input/list", "type": "edge_case"},
                {"description": "Handle negative integers if applicable", "type": "functional"},
                {"description": "Time complexity should be efficient (e.g., O(n log n))", "type": "constraint"},
                {"description": "Return the length of the longest increasing subsequence", "type": "functional"},
            ]
            
        data = json.loads(response_text)
        return data.get("requirements", [])
    except Exception as e:
        print(f"Error parsing LLM response: {e}")
        return []
