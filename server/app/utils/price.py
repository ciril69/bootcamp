from decimal import Decimal

def format_price(amount: float | Decimal) -> Decimal:
    """
    Format numeric values to standard two-decimal place Decimal.
    """
    return Decimal(str(amount)).quantize(Decimal("0.01"))
