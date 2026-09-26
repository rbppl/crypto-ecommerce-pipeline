import pandas as pd
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def transform(carts: list, products: list, prices: dict) -> pd.DataFrame:
    products_df = pd.DataFrame(products)[["id", "title", "price", "category"]]
    products_df = products_df.rename(columns={"id": "product_id", "price": "price_usd"})

    rows = []
    for cart in carts:
        for item in cart["products"]:
            rows.append({
                "cart_id":    cart["id"],
                "user_id":    cart["userId"],
                "date":       cart["date"][:10],
                "product_id": item["productId"],
                "quantity":   item["quantity"],
            })

    orders_df = pd.DataFrame(rows)

    df = orders_df.merge(products_df, on="product_id", how="left")


    df["revenue_usd"] = df["price_usd"] * df["quantity"]


    df["btc_price_usd"] = prices["bitcoin"]["usd"]
    df["eth_price_usd"] = prices["ethereum"]["usd"]
    df["sol_price_usd"] = prices["solana"]["usd"]

    df["revenue_btc"] = (df["revenue_usd"] / df["btc_price_usd"]).round(8)
    df["revenue_eth"] = (df["revenue_usd"] / df["eth_price_usd"]).round(6)
    df["revenue_sol"] = (df["revenue_usd"] / df["sol_price_usd"]).round(4)

    df["date"]     = pd.to_datetime(df["date"])
    df["quantity"] = df["quantity"].astype(int)

    df = df[[
        "cart_id", "user_id", "date",
        "product_id", "title", "category",
        "quantity", "price_usd", "revenue_usd",
        "btc_price_usd", "revenue_btc",
        "eth_price_usd", "revenue_eth",
        "sol_price_usd", "revenue_sol",
    ]]

    logger.info(f"Transformed {len(df)} order lines for {df['cart_id'].nunique()} carts")
    return df


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    from extract_orders import fetch_products, fetch_carts
    from extract_prices import fetch_prices

    products = fetch_products()
    carts    = fetch_carts()
    prices   = fetch_prices()

    df = transform(carts, products, prices)

    print(df.head(3).to_string())
    print(f"\nКолонки: {list(df.columns)}")
    print(f"Строк: {len(df)}")