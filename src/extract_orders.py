import requests
import logging
logger = logging.getLogger(__name__)

def fetch_products() -> list:
    response = requests.get(
        "https://fakestoreapi.com/products",
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    logger.info(f"Fetched {len(data)} products")
    return data


def fetch_carts() -> list:
    response = requests.get(
        "https://fakestoreapi.com/carts",
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    logger.info(f"Fetched {len(data)} carts")
    return data

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    products = fetch_products()
    print(products[0])
    carts = fetch_carts()
    print(carts[0])