import tokenize
from io import BytesIO
from typing import Set, Dict, Any

def extract_features(code: str) -> Dict[str, Any]:
    """
    Extracts lexical features from code for similarity comparison.
    """
    features = {
        "tokens": set(),
        "identifiers": set(),
        "lines_of_code": len(code.splitlines()),
    }
    
    try:
        tokens = tokenize.tokenize(BytesIO(code.encode('utf-8')).readline)
        for token in tokens:
            if token.type == tokenize.NAME:
                features["identifiers"].add(token.string)
                features["tokens"].add(token.string)
            elif token.type == tokenize.OP:
                 features["tokens"].add(token.string)
    except tokenize.TokenError:
        pass
        
    return features
