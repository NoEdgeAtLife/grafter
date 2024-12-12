from math import isclose

import pytest
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from grafter.feature_computer import FeatureComputer


@pytest.fixture
def feature_computer():
    return FeatureComputer()


def test_compute_moving_average(feature_computer):
    state = {"market_prices": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}
    assert isclose(feature_computer.compute("moving_average", state), 5.5, rel_tol=1e-9)


def test_compute_price_momentum(feature_computer):
    state = {"market_prices": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "moving_average": 5.5}
    assert isclose(feature_computer.compute("price_momentum", state), (10 - 5.5) / 5.5, rel_tol=1e-9)


def test_compute_sentiment_momentum(feature_computer):
    state = {"sentiment_scores": [0.1, 0.2, 0.3]}
    assert isclose(feature_computer.compute("sentiment_momentum", state), 0.1, rel_tol=1e-9)


def test_compute_headline_sentiment(feature_computer):
    state = {"headlines": ["This is a good product"]}
    sentiment = SentimentIntensityAnalyzer().polarity_scores(state["headlines"])["compound"]
    assert feature_computer.compute("headline_sentiment", state) == sentiment


def test_compute_text_sentiment(feature_computer):
    state = {"text_bodies": ["This is a bad product"]}
    sentiment = SentimentIntensityAnalyzer().polarity_scores(state["text_bodies"])["compound"]
    assert feature_computer.compute("text_sentiment", state) == sentiment


def test_compute_headline_sentiment_spread(feature_computer):
    state = {"headlines": ["This is a good product"], "sentiment_scores": [0.5]}
    headline_sentiment = SentimentIntensityAnalyzer().polarity_scores(state["headlines"])["compound"]
    assert isclose(
        feature_computer.compute("headline_sentiment_spread", state),
        headline_sentiment - state["sentiment_scores"][-1],
        rel_tol=1e-9,
    )


def test_compute_text_sentiment_spread(feature_computer):
    state = {"text_bodies": ["This is a bad product"], "sentiment_scores": [0.5]}
    text_sentiment = SentimentIntensityAnalyzer().polarity_scores(state["text_bodies"])["compound"]
    assert isclose(
        feature_computer.compute("text_sentiment_spread", state),
        text_sentiment - state["sentiment_scores"][-1],
        rel_tol=1e-9,
    )
