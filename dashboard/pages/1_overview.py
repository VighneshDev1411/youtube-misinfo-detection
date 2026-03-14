"""Overview page — KPI cards, dataset stats, pipeline diagram."""

import streamlit as st
import pandas as pd
from pathlib import Path

st.header("Project Overview")

DATA_DIR = Path(__file__).parent.parent / "data"

# ── KPI Cards ────────────────────────────────────────────────────────────────
st.subheader("Dataset at a Glance")

kpi_cols = st.columns(5)
kpis = [
    ("Channels", "1,561"),
    ("Videos", "440,772"),
    ("Comments", "1.06M+"),
    ("Comment Tables", "5"),
    ("Date Range", "2017–2024"),
]
for col, (label, value) in zip(kpi_cols, kpis):
    col.metric(label, value)

st.markdown("---")

# ── Data Pipeline ────────────────────────────────────────────────────────────
st.subheader("Data Pipeline Architecture")
st.markdown(
    """
    ```
    YouTube Data API v3
          │
          ├── Channel metadata ──► BigQuery: channels (1,561 rows)
          ├── Video metadata   ──► BigQuery: video_data (440,772 rows)
          └── Comments         ──► BigQuery: comment1..comment5 (1.06M+ rows)
                                        │
                    ┌───────────────────┼───────────────────┐
                    ▼                   ▼                   ▼
            Task 2: Network     Task 3: Engagement    Task 4: Commenter
            (tag overlap,       (Z-score, Isolation   (co-occurrence,
             co-posting)         Forest)               bot detection)
                    │                   │                   │
                    └───────────────────┼───────────────────┘
                                        ▼
                              Task 5: NLP Analysis
                              (sentiment, BERTopic,
                               misinfo classification)
                                        │
                                        ▼
                              Streamlit Dashboard
    ```
    """
)

st.markdown("---")

# ── Load & show summary tables if available ──────────────────────────────────
st.subheader("Analysis Outputs")

files = {
    "Channel Clusters": DATA_DIR / "channel_clusters.csv",
    "Video Anomaly Scores": DATA_DIR / "video_anomaly_scores.csv",
    "Commenter Bot Scores": DATA_DIR / "commenter_bot_scores.csv",
    "Comment Classifications": DATA_DIR / "comment_classifications.csv",
}

for name, path in files.items():
    if path.exists():
        df = pd.read_csv(path)
        with st.expander(f"{name} ({len(df):,} rows)"):
            st.dataframe(df.head(20), use_container_width=True)
    else:
        st.info(f"{name}: Run the corresponding notebook to generate this data.")

# ── Hypotheses ───────────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("Research Hypotheses")

st.markdown(
    """
    | # | Hypothesis | Task |
    |---|-----------|------|
    | H1 | Coordinated channel clusters amplify misinformation more than isolated channels | Task 2 (Network) |
    | H2 | Major conflict events correlate with engagement anomalies | Task 3 (Engagement) |
    | H3 | Narrative topics evolve in alignment with key war events | Task 5 (NLP) |
    """
)

# ── Team ─────────────────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("Author")
st.markdown("**Vignesh Pathak** — [@VighneshDev1411](https://github.com/VighneshDev1411)")
st.caption("CS 418 — University of Illinois Chicago")
