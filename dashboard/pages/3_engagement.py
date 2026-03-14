"""Engagement Anomaly Detection page."""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from utils.conflict_timeline import EVENTS_DF, add_event_annotations

st.header("Engagement Analysis & Anomaly Detection")

DATA_DIR = Path(__file__).parent.parent / "data"
ANOMALY_FILE = DATA_DIR / "video_anomaly_scores.csv"
TS_FILE = DATA_DIR / "engagement_timeseries.csv"

if not ANOMALY_FILE.exists() or not TS_FILE.exists():
    st.warning("Run `task3_.../engagement_analysis.ipynb` first to generate data.")
    st.stop()

anomalies = pd.read_csv(ANOMALY_FILE)
ts = pd.read_csv(TS_FILE)
ts["date"] = pd.to_datetime(ts["date"])

# ── Summary ──────────────────────────────────────────────────────────────────
st.subheader("Anomaly Summary")
cols = st.columns(4)
n_anomalous = anomalies["anomaly_label"].sum() if "anomaly_label" in anomalies.columns else 0
cols[0].metric("Total Videos Scored", f"{len(anomalies):,}")
cols[1].metric("Anomalous Videos", f"{n_anomalous:,}")
cols[2].metric("Anomaly Rate", f"{n_anomalous / len(anomalies) * 100:.1f}%")
cols[3].metric("Channels with Anomalies",
               f"{anomalies[anomalies.get('anomaly_label', pd.Series()) == 1]['channel_id'].nunique():,}"
               if "anomaly_label" in anomalies.columns else "N/A")

# ── Time series with events ──────────────────────────────────────────────────
st.subheader("Engagement Over Time")
metric = st.selectbox("Metric", ["view_count", "like_count", "comment_count"])

if metric in ts.columns:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=ts["date"], y=ts[metric], mode="lines",
                             name=metric, line=dict(color="#1f77b4")))

    if f"{metric}_anomaly" in ts.columns:
        anom = ts[ts[f"{metric}_anomaly"] == True]
        fig.add_trace(go.Scatter(x=anom["date"], y=anom[metric], mode="markers",
                                 name="Anomaly", marker=dict(color="red", size=8)))

    fig = add_event_annotations(fig)
    fig.update_layout(title=f"Daily {metric} with Conflict Events", height=500,
                      xaxis_title="Date", yaxis_title=metric)
    st.plotly_chart(fig, use_container_width=True)

# ── Top anomalous channels ──────────────────────────────────────────────────
st.subheader("Most Anomalous Channels")
if "anomaly_score" in anomalies.columns:
    channel_agg = (
        anomalies.groupby(["channel_id"])
        .agg(
            anomalous_videos=("anomaly_label", "sum"),
            total_videos=("anomaly_label", "count"),
            mean_anomaly_score=("anomaly_score", "mean"),
        )
        .assign(anomaly_fraction=lambda x: x["anomalous_videos"] / x["total_videos"])
        .sort_values("anomaly_fraction", ascending=False)
        .head(20)
        .reset_index()
    )
    channel_agg.index += 1
    st.dataframe(channel_agg, use_container_width=True)

# ── Anomaly scatter ──────────────────────────────────────────────────────────
st.subheader("Anomaly Scatter Plot")
if all(c in anomalies.columns for c in ["view_count", "like_count", "anomaly_label"]):
    sample = anomalies.sample(min(5000, len(anomalies)), random_state=42)
    fig2 = px.scatter(sample, x="view_count", y="like_count",
                      color="anomaly_label", opacity=0.5,
                      title="View Count vs Like Count (colored by anomaly)",
                      log_x=True, log_y=True)
    st.plotly_chart(fig2, use_container_width=True)
