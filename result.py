from dataclasses import dataclass, field
from typing import Dict


@dataclass
class Result:
    store: str
    month: str
    records: int
    # amount: Dict[str, float] = field(default_factory=lambda: ({"USD": 0.00}))
    currency: str
    amount: float
