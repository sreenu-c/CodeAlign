from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class AlignmentItem(BaseModel):
    requirement: str
    type: str
    status: str
    evidence: str

class DimensionScore(BaseModel):
    score: int
    reasoning: str
    details: Optional[Dict[str, Any]] = None

class AlignmentReport(BaseModel):
    # original alignment items (granular correctness)
    items: List[AlignmentItem]
    
    # 4 dimensions
    correctness: DimensionScore
    time_efficiency: DimensionScore
    space_efficiency: DimensionScore
    readability: DimensionScore
    
    overall_score: float
