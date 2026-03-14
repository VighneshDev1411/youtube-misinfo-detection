"""Live Comment Classifier — Enter text and get predictions."""

import streamlit as st

st.header("Live Comment Classifier")
st.markdown("Enter a YouTube comment to classify it for sentiment and misinformation.")


@st.cache_resource
def load_sentiment_model():
    from transformers import pipeline
    return pipeline("sentiment-analysis",
                    model="cardiffnlp/twitter-xlm-roberta-base-sentiment-multilingual",
                    top_k=None)


@st.cache_resource
def load_misinfo_model():
    from transformers import pipeline
    return pipeline("zero-shot-classification",
                    model="facebook/bart-large-mnli")


comment = st.text_area("Enter a comment:", height=120,
                       placeholder="e.g., 'The government is hiding the truth about what happened'")

if st.button("Classify", type="primary") and comment.strip():
    with st.spinner("Loading models..."):
        try:
            sentiment_pipe = load_sentiment_model()
            misinfo_pipe = load_misinfo_model()
        except Exception as e:
            st.error(f"Error loading models: {e}")
            st.info("Install dependencies: `pip install transformers torch`")
            st.stop()

    with st.spinner("Classifying..."):
        # Sentiment
        sent_result = sentiment_pipe(comment[:512])[0]
        sent_scores = {r["label"]: r["score"] for r in sent_result}

        # Misinformation
        misinfo_result = misinfo_pipe(
            comment[:512],
            candidate_labels=["misinformation", "propaganda", "factual reporting", "opinion"],
        )

    # ── Display results ──────────────────────────────────────────────────
    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Sentiment")
        for label, score in sorted(sent_scores.items(), key=lambda x: -x[1]):
            color = {"positive": "green", "negative": "red", "neutral": "gray"}.get(label, "blue")
            st.markdown(f":{color}[**{label.title()}**]: {score:.1%}")
        top_sent = max(sent_scores, key=sent_scores.get)
        st.success(f"Predicted: **{top_sent.title()}** ({sent_scores[top_sent]:.1%})")

    with col2:
        st.subheader("Misinformation Check")
        for label, score in zip(misinfo_result["labels"], misinfo_result["scores"]):
            st.progress(score, text=f"{label}: {score:.1%}")
        st.success(f"Predicted: **{misinfo_result['labels'][0]}** ({misinfo_result['scores'][0]:.1%})")

elif not comment.strip() and st.session_state.get("classify_clicked"):
    st.warning("Please enter a comment to classify.")

st.markdown("---")
st.caption("Models: `twitter-xlm-roberta-base-sentiment-multilingual` (sentiment), "
           "`bart-large-mnli` (zero-shot classification)")
