import os
import sys
import json

# Add src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

from codealign.alignment.behaviour_extract import extract_requirements
from codealign.alignment.code_analysis import analyze_code
from codealign.alignment.align_reasoner import align_spec_code
from codealign.cohort_stats import calculate_score

# Default Problem (LIS)
PROBLEM_TEXT = """Given an integer array nums, return the length of the longest strictly increasing subsequence.
Example 1:
Input: nums = [10,9,2,5,3,7,101,18]
Output: 4
Explanation: The longest increasing subsequence is [2,3,7,101], therefore the length is 4.
Constraints:
- 1 <= nums.length <= 2500
- -10^4 <= nums[i] <= 10^4
"""

def test_file(filename):
    filepath = os.path.join("examples", filename)
    print(f"\n{'='*50}")
    print(f"Testing: {filename}")
    print(f"{'='*50}")
    
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return

    with open(filepath, "r") as f:
        code_text = f.read()

    print("1. Extracting Requirements...")
    reqs = extract_requirements(PROBLEM_TEXT)
    
    print("2. Analyzing Code...")
    analysis = analyze_code(code_text)
    
    print("3. Aligning...")
    alignment_data = align_spec_code(reqs, code_text, analysis)
    
    print("4. Scoring...")
    # Assuming 0 risk for this test
    score_data = calculate_score(alignment_data, risk_score=0.0)
    
    print(f"\n[SCORE] Overall Score: {score_data['final_score']}/100")
    print("\n--- Detailed Scores ---")
    scores = alignment_data.get("scores", {})
    for key, val in scores.items():
        print(f"{key.replace('_', ' ').capitalize()}: {val.get('score')}/100")
        print(f"  Reason: {val.get('reasoning')[:100]}...")

if __name__ == "__main__":
    edge_cases = ["lis_empty.py", "lis_decreasing.py", "lis_duplicate.py"]
    for case in edge_cases:
        test_file(case)
