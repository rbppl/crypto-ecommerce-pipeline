import requests
import logging

logger = logging.getLogger(__name__)

COINS = ["bitcoin", "ethereum", "solana"]

def fetch_prices() -> dict:
    response = requests.get(
        "https://api.coingecko.com/api/v3/simple/price",
        params={
            "ids": ",".join(COINS),
            "vs_currencies": "usd,eur",
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    logger.info(f"Fetched prices for {list(data.keys())}")
    return data


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    prices = fetch_prices()
    print(prices)