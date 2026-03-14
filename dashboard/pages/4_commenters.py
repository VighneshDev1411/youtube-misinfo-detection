"""Commenter Analysis & Bot Detection page."""

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.header("Commenter Analysis & Bot Detection")

DATA_DIR = Path(__file__).parent.parent / "data"
BOT_FILE = DATA_DIR / "commenter_bot_scores.csv"
CLUSTERS_FILE = DATA_DIR / "commenter_clusters.csv"

if not BOT_FILE.exists():
    st.warning("Run `task4_.../commenter_analysis.ipynb` first to generate data.")
    st.stop()

bots = pd.read_csv(BOT_FILE)

# ── Summary ──────────────────────────────────────────────────────────────────
st.subheader("Bot Detection Summary")
cols = st.columns(4)
n_bots = bots["is_likely_bot"].sum() if "is_likely_bot" in bots.columns else 0
cols[0].metric("Total Commenters", f"{len(bots):,}")
cols[1].metric("Likely Bots", f"{n_bots:,}")
cols[2].metric("Bot Rate", f"{n_bots / len(bots) * 100:.1f}%")
cols[3].metric("Mean Bot Score", f"{bots['bot_score'].mean():.3f}")

# ── Bot score distribution ──────────────────────────────────────────────────
st.subheader("Bot Score Distribution")
fig = px.histogram(bots, x="bot_score", nbins=50,
                   title="Distribution of Bot Scores",
                   color_discrete_sequence=["#1f77b4"])
fig.add_vline(x=0.5, line_dash="dash", line_color="red",
              annotation_text="Bot threshold")
st.plotly_chart(fig, use_container_width=True)

# ── Top suspected bots ──────────────────────────────────────────────────────
st.subheader("Top Suspected Bots")
top_bots = bots.nlargest(20, "bot_score").reset_index(drop=True)
top_bots.index += 1
display_cols = [c for c in ["author_channel_id", "comment_count", "video_count",
                            "active_days", "bot_score"] if c in top_bots.columns]
st.dataframe(top_bots[display_cols], use_container_width=True)

# ── Activity patterns ────────────────────────────────────────────────────────
st.subheader("Commenter Activity Patterns")
if "comment_count" in bots.columns and "video_count" in bots.columns:
    sample = bots.sample(min(5000, len(bots)), random_state=42)
    fig2 = px.scatter(sample, x="video_count", y="comment_count",
                      color="bot_score", color_continuous_scale="RdYlBu_r",
                      title="Comment Count vs Video Count (colored by bot score)",
                      log_x=True, log_y=True, opacity=0.5)
    st.plotly_chart(fig2, use_container_width=True)

# ── Commenter clusters ──────────────────────────────────────────────────────
if CLUSTERS_FILE.exists():
    st.subheader("Commenter Communities")
    clusters = pd.read_csv(CLUSTERS_FILE)
    cluster_sizes = clusters["cluster_id"].value_counts().reset_index()
    cluster_sizes.columns = ["Cluster", "Members"]
    fig3 = px.bar(cluster_sizes.head(15), x="Cluster", y="Members",
                  title="Top 15 Commenter Communities by Size")
    st.plotly_chart(fig3, use_container_width=True)
