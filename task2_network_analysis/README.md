# Task 2: Network Analysis

## Objective
Build a channel-level network graph to identify coordinated groups of YouTube channels covering the Russia-Ukraine conflict.

## Methodology
- **Edge construction**: Tag overlap (Jaccard similarity > 0.15) and temporal co-posting patterns (same-day posting >= 5 days)
- **Network metrics**: PageRank, betweenness centrality, degree distribution
- **Community detection**: Louvain clustering with modularity scoring
- **Hypothesis testing (H1)**: Mann-Whitney U test comparing engagement of coordinated clusters vs isolated channels

## Outputs
- `outputs/channel_clusters.csv` — Channel-to-cluster mapping with centrality metrics
- `outputs/channel_centrality_metrics.csv` — Full centrality scores

## Key Visualizations
- Interactive network graph (nodes colored by cluster, sized by PageRank)
- Centrality bar charts
- Inter-cluster connectivity heatmap

## How to Run
```bash
jupyter notebook network_analysis.ipynb
```
