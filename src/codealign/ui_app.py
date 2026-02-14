import streamlit as st
import json
import os
import requests
import sys
from dotenv import load_dotenv

# Fix ModuleNotFoundError: Add 'src' to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__)) # .../src/codealign
src_dir = os.path.dirname(current_dir) # .../src
sys.path.insert(0, src_dir)

# Import logic
from codealign.alignment.behaviour_extract import extract_requirements
from codealign.alignment.code_analysis import analyze_code
from codealign.alignment.align_reasoner import align_spec_code
from codealign.cohort_stats import calculate_score
from codealign.authenticity.ingest import ingest_submission, get_all_submissions
from codealign.authenticity.similarity import calculate_similarity
from codealign.authenticity.ai_signals import detect_ai_signals

# -----------------------------------------------------------------------------
# Configuration & Styling
# -----------------------------------------------------------------------------
st.set_page_config(page_title="CodeAlign AI", page_icon="🧩", layout="wide")

# Custom CSS for polished look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=JetBrains+Mono:wght@400;700&display=swap');

    /* Global Font & Colors */
    :root {
        --primary-color: #2563EB; /* Royal Blue 600 */
        --success-color: #059669; /* Emerald 600 */
        --warning-color: #D97706; /* Amber 600 */
        --danger-color: #DC2626; /* Red 600 */
        --bg-color: #F8FAFC;      /* Slate 50 */
        --text-color: #1E293B;    /* Slate 800 */
    }

    html, body, [class*="css"] {
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
        color: var(--text-color);
    }
    
    code, pre {
        font-family: 'JetBrains Mono', monospace;
    }

    .main-header {
        font-size: 2.8rem;
        font-weight: 800;
        color: #1E293B;
        margin-bottom: 0.1rem;
        letter-spacing: -0.03em;
        background: -webkit-linear-gradient(45deg, #2563EB, #4F46E5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .sub-header {
        font-size: 1.1rem;
        color: #64748B;
        margin-bottom: 3rem;
        font-weight: 400;
    }

    /* Cards */
    .metric-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
        border: 1px solid #E2E8F0;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
        padding: 8px 0;
        border-bottom: 2px solid #E2E8F0;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        border-radius: 6px;
        padding: 0 16px;
        font-weight: 600;
        border: none;
        background-color: transparent;
        color: #64748B;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #EFF6FF;
        color: var(--primary-color);
        border-bottom: 2px solid var(--primary-color);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #F8FAFC;
        border-right: 1px solid #E2E8F0;
    }
    
    .sidebar-logo {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 0;
        margin-bottom: 20px;
    }
    
    .logo-icon {
        font-size: 2rem;
        background: #2563EB;
        color: white;
        width: 48px;
        height: 48px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 10px;
        font-weight: bold;
    }
    
    .logo-text {
        font-size: 1.4rem;
        font-weight: 800;
        color: #1E293B;
        letter-spacing: -0.02em;
    }

</style>
""", unsafe_allow_html=True)

# Load environment variables
load_dotenv()

# Verify API Keys
if "GROQ_API_KEY" not in os.environ:
    st.error("❌ `GROQ_API_KEY` is missing. Please check your .env file.")
    st.stop()

# -----------------------------------------------------------------------------
# Sample Data
# -----------------------------------------------------------------------------
SAMPLE_PROBLEM = """Given an integer array nums, return the length of the longest strictly increasing subsequence.

Example 1:
Input: nums = [10,9,2,5,3,7,101,18]
Output: 4
Explanation: The longest increasing subsequence is [2,3,7,101], therefore the length is 4.

Constraints:
- 1 <= nums.length <= 2500
- -10^4 <= nums[i] <= 10^4
- Time Complexity should be better than O(n^2)
"""

SAMPLE_CODE = """def lengthOfLIS(nums):
    if not nums:
        return 0
    tails = []
    for num in nums:
        import bisect
        idx = bisect.bisect_left(tails, num)
        if idx < len(tails):
            tails[idx] = num
        else:
            tails.append(num)
    return len(tails)
