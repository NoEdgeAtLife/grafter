from tempfile import NamedTemporaryFile

import pytest

from grafter.data_loader import CsvLoader


@pytest.fixture
def sample_csv_file():
    temp_file = NamedTemporaryFile(mode="w+", delete=False)
    temp_file.write("Ticker|Timestamp|Headline|Text Body|Sentiment Score|Market Price\n")
    temp_file.write("AAPL|2023-04-01T12:00:00|Test Headline|Test Body|0.5|150.75\n")
    temp_file.write("GOOGL|2023-04-01T12:01:00|Another Headline|Another Body|-0.2|2500.50\n")
    temp_file.close()
    yield temp_file.name
    import os

    os.unlink(temp_file.name)


@pytest.fixture
def csv_loader(sample_csv_file):
    loader = CsvLoader(sample_csv_file)
    return loader


@pytest.mark.asyncio
async def test_get_next_data(csv_loader):
    await csv_loader.load_data()
    data = await csv_loader.get_next_data()
    assert data["ticker"] == "AAPL"
    assert data["timestamp"] == "2023-04-01T12:00:00"
    assert data["headline"] == "Test Headline"
    assert data["text_body"] == "Test Body"
    assert data["sentiment_score"] == 0.5
    assert data["market_price"] == 150.75

    data = await csv_loader.get_next_data()
    assert data["ticker"] == "GOOGL"

    assert await csv_loader.get_next_data() is None
