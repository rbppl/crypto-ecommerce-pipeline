CREATE TABLE IF NOT EXISTS order_lines (
    id SERIAL PRIMARY KEY,
    cart_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    date DATE NOT NULL,
    product_id INTEGER NOT NULL,
    title VARCHAR(255),
    category VARCHAR(100),
    quantity INTEGER,
    price_usd NUMERIC(10, 2),
    revenue_usd NUMERIC(10, 2),
    btc_price_usd NUMERIC(12, 2),
    revenue_btc NUMERIC(12, 8),
    eth_price_usd NUMERIC(12, 2),
    revenue_eth NUMERIC(12, 6),
    sol_price_usd NUMERIC(12, 2),
    revenue_sol NUMERIC(12, 4),
    loaded_at TIMESTAMP DEFAULT NOW(),
    UNIQUE (cart_id, product_id)
);
CREATE INDEX IF NOT EXISTS idx_order_lines_date ON order_lines(date);
CREATE INDEX IF NOT EXISTS idx_order_lines_category ON order_lines(category);
CREATE INDEX IF NOT EXISTS idx_order_lines_user_id ON order_lines(user_id);