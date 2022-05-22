from dataclasses import dataclass
from datetime import datetime, date


@dataclass
class Result:
    store: str
    month: str
    record_count: int
    currency: str
    category: str
    amount: float
    min_date: date = datetime.today().date()
    max_date: date = datetime.today().date()

    def __post_init__(self):
        if self.category is None:
            self.category = ''
        # if self.min_date is None:
        #     self.min_date = ''

    def get_min(self):
        return '' if self.min_date is None else self.min_date
