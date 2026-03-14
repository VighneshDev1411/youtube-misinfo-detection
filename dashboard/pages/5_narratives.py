"""Narrative Analysis — Topics & Sentiment Trends."""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from utils.conflict_timeline import EVENTS_DF, add_event_annotations

st.header("Narrative & Sentiment Analysis")

DATA_DIR = Path(__file__).parent.parent / "data"
SENTIMENT_FILE = DATA_DIR / "sentiment_timeseries.csv"
TOPICS_FILE = DATA_DIR / "topics_over_time.csv"
CLASSIFICATIONS_FILE = DATA_DIR / "comment_classifications.csv"

if not SENTIMENT_FILE.exists() and not TOPICS_FILE.exists():
    st.warning("Run `task5_.../nlp_analysis.ipynb` first to generate data.")
    st.stop()

# ── Sentiment Over Time ─────────────────────────────────────────────────────
if SENTIMENT_FILE.exists():
    st.subheader("Sentiment Over Time")
    sent = pd.read_csv(SENTIMENT_FILE)
    sent["date"] = pd.to_datetime(sent["date"])

    fig = go.Figure()
    for col in ["positive", "negative", "neutral"]:
        if col in sent.columns:
            colors = {"positive": "#2ca02c", "negative": "#d62728", "neutral": "#7f7f7f"}
            fig.add_trace(go.Scatter(
                x=sent["date"], y=sent[col], mode="lines",
                name=col.title(), line=dict(color=colors.get(col, "#1f77b4"))
            ))
    fig = add_event_annotations(fig)
    fig.update_layout(title="Weekly Sentiment Proportions", height=500,
                      xaxis_title="Date", yaxis_title="Proportion")
    st.plotly_chart(fig, use_container_width=True)

# ── Topic Explorer ───────────────────────────────────────────────────────────
if TOPICS_FILE.exists():
    st.subheader("Topic Evolution Over Time")
    topics = pd.read_csv(TOPICS_FILE)

    if "Timestamp" in topics.columns and "Topic" in topics.columns:
        topics["Timestamp"] = pd.to_datetime(topics["Timestamp"])
        topic_list = sorted(topics["Topic"].unique())
        selected_topics = st.multiselect("Select topics to display",
                                          topic_list, default=topic_list[:5])

        filtered = topics[topics["Topic"].isin(selected_topics)]
        fig2 = px.line(filtered, x="Timestamp", y="Frequency",
                       color="Name" if "Name" in filtered.columns else "Topic",
                       title="Topic Frequency Over Time")
        fig2 = add_event_annotations(fig2)
        st.plotly_chart(fig2, use_container_width=True)

# ── Misinformation Distribution ─────────────────────────────────────────────
if CLASSIFICATIONS_FILE.exists():
    st.subheader("Misinformation Classification")
    clf = pd.read_csv(CLASSIFICATIONS_FILE)

    if "misinfo_label" in clf.columns:
        dist = clf["misinfo_label"].value_counts().reset_index()
        dist.columns = ["Label", "Count"]
        fig3 = px.pie(dist, values="Count", names="Label",
                      title="Comment Classification Distribution")
        st.plotly_chart(fig3, use_container_width=True)

    if "sentiment" in clf.columns:
        st.subheader("Sentiment Distribution")
        sent_dist = clf["sentiment"].value_counts().reset_index()
        sent_dist.columns = ["Sentiment", "Count"]
        fig4 = px.bar(sent_dist, x="Sentiment", y="Count",
                      title="Overall Sentiment Distribution",
                      color="Sentiment",
                      color_discrete_map={"positive": "#2ca02c",
                                          "negative": "#d62728",
                                          "neutral": "#7f7f7f"})
        st.plotly_chart(fig4, use_container_width=True)
