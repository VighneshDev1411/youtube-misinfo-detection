# Task 3: Engagement Analysis & Anomaly Detection

## Objective
Detect engagement anomalies in YouTube video data and correlate them with key Russia-Ukraine conflict events.

## Methodology
- **Feature engineering**: Per-video engagement ratios (like/view, comment/view), daily/weekly aggregates
- **Z-Score anomaly detection**: Rolling 30-day statistics, flagging spikes > 2.5 standard deviations
- **Isolation Forest**: Unsupervised anomaly detection on multi-dimensional feature matrix
- **Channel-level scoring**: Aggregate anomaly signals per channel for suspiciousness ranking
- **Event correlation (H2)**: Statistical tests comparing engagement in [-7, +14] day windows around conflict events

## Outputs
- `outputs/video_anomaly_scores.csv` — Per-video anomaly scores and labels
- `outputs/engagement_timeseries.csv` — Daily engagement metrics with anomaly flags

## Key Visualizations
- Engagement timeline with conflict event annotations
- Anomaly scatter plots (view count vs like count)
- Event impact bar chart

## How to Run
```bash
jupyter notebook engagement_analysis.ipynb
```
