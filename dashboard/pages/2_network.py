"""Network Analysis page — Interactive channel network graph."""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

st.header("Channel Network Analysis")

DATA_DIR = Path(__file__).parent.parent / "data"
CLUSTERS_FILE = DATA_DIR / "channel_clusters.csv"
CENTRALITY_FILE = DATA_DIR / "channel_centrality_metrics.csv"

if not CLUSTERS_FILE.exists():
    st.warning("Run `task2_network_analysis/network_analysis.ipynb` first to generate data.")
    st.stop()

df = pd.read_csv(CLUSTERS_FILE)

# ── Summary metrics ──────────────────────────────────────────────────────────
st.subheader("Network Summary")
cols = st.columns(4)
cols[0].metric("Channels", f"{len(df):,}")
cols[1].metric("Communities", df["cluster_id"].nunique())
cols[2].metric("Mean PageRank", f"{df['pagerank'].mean():.4f}")
cols[3].metric("Max PageRank", f"{df['pagerank'].max():.4f}")

# ── Cluster size distribution ────────────────────────────────────────────────
st.subheader("Community Sizes")
cluster_sizes = df["cluster_id"].value_counts().reset_index()
cluster_sizes.columns = ["Cluster", "Count"]
fig = px.bar(cluster_sizes.head(20), x="Cluster", y="Count",
             title="Top 20 Communities by Size")
st.plotly_chart(fig, use_container_width=True)

# ── Top channels by PageRank ─────────────────────────────────────────────────
st.subheader("Top Channels by PageRank")
top = df.nlargest(20, "pagerank")[["channel_title", "cluster_id", "pagerank", "degree"]].reset_index(drop=True)
top.index += 1
st.dataframe(top, use_container_width=True)

fig2 = px.bar(top, x="pagerank", y="channel_title", orientation="h",
              color="cluster_id", title="Top 20 Channels by PageRank")
fig2.update_layout(yaxis=dict(autorange="reversed"), height=600)
st.plotly_chart(fig2, use_container_width=True)

# ── Cluster filter ───────────────────────────────────────────────────────────
st.subheader("Explore by Cluster")
selected = st.selectbox("Select cluster", sorted(df["cluster_id"].unique()))
filtered = df[df["cluster_id"] == selected].sort_values("pagerank", ascending=False)
st.dataframe(filtered[["channel_title", "pagerank", "degree"]].head(20), use_container_width=True)
