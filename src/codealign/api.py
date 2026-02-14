from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Any

from .alignment.behaviour_extract import extract_requirements
from .alignment.code_analysis import analyze_code
from .alignment.align_reasoner import align_spec_code
from .cohort_stats import calculate_score
from .authenticity.ingest import ingest_submission, get_all_submissions
from .authenticity.similarity import calculate_similarity
from .authenticity.ai_signals import detect_ai_signals

app = FastAPI(
    title="CodeAlign API",
    description="AI-powered backend for evaluating coding assignments.",
    version="1.0.0"
)

class EvaluationRequest(BaseModel):
    """Request model for code evaluation."""
    problem_text: str = Field(..., description="The full text of the problem statement.")
    code: str = Field(..., description="The candidate's source code.")
    student_id: Optional[str] = Field("anonymous", description="ID of the student submission.")

class AuthenticityRequest(BaseModel):
    """Request model for authenticity checks."""
    code: str = Field(..., description="The candidate's source code.")
    student_id: Optional[str] = "anonymous"
    problem_id: Optional[str] = "default"

@app.post("/evaluate", summary="Evaluate a submission")
def evaluate(request: EvaluationRequest) -> Dict[str, Any]:
    """
    Performs a full evaluation of the submission:
    1. Alignment with Problem Statement
    2. Code Quality & Correctness
    3. Authenticity Risk
    """
    # 1. Extract Requirements
    requirements = extract_requirements(request.problem_text)
    
    # 2. Analyze Code
    analysis_result = analyze_code(request.code)
    if "error" in analysis_result:
        raise HTTPException(status_code=400, detail=analysis_result["error"])
        
    # 3. Align Spec <-> Code (Returns dict with 'alignment' and 'scores')
    alignment_data = align_spec_code(requirements, request.code, analysis_result)
    
    # 4. Check Authenticity
    ai_signals = detect_ai_signals(request.code)
    
    # 5. Score
    risk_score = ai_signals['confidence'] * 100
    score_data = calculate_score(alignment_data, risk_score=risk_score)
    
    return {
        "overall_score": score_data["final_score"],
        "breakdown": score_data["breakdown"],
        "detailed_scores": alignment_data.get("scores", {}),
        "alignment_details": alignment_data.get("alignment", []),
        "authenticity_risk": risk_score,
        "authenticity_signals": ai_signals,
        "feedback": alignment_data.get("feedback", {})
    }

@app.post("/check_authenticity", summary="Check specific authenticity risk")
def check_authenticity(request: AuthenticityRequest) -> Dict[str, Any]:
    """
    Checks for plagiarism (similarity) and AI generation patterns.
    """
    # 1. Ingest/Store
    current_sub = ingest_submission(request.code, request.student_id, request.problem_id)
    
    # 2. Compare against others
    others = get_all_submissions(request.problem_id)
    max_similarity = 0.0
    most_similar_id = None
    
    for other in others:
        if other['id'] == current_sub['id']:
            continue
        sim = calculate_similarity(request.code, other.get('code', ''))
        if sim > max_similarity:
            max_similarity = sim
            most_similar_id = other['id']
            
    # 3. AI Signals
    ai_signals = detect_ai_signals(request.code)
    
    return {
        "max_similarity": max_similarity,
        "most_similar_submission_id": most_similar_id,
        "ai_signals": ai_signals,
        "risk_score": max(max_similarity * 100, ai_signals['confidence'] * 100)
    }
