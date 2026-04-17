from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class CreatePromoCodeDTO:
    code: str
    discount_type: str
    discount_value: float
    min_order_value: float
    max_usage: int
    valid_from: Optional[datetime] = None
    valid_until: Optional[datetime] = None
