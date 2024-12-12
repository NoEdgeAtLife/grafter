import json
import os
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

import lmdb


class FeatureStore(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def save_features(self, timestamp: int, ticker: str, features: dict[str, Any]):
        pass

    @abstractmethod
    def load_latest_features(self, ticker: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def serialize_features(self, features: dict[str, Any]) -> bytes:
        pass

    @abstractmethod
    def deserialize_features(self, value: bytes) -> dict[str, Any]:
        pass


class LMDBFeatureStore(FeatureStore):
    def __init__(self, config: dict[str, Any]):
        os.makedirs(config["path"], exist_ok=True)
        self.env = lmdb.open(config["path"], map_size=1099511627776)

    def save_features(self, timestamp: int, ticker: str, features: dict[str, Any]):
        with self.env.begin(write=True) as txn:
            key = f"{timestamp}:{ticker}".encode()
            value = self.serialize_features(features)
            txn.put(key, value)

    def serialize_features(self, features: dict[str, Any]) -> bytes:
        def default_converter(o):
            if isinstance(o, datetime):
                return o.__str__()

        return json.dumps(features, default=default_converter).encode()

    def load_latest_features(self, ticker: str) -> dict[str, Any]:
        with self.env.begin(write=False) as txn:
            cursor = txn.cursor()
            prefix = f":{ticker}".encode()
            latest_key = None
            for key, _ in cursor:
                if key.endswith(prefix):
                    latest_key = key
            if latest_key is None:
                return {}
            value = txn.get(latest_key)
        return self.deserialize_features(value)

    def deserialize_features(self, value: bytes) -> dict[str, Any]:
        return json.loads(value.decode())

    def get_tickers(self) -> list[str]:
        tickers = set()
        with self.env.begin(write=False) as txn:
            cursor = txn.cursor()
            for key, _ in cursor:
                ticker = key.decode().split(":")[1]
                tickers.add(ticker)
        return list(tickers)


class InMemoryFeatureStore(FeatureStore):
    def __init__(self):
        self.store = {}

    def save_features(self, timestamp: int, ticker: str, features: dict[str, Any]):
        key = f"{timestamp}:{ticker}"
        self.store[key] = self.serialize_features(features)

    def serialize_features(self, features: dict[str, Any]) -> bytes:
        def default_converter(o):
            if isinstance(o, datetime):
                return o.__str__()

        return json.dumps(features, default=default_converter).encode()

    def load_latest_features(self, ticker: str) -> dict[str, Any]:
        prefix = f":{ticker}"
        latest_key = None
        for key in self.store:
            if key.endswith(prefix):
                latest_key = key
        if latest_key is None:
            return {}
        value = self.store[latest_key]
        return self.deserialize_features(value)

    def deserialize_features(self, value: bytes) -> dict[str, Any]:
        return json.loads(value.decode())

    def get_tickers(self) -> list[str]:
        tickers = set()
        for key in self.store:
            ticker = key.split(":")[1]
            tickers.add(ticker)
        return list(tickers)
