from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import logging

logger = logging.getLogger(__name__)

default_args = {
    "owner": "artem",
    "retries": 2,                          
    "retry_delay": timedelta(minutes=5),  
    "email_on_failure": False,
}

def extract_prices(**context):
    response = requests.get(
        "https://api.coingecko.com/api/v3/simple/price",
        params={"ids": "bitcoin,ethereum,solana", "vs_currencies": "usd,eur"},
        timeout=30,
    )
    response.raise_for_status()
    prices = response.json()
    logger.info(f"Prices: {prices}")

    context["ti"].xcom_push(key="prices", value=prices)
    return prices


def extract_orders(**context):
    carts = requests.get("https://fakestoreapi.com/carts", timeout=30).json()
    products = requests.get("https://fakestoreapi.com/products", timeout=30).json()
    logger.info(f"Fetched {len(carts)} carts, {len(products)} products")

    context["ti"].xcom_push(key="carts", value=carts)
    context["ti"].xcom_push(key="products", value=products)


def transform(**context):
    ti = context["ti"]

    prices   = ti.xcom_pull(task_ids="extract_prices", key="prices")
    carts    = ti.xcom_pull(task_ids="extract_orders", key="carts")
    products = ti.xcom_pull(task_ids="extract_orders", key="products")

    product_index = {p["id"]: p for p in products}

    rows = []
    for cart in carts:
        for item in cart["products"]:
            product = product_index.get(item["productId"], {})
            price_usd = product.get("price", 0)
            quantity  = item["quantity"]
            revenue   = price_usd * quantity

            rows.append({
                "cart_id":    cart["id"],
                "user_id":    cart["userId"],
                "product_id": item["productId"],
                "title":      product.get("title", "unknown"),
                "quantity":   quantity,
                "revenue_usd": round(revenue, 2),
                "revenue_btc": round(revenue / prices["bitcoin"]["usd"], 8),
            })

    logger.info(f"Transformed {len(rows)} order lines")
    ti.xcom_push(key="rows", value=rows)


def load(**context):
    ti   = context["ti"]
    rows = ti.xcom_pull(task_ids="transform", key="rows")

    logger.info(f"Loading {len(rows)} rows")
    for row in rows[:3]: 
        logger.info(row)
    logger.info("Load complete!")


with DAG(
    dag_id="crypto_etl",
    default_args=default_args,
    description="ETL pipeline: crypto prices + e-commerce orders",
    schedule="@daily",          
    start_date=datetime(2024, 1, 1),
    catchup=False,              
    tags=["crypto", "etl"],
) as dag:

    t1 = PythonOperator(
        task_id="extract_prices",
        python_callable=extract_prices,
    )

    t2 = PythonOperator(
        task_id="extract_orders",
        python_callable=extract_orders,
    )

    t3 = PythonOperator(
        task_id="transform",
        python_callable=transform,
    )

    t4 = PythonOperator(
        task_id="load",
        python_callable=load,
    )

    [t1, t2] >> t3 >> t4