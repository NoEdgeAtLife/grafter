from typing import Any

import dask.dataframe as dd


class DataLoader:
    def __init__(self):
        # Initialize data source connections
        pass

    def get_next_data(self) -> dict[str, Any]:
        # Fetch and return next data point
        raise NotImplementedError("get_next_data is not implemented for this class")


class CsvLoader(DataLoader):
    def __init__(self, file_path: str):
        self.file_path = file_path

    async def load_data(self):
        self.df = dd.read_csv(self.file_path, delimiter="|")

    async def get_next_data(self) -> dict[str, Any] | None:
        if not hasattr(self, "df"):
            await self.load_data()

        if not hasattr(self, "df_iter"):
            self.df_iter = self.df.iterrows()

        try:
            _, row = next(self.df_iter)
            return {
                "ticker": row["Ticker"],
                "timestamp": row["Timestamp"],
                "headline": row["Headline"],
                "text_body": row["Text Body"],
                "sentiment_score": float(row["Sentiment Score"]),
                "market_price": float(row["Market Price"]),
            }
        except StopIteration:
            return None

    def __del__(self):
        if hasattr(self, "df"):
            del self.df
