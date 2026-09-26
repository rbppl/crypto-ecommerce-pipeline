import os
import logging
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


def get_conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", 5432),
        dbname=os.getenv("DB_NAME", "ecommerce_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "password"),
    )


def create_tables() -> None:
    with get_conn() as conn:
        with conn.cursor() as cur:
            with open("sql/create_tables.sql") as f:
                cur.execute(f.read())
        conn.commit()
    logger.info("Tables created")


def load(records: list) -> None:
    rows = [(
        r["cart_id"], r["user_id"], r["date"],
        r["product_id"], r["title"], r["category"],
        r["quantity"], r["price_usd"], r["revenue_usd"],
        r["btc_price_usd"], r["revenue_btc"],
        r["eth_price_usd"], r["revenue_eth"],
        r["sol_price_usd"], r["revenue_sol"],
    ) for r in records]

    upsert_sql = """
        INSERT INTO order_lines (
            cart_id, user_id, date, product_id, title, category,
            quantity, price_usd, revenue_usd,
            btc_price_usd, revenue_btc,
            eth_price_usd, revenue_eth,
            sol_price_usd, revenue_sol
        ) VALUES %s
        ON CONFLICT (cart_id, product_id) DO UPDATE SET
            quantity      = EXCLUDED.quantity,
            price_usd     = EXCLUDED.price_usd,
            revenue_usd   = EXCLUDED.revenue_usd,
            btc_price_usd = EXCLUDED.btc_price_usd,
            revenue_btc   = EXCLUDED.revenue_btc,
            eth_price_usd = EXCLUDED.eth_price_usd,
            revenue_eth   = EXCLUDED.revenue_eth,
            sol_price_usd = EXCLUDED.sol_price_usd,
            revenue_sol   = EXCLUDED.revenue_sol,
            loaded_at     = NOW()
    """

    with get_conn() as conn:
        with conn.cursor() as cur:
            psycopg2.extras.execute_values(cur, upsert_sql, rows)
        conn.commit()

    logger.info(f"Loaded {len(rows)} rows into order_lines")