"""

SAMPLES = {
    "Python": {
        "problem": SAMPLE_PROBLEM,
        "code": SAMPLE_CODE
    },
    "C++": {
        "problem": SAMPLE_PROBLEM,
        "code": """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int lengthOfLIS(vector<int>& nums) {
        if (nums.empty()) return 0;
        vector<int> tails;
        for (int num : nums) {
            auto it = lower_bound(tails.begin(), tails.end(), num);
            if (it == tails.end()) {
                tails.push_back(num);
            } else {
                *it = num;
            }
        }
        return tails.size();
    }
};"""
    },
    "Java": {
        "problem": SAMPLE_PROBLEM,
        "code": """import java.util.ArrayList;
import java.util.Collections;

class Solution {
    public int lengthOfLIS(int[] nums) {
        if (nums.length == 0) return 0;
        ArrayList<Integer> tails = new ArrayList<>();
        
        for (int num : nums) {
            int idx = Collections.binarySearch(tails, num);
            if (idx < 0) idx = -(idx + 1);
            
            if (idx == tails.size()) {
                tails.add(num);
            } else {
                tails.set(idx, num);
            }
        }
        return tails.size();
    }
}"""
    },
    "C": {
        "problem": SAMPLE_PROBLEM,
        "code": """#include <stdio.h>
#include <stdlib.h>

int lengthOfLIS(int* nums, int numsSize) {
    if (numsSize == 0) return 0;
    
    int* tails = (int*)malloc(numsSize * sizeof(int));
    int size = 0;
    
    for (int i = 0; i < numsSize; i++) {
        int l = 0, r = size;
        while (l < r) {
            int m = l + (r - l) / 2;
            if (tails[m] < nums[i])
                l = m + 1;
            else
                r = m;
        }
        if (l == size) {
            tails[size++] = nums[i];
        } else {
            tails[l] = nums[i];
        }
    }
    
    free(tails);
    return size;
}"""
    },
    "JavaScript": {
        "problem": SAMPLE_PROBLEM,
        "code": """/**
 * @param {number[]} nums
 * @return {number}
 */
