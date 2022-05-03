from dataclasses import dataclass, field


@dataclass
class Result:
    store: str
    month: str
    records: int
    currency: str
    category: str
    amount: float

    def __post_init__(self):
        if self.category is None:
            self.category = ''
