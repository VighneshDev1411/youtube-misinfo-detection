"""BigQuery helpers and consistent Plotly theming for the CS418 project."""

from google.cloud import bigquery
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

# ── BigQuery config ──────────────────────────────────────────────────────────
PROJECT_ID = "infinite-rope-363317"
DATASET = "youtube_data"

_client = None


def get_client():
    """Lazy-init BigQuery client."""
    global _client
    if _client is None:
        _client = bigquery.Client(project=PROJECT_ID)
    return _client


def query_to_df(sql: str) -> pd.DataFrame:
    """Run a SQL query and return a DataFrame."""
    return get_client().query(sql).to_dataframe()


def table(name: str) -> str:
    """Return fully-qualified table reference."""
    return f"`{PROJECT_ID}.{DATASET}.{name}`"


# ── Convenience loaders ──────────────────────────────────────────────────────

def load_channels() -> pd.DataFrame:
    """Load the channels table."""
    sql = f"""
    SELECT channel_id, channel_title, description, custom_url, created_at,
           country, view_count, subscriber_count, video_count
    FROM {table('channels')}
    """
    df = query_to_df(sql)
    for col in ["view_count", "subscriber_count", "video_count"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def load_videos(columns: list[str] | None = None) -> pd.DataFrame:
    """Load the video_data table (440K rows). Optionally select specific columns."""
    cols = ", ".join(columns) if columns else (
        "channel_id, channel_title, video_id, category_id, published_at, "
        "title, description, view_count, like_count, comment_count, tags"
    )
    sql = f"SELECT {cols} FROM {table('video_data')}"
    df = query_to_df(sql)
    if "published_at" in df.columns:
        df["published_at"] = pd.to_datetime(df["published_at"], errors="coerce", utc=True)
    for col in ["view_count", "like_count", "comment_count"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def load_comments(limit: int | None = None, sample_frac: float | None = None) -> pd.DataFrame:
    """Load comments from all 5 comment tables via UNION ALL.

    Args:
        limit: hard row cap (applied per-table before union)
        sample_frac: approximate fraction to sample (uses TABLESAMPLE)
    """
    parts = []
    for i in range(1, 6):
        base = f"""
        SELECT video_id, comment_id, parent_id, comment_text,
               author_name, author_channel_id, published_at,
               like_count, reply_count
        FROM {table(f'comment{i}')}
        """
        if limit:
            base += f" LIMIT {limit // 5}"
        parts.append(base)

    sql = " UNION ALL ".join(parts)

    if sample_frac and not limit:
        sql = f"SELECT * FROM ({sql}) WHERE RAND() < {sample_frac}"

    df = query_to_df(sql)
    df["published_at"] = pd.to_datetime(df["published_at"], errors="coerce", utc=True)
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
