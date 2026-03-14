"""Data loading helpers and consistent Plotly theming for the CS418 project.

Loads from local CSVs in collected_data/ (and sample_data/ for channels).
"""

import json
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from pathlib import Path

# ── Data paths ───────────────────────────────────────────────────────────────
_PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = _PROJECT_ROOT / "collected_data"
SAMPLE_DIR = _PROJECT_ROOT / "sample_data"


def table(name: str) -> str:
    """Kept for compatibility with notebooks that use SQL strings.
    Returns table name as-is since we're loading from CSVs now."""
    return name


def query_to_df(sql: str) -> pd.DataFrame:
    """Not available in local mode. Raises an error with guidance."""
    raise NotImplementedError(
        "BigQuery is not available. Use load_videos(), load_channels(), "
        "or load_comments() instead, or load CSVs directly."
    )


# ── Convenience loaders ──────────────────────────────────────────────────────

def load_channels() -> pd.DataFrame:
    """Load channels from sample_data/channel_data.json."""
    with open(SAMPLE_DIR / "channel_data.json") as f:
        channels = json.load(f)
    df = pd.DataFrame(channels)
    for col in ["view_count", "subscriber_count", "video_count"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def load_videos(columns: list[str] | None = None) -> pd.DataFrame:
    """Load video data from collected_data/video_data.csv."""
    df = pd.read_csv(DATA_DIR / "video_data.csv", low_memory=False)
    if "published_at" in df.columns:
        df["published_at"] = pd.to_datetime(df["published_at"], errors="coerce", utc=True)
    for col in ["view_count", "like_count", "comment_count"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    if columns:
        available = [c for c in columns if c in df.columns]
        df = df[available]
    return df


def load_comments(limit: int | None = None, sample_frac: float | None = None) -> pd.DataFrame:
    """Load comments from collected_data/comments.csv.

    Args:
        limit: hard row cap
        sample_frac: approximate fraction to sample
    """
    df = pd.read_csv(DATA_DIR / "comments.csv", low_memory=False)
    df["published_at"] = pd.to_datetime(df["published_at"], errors="coerce", utc=True)

    if sample_frac:
        df = df.sample(frac=sample_frac, random_state=42)
    if limit:
        df = df.head(limit)

    return df


# ── Plotly theme ─────────────────────────────────────────────────────────────

COLORS = {
    "primary": "#1f77b4",
    "secondary": "#ff7f0e",
    "anomaly": "#d62728",
    "cluster": ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
                 "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"],
    "bg": "#fafafa",
    "grid": "#e5e5e5",
}

_template = go.layout.Template(
    layout=go.Layout(
        font=dict(family="Inter, system-ui, sans-serif", size=13),
        plot_bgcolor=COLORS["bg"],
        paper_bgcolor="white",
        colorway=COLORS["cluster"],
        xaxis=dict(gridcolor=COLORS["grid"], showgrid=True),
        yaxis=dict(gridcolor=COLORS["grid"], showgrid=True),
        title=dict(font=dict(size=18), x=0.02, xanchor="left"),
        margin=dict(l=60, r=30, t=60, b=50),
        hoverlabel=dict(bgcolor="white", font_size=12),
    )
)
pio.templates["cs418"] = _template
pio.templates.default = "cs418"
