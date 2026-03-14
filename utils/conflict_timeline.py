"""Key Russia-Ukraine conflict events for chart annotations."""

import pandas as pd

EVENTS = [
    ("2022-02-24", "Russia invades Ukraine"),
    ("2022-03-02", "UN General Assembly condemns invasion"),
    ("2022-03-16", "Mariupol theatre airstrike"),
    ("2022-04-02", "Bucha massacre revealed"),
    ("2022-04-14", "Moskva cruiser sunk"),
    ("2022-05-20", "Mariupol falls to Russia"),
    ("2022-06-25", "Russia captures Severodonetsk"),
    ("2022-08-29", "Kherson counter-offensive begins"),
    ("2022-09-21", "Russia announces partial mobilization"),
    ("2022-09-30", "Russia annexes four regions"),
    ("2022-10-08", "Kerch Bridge explosion"),
    ("2022-11-11", "Ukraine recaptures Kherson"),
    ("2022-12-21", "Zelensky visits Washington"),
    ("2023-01-25", "Western tanks pledged to Ukraine"),
    ("2023-05-20", "Wagner captures Bakhmut"),
    ("2023-06-06", "Kakhovka Dam destruction"),
    ("2023-06-24", "Wagner mutiny / Prigozhin march"),
    ("2023-10-07", "Hamas attacks Israel (attention shift)"),
    ("2024-02-17", "Avdiivka falls to Russia"),
    ("2024-06-15", "Swiss peace summit"),
]

EVENTS_DF = pd.DataFrame(EVENTS, columns=["date", "event"])
EVENTS_DF["date"] = pd.to_datetime(EVENTS_DF["date"], utc=True)


def add_event_annotations(fig, y_position="top", events_df=None):
    """Add vertical lines and labels for conflict events to a Plotly figure.

    Args:
        fig: plotly.graph_objects.Figure
        y_position: 'top' or 'bottom' for label placement
        events_df: override default events DataFrame
    """
    df = events_df if events_df is not None else EVENTS_DF
    y_ref = 1.02 if y_position == "top" else -0.08

    for _, row in df.iterrows():
        fig.add_vline(
            x=row["date"], line_dash="dot", line_color="rgba(150,150,150,0.5)", line_width=1
        )
        fig.add_annotation(
            x=row["date"], y=y_ref, yref="paper",
            text=row["event"], showarrow=False,
            textangle=-45, font=dict(size=8, color="gray"),
            xanchor="left", yanchor="bottom",
        )
    return fig


def get_event_windows(window_before: int = 7, window_after: int = 14) -> pd.DataFrame:
    """Return DataFrame with start/end windows around each event."""
    df = EVENTS_DF.copy()
    df["window_start"] = df["date"] - pd.Timedelta(days=window_before)
    df["window_end"] = df["date"] + pd.Timedelta(days=window_after)
    return df
