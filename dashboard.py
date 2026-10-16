import streamlit as st
import pandas as pd
import joblib
import os

st.set_page_config(page_title="Git Repo Risk Predictor", layout="wide")

# 1. Load the ML brain directly
if os.path.exists("bug_predictor.pkl"):
    model = joblib.load("bug_predictor.pkl")
else:
    st.error("Model brain file bug_predictor.pkl not found!")

st.title("📊 Git Repository Risk Assessment & Defect Predictor")

# 2. READ THE CODE DIRECTLY FROM SAMPLE_APP.PY
code_complexity = 0
lines_added = 0

if os.path.exists("sample_app.py"):
    with open("sample_app.py", "r") as f:
        lines = f.readlines()
        lines_added = len(lines)
        # Directly count the depth of nested loops
        for line in lines:
            if "for " in line:
                code_complexity += 1.5  # Add complexity weight for each loop found

# 3. RUN REAL-TIME ML INFERENCE INSTANTLY (Fixed to lowercase to match the model!)
input_data = pd.DataFrame([[lines_added, 0, code_complexity]], 
                           columns=['lines_added', 'lines_deleted', 'code_complexity'])

# Predict probability percentage
risk_probability = model.predict_proba(input_data)[0][1] * 100

# 4. SHOW THE OUTPUT BOXES
col1, col2 = st.columns(2)
col1.metric("Current Code Complexity", f"{code_complexity:.2f}")
col2.metric("Lines Evaluated", f"{lines_added}")

# 5. THE OUTPUT GATE BANNER
st.subheader("🛡️ Real-Time Risk Predictor Gate")
if risk_probability > 50 or code_complexity >= 4.0:
    st.error(f"🚨 CRITICAL RISK (Defect Propensity Score: {risk_probability:.1f}%)")
    st.warning("Recommendation: Reject pull request. Code structure contains highly volatile nested structures.")
else:
    st.success(f"✅ SAFE (Defect Propensity Score: {risk_probability:.1f}%)")
    st.info("Recommendation: Approve commit pipeline. Code architecture is linear and clean.")
