from datetime import datetime
from typing import Any

from grafter.data_loader import DataLoader


class StateManager:
    def __init__(self, data_source: DataLoader):
        self.states = {}
        self.data_source = data_source

    async def update_state(
        self, ticker: str, timestamp: str, headline: str, text_body: str, sentiment_score: float, market_price: float
    ) -> dict:
        if ticker not in self.states:
            self.states[ticker] = {
                "last_update": None,
                "market_prices": [],
                "sentiment_scores": [],
                "headlines": [],
                "text_bodies": [],
            }

        state = self.states[ticker]
        current_time = datetime.fromisoformat(timestamp)

        # Update basic state
        state["last_update"] = current_time
        state["market_prices"].append(market_price)
        state["sentiment_scores"].append(sentiment_score)
        state["headlines"].append(headline)
        state["text_bodies"].append(text_body)

        # Limit the history to last 100 entries
        max_history = 100
        state["market_prices"] = state["market_prices"][-max_history:]
        state["sentiment_scores"] = state["sentiment_scores"][-max_history:]
        state["headlines"] = state["headlines"][-max_history:]
        state["text_bodies"] = state["text_bodies"][-max_history:]

        # Check for new news
        if len(state["headlines"]) > 1:
            state["has_new_news"] = state["headlines"][-1] != state["headlines"][-2]
        else:
            state["has_new_news"] = headline is not None

        return state

    def get_state(self, ticker) -> dict[str, dict[str, Any]]:
        return self.states[ticker]
