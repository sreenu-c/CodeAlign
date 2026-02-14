from typing import Dict, Any
from .features import extract_features

def calculate_similarity(code1: str, code2: str) -> float:
    """
    Calculates similarity between two code snippets.
    Returns a float between 0.0 and 1.0.
    """
    # 1. Structural similarity (Jaccard on tokens)
    feat1 = extract_features(code1)
    feat2 = extract_features(code2)
    
    tokens1 = feat1.get("tokens", set())
    tokens2 = feat2.get("tokens", set())
    
    if not tokens1 and not tokens2:
        return 1.0
    if not tokens1 or not tokens2:
        return 0.0
        
    intersection = len(tokens1.intersection(tokens2))
    union = len(tokens1.union(tokens2))
    
    jaccard_sim = intersection / union if union > 0 else 0.0
    
    # 2. Sequence matcher (approximating AST/structure via text)
    from difflib import SequenceMatcher
    seq_sim = SequenceMatcher(None, code1, code2).ratio()
    
    # Weighted average (favoring sequence matcher for now as it captures order)
    return (0.3 * jaccard_sim) + (0.7 * seq_sim)

def find_similar(embedding, submissions: list, threshold: float = 0.85, exclude_candidate_id: str = None) -> list:
    """
    Finds similar submissions from a list, excluding a specific candidate ID.
    
    Args:
        embedding: The embedding of the current submission (unused in this version, kept for API compatibility).
        submissions: List of stored submission dictionaries.
        threshold: specific threshold for similarity.
        exclude_candidate_id: The ID of the candidate to exclude from checks.
        
    Returns:
        List of similar submission dictionaries.
    """
    similar = []
    # Note: 'embedding' arg is in the signature because the user requested it, 
    # but our current 'calculate_similarity' uses code text, not embeddings.
    # We will use the 'code' field from the submissions.
    
    
    # We need the code text to compare against, so we assume 'embedding' argument is acting as a placeholder 
    # for the query code in this context, or we adjust the usage.
    # To support the user's specific request signature:
    # `def find_similar(self, embedding, threshold=0.85, exclude_candidate_id=None):`
    # We will assume `embedding` here is actually the code string in our current architecture 
    # (since we don't have a Vector DB handy to do pure embedding similarity in this function easily without passing the model).
    
    # ADAPTATION: We will use 'embedding' as 'query_code' for our text-based matching.
    query_code = embedding 

    for stored in submissions:
        # User's requested logic:
        # "Only flag if similar code comes from a DIFFERENT candidate"
        stored_candidate_id = stored.get('student_id', 'anonymous')
        
        if exclude_candidate_id and stored_candidate_id == exclude_candidate_id:
            continue  # Skip this candidate's own submissions

        # Calculate similarity (using our existing function)
        stored_code = stored.get('code', '')
        similarity = calculate_similarity(query_code, stored_code)

        if similarity >= threshold:
            stored['similarity_score'] = similarity # Add score to result
            similar.append(stored)

    return similar
