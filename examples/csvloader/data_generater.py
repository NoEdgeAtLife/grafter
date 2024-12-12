import csv
import random
from datetime import datetime, timedelta


def generate_sample_data(filename, num_entries=100):
    tickers = ["AAPL", "GOOGL", "MSFT", "AMZN", "FB"]
    headlines = [
        "Company X Announces New Product",
        "Market Volatility Increases",
        "Earnings Report Exceeds Expectations",
        "Merger Talks Underway",
        "Economic Indicators Show Growth",
    ]

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file, delimiter="|")
        writer.writerow(["Ticker", "Timestamp", "Headline", "Text Body", "Sentiment Score", "Market Price"])

        base_time = datetime.now()
        for i in range(num_entries):
            ticker = random.choice(tickers)
            timestamp = (base_time + timedelta(minutes=i)).isoformat()
            headline = random.choice(headlines)
            text_body = f"This is a detailed news article about {headline.lower()}."
            sentiment_score = round(random.uniform(-1, 1), 2)
            market_price = round(random.uniform(100, 1000), 2)

            writer.writerow([ticker, timestamp, headline, text_body, sentiment_score, market_price])


if __name__ == "__main__":
    generate_sample_data("sample_data.csv")
    print("Sample data file 'sample_data.csv' has been generated.")
