# Crypto E-Commerce ETL Pipeline

ETL pipeline that extracts e-commerce orders and real-time crypto prices,
transforms the data, validates it, and loads it into PostgreSQL.

## Stack
- Python 3.10 (requests, pandas, pydantic, psycopg2)
- PostgreSQL 15 (Docker)

## Pipeline
Extract → Transform → Validate → Load

1. **Extract** — fetches orders from Fake Store API + BTC/ETH/SOL prices from CoinGecko
2. **Transform** — joins orders with products, calculates revenue in USD and crypto
3. **Validate** — checks data quality with Pydantic schemas
4. **Load** — upserts records into PostgreSQL

## How to run

1. Clone the repo
2. Create virtual environment: `python -m venv venv`
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and fill in DB credentials
5. Start Postgres: `docker run -d --name postgres -e POSTGRES_PASSWORD=password -e POSTGRES_DB=ecommerce_db -p 5432:5432 postgres:15`
6. Run: `python pipeline.py`

## Analytics

See `sql/analytics.sql` for queries:
- Revenue by product category
- Top users by spending
- Most popular products
- Category revenue share (%)
- Running total by date