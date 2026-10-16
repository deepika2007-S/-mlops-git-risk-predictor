import streamlit as st
import pandas as pd
import plotly.express as px
import os
import joblib
from radon.complexity import cc_visit

# 1. Page Configuration layout
st.set_page_config(page_title="MLOps Git Risk Dashboard", layout="wide")
st.title("🛡️ MLOps Git Repository Risk Assessment Dashboard")
st.markdown("Real-time visual monitoring of code metrics and machine learning defect predictions.")

# 2. Check and load the dataset
csv_path = 'dataset.csv'
model_path = 'bug_predictor.pkl'

if not os.path.exists(csv_path):
    st.error(f"Error: {csv_path} not found. Please run your data miner script first.")
    st.stop()

df = pd.read_csv(csv_path)

# 3. Sidebar Configuration for File Simulation
st.sidebar.header("🔍 Real-Time Code File Simulator")
st.sidebar.markdown("Simulate a live developer code change to evaluate risk patterns visually.")

lines_added = st.sidebar.number_input("Lines Added", min_value=0, max_value=500, value=25)
lines_deleted = st.sidebar.number_input("Lines Deleted", min_value=0, max_value=500, value=5)
raw_code = st.sidebar.text_area("Paste Code Modification snippet:", value='def test_func():\n    for i in range(10):\n        print(i)')

# Calculate code complexity of text area dynamically
def get_complexity(content):
    try:
        blocks = cc_visit(content)
        return sum([b.complexity for b in blocks]) / len(blocks) if blocks else 1.0
    except:
        return 1.0

calculated_complexity = get_complexity(raw_code)
st.sidebar.info(f"Calculated Complexity Index: {calculated_complexity:.2f}")

# 4. Main Metric Cards row
st.subheader("📊 Repository Overview Metrics")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Commits Evaluated", len(df))
with col2:
    st.metric("Average Lines Added", f"{df['lines_added'].mean():.1f}")
with col3:
    st.metric("Average Code Complexity", f"{df['code_complexity'].mean():.2f}")
with col4:
    total_bugs = int(df['is_bug_prone'].sum())
    st.metric("Defects Prevented", total_bugs)

st.markdown("---")

# 5. Live Machine Learning Prediction Section
st.subheader("🎯 Real-Time Risk Predictor Gate")
if os.path.exists(model_path):
    model = joblib.load(model_path)
    # Perform instant calculation matrix
    features = [[lines_added, lines_deleted, calculated_complexity]]
    risk_proba = model.predict_proba(features)[0][1] * 100
    
    if risk_proba >= 60.0:
        st.error(f"❌ HIGH RISK ALERT: Defect Propensity Score is {risk_proba:.1f}%. This change would be BLOCKED.")
    elif risk_proba >= 35.0:
        st.warning(f"⚠️ WARNING: Defect Propensity Score is {risk_proba:.1f}%. Review structural code duplication.")
    else:
        st.success(f"✅ SAFE: Defect Propensity Score is {risk_proba:.1f}%. Optimal risk status matrix metrics.")
else:
    st.warning("Pre-trained model file 'bug_predictor.pkl' not found. Please train the model to enable live predictions.")

st.markdown("---")

# 6. Interactive Visualizations Layout
st.subheader("📈 Historical Code Metric Explorations")
viz_col1, viz_col2 = st.columns(2)

with viz_col1:
    fig_scatter = px.scatter(
        df, x='lines_added', y='code_complexity', color='is_bug_prone',
        title="Lines Added vs Code Complexity Patterns",
        labels={'lines_added': 'Lines Added', 'code_complexity': 'Complexity Index', 'is_bug_prone': 'Is Bug Prone'},
        color_continuous_scale=px.colors.sequential.Reds
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

with viz_col2:
    fig_hist = px.histogram(
        df, x='lines_deleted', color='is_bug_prone', barmode='overlay',
        title="Distribution of Deleted Lines across Commit Profiles",
        labels={'lines_deleted': 'Lines Deleted', 'count': 'Commit Frequency'}
    )
    st.plotly_chart(fig_hist, use_container_width=True)
