from dataclasses import dataclass, field
from datetime import MINYEAR, MAXYEAR, datetime


@dataclass
class Result:
    store: str
    month: str
    record_count: int
    currency: str
    category: str
    amount: float
    min_date: datetime = MINYEAR
    max_date: datetime = MAXYEAR

    def __post_init__(self):
        if self.category is None:
            self.category = ''
        # if self.min_date is None:
        #     self.min_date = ''

    def get_min(self):
        return '' if self.min_date is None else self.min_date
