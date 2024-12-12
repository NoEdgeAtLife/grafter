from datetime import datetime

import pytest

from grafter.data_loader import DataLoader
from grafter.state_manager import StateManager


@pytest.fixture
def data_loader():
    return DataLoader()


@pytest.fixture
def state_manager(data_loader):
    return StateManager(data_loader)


@pytest.mark.asyncio
async def test_update_state(state_manager):
    ticker = "AAPL"
    timestamp = "2023-01-01T12:00:00"
    headline = "Apple releases new product"
    text_body = "Apple has released a new product today."
    sentiment_score = 0.8
    market_price = 150.0

    state = await state_manager.update_state(ticker, timestamp, headline, text_body, sentiment_score, market_price)

    assert state["last_update"] == datetime.fromisoformat(timestamp)
    assert state["market_prices"] == [market_price]
    assert state["sentiment_scores"] == [sentiment_score]
    assert state["headlines"] == [headline]
    assert state["text_bodies"] == [text_body]
    assert state["has_new_news"]


@pytest.mark.asyncio
async def test_update_state_multiple_entries(state_manager):
    ticker = "AAPL"
    timestamp1 = "2023-01-01T12:00:00"
    headline1 = "Apple releases new product"
    text_body1 = "Apple has released a new product today."
    sentiment_score1 = 0.8
    market_price1 = 150.0

    timestamp2 = "2023-01-02T12:00:00"
    headline2 = "Apple stock rises"
    text_body2 = "Apple stock has risen after the product release."
    sentiment_score2 = 0.9
    market_price2 = 155.0

    await state_manager.update_state(ticker, timestamp1, headline1, text_body1, sentiment_score1, market_price1)
    state = await state_manager.update_state(ticker, timestamp2, headline2, text_body2, sentiment_score2, market_price2)

    assert state["last_update"] == datetime.fromisoformat(timestamp2)
    assert state["market_prices"] == [market_price1, market_price2]
    assert state["sentiment_scores"] == [sentiment_score1, sentiment_score2]
    assert state["headlines"] == [headline1, headline2]
    assert state["text_bodies"] == [text_body1, text_body2]
    assert state["has_new_news"]


@pytest.mark.asyncio
async def test_get_state(state_manager):
    ticker = "AAPL"
    timestamp = "2023-01-01T12:00:00"
    headline = "Apple releases new product"
    text_body = "Apple has released a new product today."
    sentiment_score = 0.8
    market_price = 150.0

    await state_manager.update_state(ticker, timestamp, headline, text_body, sentiment_score, market_price)
    state = state_manager.get_state(ticker)

    assert state["last_update"] == datetime.fromisoformat(timestamp)
    assert state["market_prices"] == [market_price]
    assert state["sentiment_scores"] == [sentiment_score]
    assert state["headlines"] == [headline]
    assert state["text_bodies"] == [text_body]
    assert state["has_new_news"]
