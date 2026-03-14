# Coordinated Amplification and Misinformation Detection in Global YouTube Conflict Narratives

[![Course](https://img.shields.io/badge/Course-CS%20418-blue)](https://github.com/VighneshDev1411/youtube-misinfo-detection)
## Overview

End-to-end data science pipeline that detects coordinated misinformation campaigns across 1,500+ YouTube channels and 1M+ comments covering the Russia-Ukraine conflict. Combines network science, anomaly detection, and modern NLP to analyze the full lifecycle of misinformation narratives.

**Author:** Vignesh Pathak — [@VighneshDev1411](https://github.com/VighneshDev1411)
**Origin:** CS 418, University of Illinois Chicago

## Research Hypotheses

| # | Hypothesis | Task | Method |
|---|-----------|------|--------|
| H1 | Coordinated channel clusters amplify misinformation | Task 2 | Mann-Whitney U test on cluster engagement |
| H2 | Conflict events correlate with engagement anomalies | Task 3 | Z-score + Isolation Forest with event windows |
| H3 | Narratives evolve in alignment with war events | Task 5 | BERTopic topics_over_time + sentiment trends |

## Dataset

| Data | Size | Source |
|------|------|--------|
| Channels | 1,561 | YouTube Data API v3 |
| Videos | 440,772 | YouTube Data API v3 |
| Comments | 1.06M+ | YouTube Data API v3 |
| Storage | BigQuery | `infinite-rope-363317.youtube_data` |

## Project Structure

```
.
├── utils/                              # Shared utilities
│   ├── bq_helpers.py                   # BigQuery client & Plotly theme
│   └── conflict_timeline.py            # 20 key conflict events
├── task1_data_collection_and_cleanup/  # Data pipeline (YouTube API → BigQuery)
│   ├── channels/                       # Channel data collection & upload
│   ├── videos/                         # Video data collection & upload
│   ├── comments/                       # Comment data collection & upload
│   └── eda/                            # Exploratory data analysis
├── task2_network_analysis/             # Channel network graph
│   ├── network_analysis.ipynb          # Tag overlap, co-posting, Louvain clustering
│   └── outputs/                        # channel_clusters.csv, centrality_metrics.csv
├── task3_engagement_analysis_.../      # Anomaly detection
│   ├── engagement_analysis.ipynb       # Z-score, Isolation Forest, event correlation
│   └── outputs/                        # video_anomaly_scores.csv, timeseries.csv
├── task4_commenter_level_.../          # Commenter analysis
│   ├── commenter_analysis.ipynb        # Server-side BQ joins, bot detection
│   └── outputs/                        # commenter_bot_scores.csv, clusters.csv
├── task5_nlp_and_narrative_.../        # NLP analysis
│   ├── nlp_analysis.ipynb              # Sentiment, BERTopic, misinfo classification
│   └── outputs/                        # classifications.csv, topics_over_time.csv
├── dashboard/                          # Streamlit dashboard
│   ├── app.py                          # Main entry point
│   └── pages/                          # Overview, Network, Engagement, etc.
├── requirements.txt
└── project_highlights.md               # LinkedIn/resume bullet points
```

## Quick Start

### Installation
```bash
pip install -r requirements.txt
```

### Run Notebooks
Each task's notebook queries BigQuery directly. Requires `gcloud auth application-default login`.

```bash
cd task3_engagement_analysis_and_anomaly_detection
jupyter notebook engagement_analysis.ipynb
```

### Launch Dashboard
```bash
streamlit run dashboard/app.py
```

The dashboard reads pre-computed CSVs from notebook outputs. Run the notebooks first to generate data.

## Tech Stack

Python, BigQuery, Pandas, NetworkX, Plotly, Scikit-learn, HuggingFace Transformers, BERTopic, Streamlit

## License

Academic project — CS 418, University of Illinois Chicago.
