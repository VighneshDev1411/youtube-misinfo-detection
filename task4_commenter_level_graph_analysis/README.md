# Task 4: Commenter-Level Graph Analysis

## Objective
Analyze commenter behavior patterns, detect bot-like accounts, and build a commenter co-occurrence network.

## Methodology
- **Server-side BigQuery joins**: Co-occurrence edge list computed in SQL (not Python) — pushes computation to the warehouse instead of pulling 1M+ rows locally
- **Network construction**: Weighted graph from commenter co-occurrence (shared videos >= 3)
- **Bot detection**: Composite scoring based on posting volume, burst activity, cross-channel presence, and network centrality
- **Community detection**: Louvain clustering on top-5000 commenters by degree
- **Cross-task integration**: Map commenter clusters to channel clusters from Task 2

## Outputs
- `outputs/commenter_bot_scores.csv` — Bot scores and flags per commenter
- `outputs/commenter_clusters.csv` — Community assignments and centrality metrics

## Key Visualizations
- Bot score distribution histogram
- Commenter activity scatter plots
- Community size distribution

## How to Run
```bash
jupyter notebook commenter_analysis.ipynb
```
