from pydantic import BaseModel
from typing import List, Optional

class AuthenticityReport(BaseModel):
    risk_score: float
    verdict: str
    reasons: List[str]
