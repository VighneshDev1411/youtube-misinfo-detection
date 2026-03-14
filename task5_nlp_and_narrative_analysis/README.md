# Task 5: NLP & Narrative Analysis

## Objective
Analyze comment narratives, sentiment trends, and misinformation patterns across the Russia-Ukraine conflict timeline.

## Methodology
- **Language detection**: `langdetect` to classify EN/RU/UK/OTHER
- **Sentiment analysis**: `cardiffnlp/twitter-xlm-roberta-base-sentiment-multilingual` for multilingual sentiment
- **Topic modeling**: BERTopic with `paraphrase-multilingual-MiniLM-L12-v2` embeddings, tracking topic evolution over time
- **Misinformation classification**: Zero-shot classification with `facebook/bart-large-mnli` (labels: misinformation, propaganda, factual reporting, opinion)
- **Hypothesis testing (H3)**: Do narrative topics shift predictably around conflict events?

## Outputs
- `outputs/comment_classifications.csv` — Per-comment sentiment, topic, and misinformation labels
- `outputs/topics_over_time.csv` — BERTopic temporal evolution data
- `outputs/sentiment_timeseries.csv` — Weekly sentiment aggregates

## Key Visualizations
- Sentiment trends with conflict event overlays
- Topic evolution timeline
- Misinformation proportion over time
- Cross-task integration (sentiment by channel cluster, anomalous video sentiment)

## How to Run
```bash
jupyter notebook nlp_analysis.ipynb
```
