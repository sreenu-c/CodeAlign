from typing import List, Dict, Any

def calculate_cohort_stats(submissions):
    """
    Placeholder for cohort stats aggregation.
    """
    pass

def calculate_score(alignment_data: Dict[str, Any], risk_score: float = 0.0) -> Dict[str, Any]:
    """
    Calculates a final score based on the 4 dimensions + authenticity risk.
    """
    scores = alignment_data.get("scores", {})
    
    s_corr = scores.get("correctness", {}).get("score", 0)
    s_time = scores.get("time_efficiency", {}).get("score", 0)
    s_space = scores.get("space_efficiency", {}).get("score", 0)
    s_read = scores.get("readability", {}).get("score", 0)
    
    # Weighted Average
    # Correctness: 40%, Time: 20%, Space: 20%, Readability: 20%
    base_score = (s_corr * 0.4) + (s_time * 0.2) + (s_space * 0.2) + (s_read * 0.2)
    
    # Authenticity is now reported separately, NOT as a penalty.
    # We return risk_score for the UI to display as a flag.
    
    return {
        "final_score": round(base_score, 1),
        "breakdown": {
            "correctness": s_corr,
            "time_efficiency": s_time,
            "space_efficiency": s_space,
            "readability": s_read
        },
        "penalty": 0, # Deprecated
        "risk_score": risk_score
    }