var lengthOfLIS = function(nums) {
    if (nums.length === 0) return 0;
    const tails = [];
    
    for (const num of nums) {
        let i = 0, j = tails.length;
        while (i < j) {
            const m = Math.floor((i + j) / 2);
            if (tails[m] < num)
                i = m + 1;
            else
                j = m;
        }
        if (i === tails.length)
            tails.push(num);
        else
            tails[i] = num;
    }
    return tails.length;
};"""
    }
}

# -----------------------------------------------------------------------------
# Sidebar
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="logo-icon">CA</div>
        <div class="logo-text">CodeAlign</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(
        "**Smart Evaluation System**\n\n"
        "Go beyond Pass/Fail. Get insights on:\n"
        "- ✅ Correctness\n"
        "- ⚡ Efficiency\n"
        "- 🧹 Readability\n"
        "- 🕵️ Authenticity"
    )
    st.markdown("---")
    st.markdown("---")
    st.caption("v1.0.0 Hackathon Edition")
    
    # Session Simulation
    st.markdown("### 🔧 Debug / Demo")
    student_id = st.text_input("Simulate Student ID", value="Student_1", help="Change this ID to test plagiarism detection between different users.")

# -----------------------------------------------------------------------------
# Header
# -----------------------------------------------------------------------------
st.markdown('<div class="main-header">🧩 CodeAlign</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-Powered Assignment Evaluator & Authenticity Detector</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Main Layout
# -----------------------------------------------------------------------------
# Initialize session state for inputs if not present
if "problem_input" not in st.session_state:
    st.session_state.problem_input = ""
if "code_input" not in st.session_state:
    st.session_state.code_input = ""

# Layout Columns
left_col, right_col = st.columns([1, 1], gap="large")

with left_col:
    st.markdown("### 1️⃣ Input")
    
    # Language Select
    lang = st.selectbox("Programming Language", ["Python", "C++", "Java", "C", "JavaScript"], key="language")
    
    # helper to load sample
    if st.button(f"🪄 Load {lang} Sample", use_container_width=True):
        sample = SAMPLES.get(lang)
        if sample:
            st.session_state["problem_area"] = sample["problem"]
            st.session_state["code_area"] = sample["code"]
            st.rerun()
        else:
            st.warning(f"No sample available for {lang}")

    st.markdown("#### Problem Statement")
    problem_text = st.text_area(
        "Paste the problem description here...",
        height=250,
        key="problem_area"
    )
    
    st.markdown("#### Candidate Submission")
    input_tab1, input_tab2 = st.tabs(["📝 Paste Code", "📁 Upload File"])
    
    with input_tab1:
        code_text_input = st.text_area(
            "Paste code here...",
            height=250,
            key="code_area"
        )
    
    with input_tab2:
        uploaded_file = st.file_uploader("Upload .py, .txt, .c, .cpp", type=["py", "txt", "c", "cpp", "java"])
    
    # Determine source
    final_code = code_text_input
    source_label = "Text Input"
    
    if uploaded_file is not None:
        uploaded_file.seek(0)
        content = uploaded_file.read().decode("utf-8")
        if content:
            final_code = content
            source_label = f"File: {uploaded_file.name}"
            st.success(f"✅ Loaded {source_label}")

    analyze_btn = st.button("🚀 Analyze Submission", type="primary", use_container_width=True)


# -----------------------------------------------------------------------------
# Logic & Results
# -----------------------------------------------------------------------------

if "language" not in st.session_state:
    st.session_state.language = "Python"

if analyze_btn:
    if not problem_text.strip():
        st.error("⚠️ Please enter a problem statement.")
        st.stop()
    if not final_code.strip():
        st.error("⚠️ Please provide code to analyze.")
        st.stop()
    
    # Auto-detect language if file upload
    detected_lang = st.session_state.language
    if uploaded_file:
        ext = uploaded_file.name.split('.')[-1].lower()
        mapping = {'py': 'Python', 'cpp': 'C++', 'c': 'C', 'java': 'Java', 'js': 'JavaScript'}
        detected_lang = mapping.get(ext, "Python")

    with right_col:
        st.markdown("### 2️⃣ Analysis Report")
        status_container = st.container()
        
        with st.status(f"🔍 Analyzing {detected_lang} Code...", expanded=True) as status:
            st.write("Extracting requirements...")
            reqs = extract_requirements(problem_text)
            
            st.write(f"Analyzing {detected_lang} code structure...")
            # Pass language to analyzer
            analysis = analyze_code(final_code, language=detected_lang)
            
            if analysis.get("error"):
                st.error(analysis["error"])
                st.stop()
            
            st.write("Evaluating alignment & correctness...")
            # Pass language to reasoner
            alignment_data = align_spec_code(reqs, final_code, analysis, language=detected_lang)
            
            st.write("Checking authenticity...")
            max_sim = 0.0
            try:
                # Ingest as the current simulated student
                current_id = ingest_submission(final_code, student_id=student_id)['id']
                
                others = get_all_submissions("default")
                
                # Use the new function for plagiarism check
                from codealign.authenticity.similarity import find_similar
                
                # Check against everyone EXCEPT the current simulated student
                similar_matches = find_similar(final_code, others, threshold=0.01, exclude_candidate_id=student_id)
                
                if similar_matches:
                    max_sim = max(s['similarity_score'] for s in similar_matches)
                else:
                    max_sim = 0.0
            except Exception as e:
                print(f"Auth check failed: {e}")

            ai_signals = detect_ai_signals(final_code)
            risk_score = max(max_sim * 100, ai_signals['confidence'] * 100)
            
            score_data = calculate_score(alignment_data, risk_score)
            status.update(label="✅ Analysis Complete!", state="complete", expanded=False)

        # --- RESULTS DISPLAY ---
        
        # 1. Overview Card
        final_score = score_data['final_score']
        score_color = "#4CAF50" if final_score >= 80 else "#FFC107" if final_score >= 50 else "#F44336"
        
        st.markdown(f"""
        <div style="background-color: white; border: 1px solid #ddd; border-radius: 10px; padding: 20px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
            <h3 style="margin:0; color: #555;">Overall Alignment Score</h3>
            <div style="font-size: 64px; font-weight: 800; color: {score_color}; line-height: 1.2;">
                {final_score}
            </div>
            <p style="margin:0; color: #888;">out of 100</p>
        </div>
        <br>
        """, unsafe_allow_html=True)

        res_tab1, res_tab2, res_tab3, res_tab4 = st.tabs([
            "📊 Dashboard", "✅ Requirements", "💡 Feedback", "🕵️ Authenticity"
        ])
        
        breakdown = score_data.get('breakdown', {})
        raw_scores = alignment_data.get("scores", {})

        with res_tab1:
            st.markdown("#### Performance Dimensions")
            q1, q2 = st.columns(2)
            q3, q4 = st.columns(2)
            
            def metric_box(col, label, key):
                val = breakdown.get(key, 0)
                reason = raw_scores.get(key, {}).get("reasoning", "N/A")
                col.metric(label, f"{val}/100")
                col.caption(reason)

            metric_box(q1, "Correctness", "correctness")
            metric_box(q2, "Time Efficiency", "time_efficiency")
            metric_box(q3, "Space Efficiency", "space_efficiency")
            metric_box(q4, "Readability", "readability")

        with res_tab2:
            st.markdown("#### Problem Alignment Checklist")
            align_items = alignment_data.get("alignment", [])
            if not align_items:
                st.warning("No specific requirements extracted.")
            
            for item in align_items:
                status = item.get('status', 'unknown').lower()
                icon = "✅" if status == 'fulfilled' else "⚠️" if status == 'partial' else "❌"
                
                with st.expander(f"{icon} {item['requirement']}"):
                    st.write(f"**Status:** {status.upper()}")
                    st.write(f"**Type:** {item.get('type', 'Functional')}")
                    st.markdown(f"**Evidence:** _{item.get('evidence', 'No evidence provided.')}_")

        with res_tab3:
            st.markdown("#### Improvement Report")
            feedback = alignment_data.get("feedback", {})
            
            if feedback.get("strengths"):
                st.write("**✅ Strengths**")
                for s in feedback['strengths']:
                    st.success(f"• {s}")
            
            if feedback.get("weaknesses"):
                st.write("**⚠️ Weaknesses**")
                for w in feedback['weaknesses']:
                    st.error(f"• {w}")
            
            if feedback.get("improvement_suggestions"):
                st.write("**🚀 Suggestions**")
                for i in feedback['improvement_suggestions']:
                    st.info(f"• {i}")
            
            if feedback.get("better_approach"):
                with st.expander("✨ View Better Solution Approach"):
                    st.markdown(feedback["better_approach"])

        with res_tab4:
            st.markdown("#### Authenticity Analysis")
            
            risk_label = "High" if risk_score > 70 else "Moderate" if risk_score > 30 else "Low"
            risk_color = "red" if risk_score > 70 else "orange" if risk_score > 30 else "green"
            
            c1, c2 = st.columns([1, 2])
            with c1:
                st.metric("Risk Level", f"{risk_label}", f"{int(risk_score)}%")
            
            with c2:
                if max_sim > 0.8:
                    st.error(f"🚨 High similarity ({max_sim:.2f}) to a previous submission.")
                
                if ai_signals.get('signals'):
                    st.warning("**AI Signals Detected:**")
                    for sig in ai_signals['signals']:
                        st.write(f"• {sig}")
                elif max_sim <= 0.8:
                    st.success("No strong evidence of plagiarism or AI generation.")
