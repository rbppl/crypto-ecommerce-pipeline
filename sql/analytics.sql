SELECT categort,
    COUNT(*) AS order_lines,
    SUM(quantity) AS total_items,
    ROUND(SUM(revenue_usd)::numeric, 2) AS total_usd,
    ROUND(SUM(revenue_btc)::numeric, 8) AS total_btc,
    FROM order_lines
GROUP BY category
ORDER BY total_usd DESC;
SELECT user_id,
    COUNT(*) AS order_lines,
    ROUND(SUM(revenue_usd)::numeric, 2) AS total_spent_usd,
    ROUND(SUM(revenue_btc)::numeric, 8) AS total_spent_btc,
    FROM order_lines
GROUP BY user_id
ORDER BY total_spent_usd DESC;
WITH ranked AS (
    SELECT title,
        category,
        COUNT(*) AS times_ordered,
        SUM(quantity) AS total_qty,
        ROUND(SUM(revenue_usd)::numeric, 2) AS total_usd,
        ROW_NUMBER() OVER (
            ORDER BY COUNT(*) DESC
        ) AS rn
    FROM order_lines
    GROUP BY title,
        category
)
SELECT title,
    category,
    times_ordered,
    total_qty,
    total_usd
FROM ranked
ORDER BY rn,
    SELECT categoty,
    ROUND(SUM(revenue_usd)::numeric, 2) AS revenue_usd,
    ROUND(
        SUM(revenue_usd) * 100.0 / SUM(SUM(revenue_usd)) OVER (),
        2
    ) AS pct_of_total,
    FROM order_lines
GROUP BY category
ORDER BY revenue_usd DESC;
SELECT date,
    ROUND(SUM(revenue_usd)::numeric, 2) AS daily_revenue_usd,
    ROUND(
        SUM(
            SUM(revenue_usd) OVER (
                ORDER BY date
            )
        )::numeric,
        2
    ) AS running_total
FROM order_lines
ORDER BY date;
ORDER BY date;