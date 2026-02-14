import json
from typing import List, Dict, Any
from codealign import client

def align_spec_code(requirements: List[Dict[str, str]], code: str, analysis: Dict[str, Any], language: str = "Python") -> Dict[str, Any]:
    """
    Checks if the code fulfills requirements using an LLM.
    """
    
    prompt = f"""
    You are an expert AI Coding Assignment Evaluator.
    Evaluate the user's {language} code based on the following dimensions:

    1. Correctness (Functional Alignment):
       - Does the code meet all the listed requirements?
       - Does it handle edge cases (empty input, negatives, etc.)?
       - Assign a score (0-100).
    
    2. Time Efficiency:
       - Detect the time complexity (e.g., O(n), O(n^2)).
       - Is it optimal for this problem?
       - Assign a score (0-100).

    3. Space Efficiency:
       - Analyze memory usage.
       - Assign a score (0-100).

    4. Readability & Code Quality:
       - Check variable naming, comments, docstrings, modularity.
       - NOTE: Lack of comments should be a MINOR weakness (e.g., -5 points) if code is clean and self-explanatory. Do not heavily penalize readable code.
       - Assign a score (0-100).

    Requirements to Check:
    {json.dumps(requirements, indent=2)}
    
    Code Analysis Info:
    {json.dumps(analysis, indent=2)}
    
    Code:
    {code}
    
    Output JSON format:
    {{
        "alignment": [
            {{"requirement": "...", "status": "fulfilled|partial|missing", "type": "Functional|Non-functional", "evidence": "..."}}
        ],
        "scores": {{
            "correctness": {{ "score": 90, "reasoning": "...", "details": {{ "passed_cases": "..." }} }},
            "time_efficiency": {{ "score": 80, "reasoning": "...", "details": {{ "complexity": "O(n)" }} }},
            "space_efficiency": {{ "score": 85, "reasoning": "..." }},
            "readability": {{ "score": 75, "reasoning": "..." }}
        }},
        "feedback": {{
            "strengths": ["Good use of helper functions", "Clean variable naming"],
            "weaknesses": ["Missed edge case for empty input", "Nested loops cause O(n^2)"],
            "improvement_suggestions": ["Use a set for O(1) lookups", "Add docstrings"],
            "better_approach": "A more optimal approach would be to use dynamic programming with binary search to achieve O(n log n) time complexity."
        }}
    }}
    """
    
    system_prompt = "You are a senior technical interviewer evaluating code quality and correctness."

    try:
        response_text = client.generate_text(
            system_prompt=system_prompt,
            user_prompt=prompt,
            json_mode=True
        )

        if not response_text:
             # Failover/Mock
            return {
                "alignment": [],
                "scores": {
                    "correctness": {"score": 0, "reasoning": "LLM Failed"},
                    "time_efficiency": {"score": 0, "reasoning": "LLM Failed"},
                    "space_efficiency": {"score": 0, "reasoning": "LLM Failed"},
                    "readability": {"score": 0, "reasoning": "LLM Failed"}
                }
            }

        data = json.loads(response_text)
        return data
    except Exception as e:
        print(f"Error calling LLM: {e}")
        return {"alignment": [], "scores": {}}
