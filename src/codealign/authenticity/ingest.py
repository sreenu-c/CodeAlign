import uuid
import json
import os
import logging
from typing import Dict, Any, List
from codealign import client

logger = logging.getLogger(__name__)

# File to persist submissions
DATA_FILE = "submissions.json"
SUBMISSIONS_DB = {}

def load_submissions():
    """Loads submissions from JSON file."""
    global SUBMISSIONS_DB
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                SUBMISSIONS_DB = json.load(f)
            logger.info(f"Loaded {len(SUBMISSIONS_DB)} submissions from {DATA_FILE}")
        except Exception as e:
            logger.error(f"Failed to load submissions: {e}")
            SUBMISSIONS_DB = {}
    else:
        SUBMISSIONS_DB = {}

def save_submissions():
    """Saves submissions to JSON file."""
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(SUBMISSIONS_DB, f, indent=2)
    except Exception as e:
        logger.error(f"Failed to save submissions: {e}")

# Load on module import
load_submissions()

def ingest_submission(code: str, student_id: str = "anonymous", problem_id: str = "default") -> Dict[str, Any]:
    """
    Stores a submission and returns its metadata.
    Persists to local JSON file.
    """
    # Check for duplicate code to avoid spamming DB? 
    # For now, just ingest everything.
    
    submission_id = str(uuid.uuid4())
    
    # Compute embedding
    embedding = client.get_embedding(code)
    
    submission = {
        "id": submission_id,
        "student_id": student_id,
        "problem_id": problem_id,
        "code": code,
        "embedding": embedding
    }
    
    SUBMISSIONS_DB[submission_id] = submission
    save_submissions()
    
    return submission

def get_all_submissions(problem_id: str) -> list:
    return [s for s in SUBMISSIONS_DB.values() if s.get('problem_id') == problem_id]
