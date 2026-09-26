import logging
import sys 
import os 

sys.path.insert(0, "src")
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/pipeline.log"),])
logger = logging.getLogger(__name__)

from extract_orders import fetch_products, fetch_carts
from extract_prices import fetch_prices
from transform import transform 
from validate import validate
from load import create_tables, load

def run() -> None:
    logger.info("=== Pipeline started ===")

    # Extract
    carts = fetch_carts()
    products = fetch_products()
    prices = fetch_prices()
    

    # Transform
    df = transform(carts, products, prices)

    # Validate
    valid, errors = validate(df)
    if errors:
        logger.warning(f"{len(errors)} records failed validation")
    # Load
    create_tables()
    load(valid)

    logger.info("=== Pipeline finished ===")

if __name__ == "__main__":
    run()