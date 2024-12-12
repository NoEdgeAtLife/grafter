from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class FeatureComputer:
    sentiment = SentimentIntensityAnalyzer()

    def compute(self, feature_name: str, state: dict) -> float | None:
        if feature_name == "moving_average":
            return self._compute_moving_average(state)
        elif feature_name == "price_momentum":
            return self._compute_price_momentum(state)
        elif feature_name == "sentiment_momentum":
            return self._compute_sentiment_momentum(state)
        elif feature_name == "headline_sentiment":
            return self._compute_headline_sentiment(state)
        elif feature_name == "text_sentiment":
            return self._compute_text_sentiment(state)
        elif feature_name == "headline_sentiment_spread":
            return self._compute_headline_sentiment_spread(state)
        elif feature_name == "text_sentiment_spread":
            return self._compute_text_sentiment_spread(state)
        else:
            return state[feature_name]

    def _compute_moving_average(self, state) -> float | None:
        window_size = 10
        if len(state["market_prices"]) >= window_size:
            return sum(state["market_prices"][-window_size:]) / window_size
        return None

    def _compute_price_momentum(self, state) -> float | None:
        if state["moving_average"] is not None and len(state["market_prices"]) > 1:
            return (state["market_prices"][-1] - state["moving_average"]) / state["moving_average"]
        return None

    def _compute_sentiment_momentum(self, state) -> float | None:
        if len(state["sentiment_scores"]) > 1:
            return state["sentiment_scores"][-1] - state["sentiment_scores"][-2]
        return None

    def _compute_headline_sentiment(self, state) -> float | None:
        if state["headlines"] is None:
            return None
        return self.sentiment.polarity_scores(state["headlines"][-1])["compound"]

    def _compute_text_sentiment(self, state) -> float | None:
        if state["text_bodies"] is None:
            return None
        return self.sentiment.polarity_scores(state["text_bodies"][-1])["compound"]

    def _compute_headline_sentiment_spread(self, state) -> float | None:
        if state["headlines"] is None or state["sentiment_scores"] is None:
            return None
        return self._compute_headline_sentiment(state) - state["sentiment_scores"][-1]

    def _compute_text_sentiment_spread(self, state) -> float | None:
        if state["text_bodies"] is None:
            return None
        return self._compute_text_sentiment(state) - state["sentiment_scores"][-1]
