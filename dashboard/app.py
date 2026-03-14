"""
Coordinated Amplification & Misinformation Detection Dashboard
CS418 — The Fact Finders
"""

import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="YouTube Misinfo Detection",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_DIR = Path(__file__).parent / "data"

st.sidebar.title("YouTube Misinfo Detection")
st.sidebar.caption("CS 418 — Vignesh Pathak")
st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    **Pages**
    - Overview — Dataset stats & pipeline
    - Network — Channel network graph
    - Engagement — Anomaly detection
    - Commenters — Bot detection
    - Narratives — Topics & sentiment
    - Classifier — Live comment classifier
    """
)

st.title("Coordinated Amplification & Misinformation Detection")
st.subheader("Global YouTube Conflict Narratives")

st.markdown("---")
st.markdown("Use the **sidebar** to navigate between analysis pages, or select a page below.")

cols = st.columns(3)
pages = [
    ("1_overview", "Overview", "Dataset statistics and data pipeline architecture"),
    ("2_network", "Network Analysis", "Channel network graph with community detection"),
    ("3_engagement", "Engagement Anomalies", "Time series anomaly detection with conflict events"),
    ("4_commenters", "Commenter Analysis", "Bot detection and commenter networks"),
    ("5_narratives", "Narrative Analysis", "Topic modeling and sentiment trends"),
    ("6_classifier", "Live Classifier", "Classify any comment for misinformation"),
]

for i, (key, title, desc) in enumerate(pages):
    with cols[i % 3]:
        st.markdown(f"### {title}")
        st.markdown(desc)
