from pydantic import BaseModel, Field, ValidationError, field_validator
from datetime import date
import logging

logger = logging.getLogger(__name__)


class OrderLine(BaseModel):
    cart_id:       int
    user_id:       int
    date:          date
    product_id:    int
    title:         str
    category:      str
    quantity:      int   = Field(gt=0)
    price_usd:     float = Field(gt=0)
    revenue_usd:   float = Field(ge=0)
    btc_price_usd: float = Field(gt=0)
    revenue_btc:   float = Field(ge=0)
    eth_price_usd: float = Field(gt=0)
    revenue_eth:   float = Field(ge=0)
    sol_price_usd: float = Field(gt=0)
    revenue_sol:   float = Field(ge=0)

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v):
        if not v.strip():
            raise ValueError("title cannot be empty")
        return v.strip()


def validate(df) -> tuple:
    valid  = []
    errors = []

    for row in df.to_dict("records"):
        try:
            OrderLine(**row)
            valid.append(row)
        except ValidationError as e:
            logger.warning(f"Invalid row cart_id={row.get('cart_id')}: {e}")
            errors.append(row)

    logger.info(f"Valid: {len(valid)}, Errors: {len(errors)}")
    return valid, errors


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    from extract_orders import fetch_products, fetch_carts
    from extract_prices import fetch_prices
    from transform import transform

    carts    = fetch_carts()
    products = fetch_products()
    prices   = fetch_prices()
    df       = transform(carts, products, prices)

    valid, errors = validate(df)
    print(f"Valid:  {len(valid)}")
    print(f"Errors: {len(errors)}")