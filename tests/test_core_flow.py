import pytest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from codealign.cohort_stats import calculate_score

def test_calculate_score_perfect():
    """Test that perfect alignment scores result in high final score."""
    alignment_data = {
        "scores": {
            "correctness": {"score": 100},
            "time_efficiency": {"score": 100},
            "space_efficiency": {"score": 100},
            "readability": {"score": 100}
        }
    }
    result = calculate_score(alignment_data, risk_score=0)
    assert result['final_score'] == 100.0
    assert result['risk_score'] == 0

def test_calculate_score_authenticity_no_penalty():
    """Test that high risk score does NOT lower the technical score."""
    alignment_data = {
        "scores": {
            "correctness": {"score": 100},
            "time_efficiency": {"score": 100},
            "space_efficiency": {"score": 100},
            "readability": {"score": 100}
        }
    }
    # Risk is 100%
    result = calculate_score(alignment_data, risk_score=100)
    
    # Final score should still be 100 because we decoupled it!
    assert result['final_score'] == 100.0  
    assert result['risk_score'] == 100

def test_calculate_score_weighted():
    """Test weighted calculation (40% correct, 20% others)."""
    alignment_data = {
        "scores": {
            "correctness": {"score": 50},  # 50 * 0.4 = 20
            "time_efficiency": {"score": 100}, # 100 * 0.2 = 20
            "space_efficiency": {"score": 100}, # 100 * 0.2 = 20
            "readability": {"score": 100}     # 100 * 0.2 = 20
        }
    }
    # Total should be 20+20+20+20 = 80
    result = calculate_score(alignment_data, risk_score=0)
    assert result['final_score'] == 80.0
