import asyncio
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from grafter.config import AppConfig
from grafter.data_loader import CsvLoader
from grafter.graph_manager import GraphManager, StateManager

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "./config.yaml")
DATA_FILE = os.path.join(os.path.dirname(__file__), "./sample_data.csv")


async def run_app():
    app_config = AppConfig.from_yaml(CONFIG_FILE)

    csv_loader = CsvLoader(DATA_FILE)
    await csv_loader.load_data()

    state_manager = StateManager(csv_loader)
    graph_manager = GraphManager(
        app_config.feature_config, app_config.event_trigger_config, state_manager, app_config.feature_store_config
    )

    while True:
        data = await csv_loader.get_next_data()
        if data is None:
            break
        await graph_manager.on_update(data)
        await asyncio.sleep(0.1)

    # Print the features from feature store after all data is processed
    print("Feature Store:")
    for ticker in graph_manager.feature_store.get_tickers():
        print(f"{ticker}: {graph_manager.feature_store.load_latest_features(ticker)}")


if __name__ == "__main__":
    asyncio.run(run_app())
