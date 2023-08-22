from dataclasses import dataclass
from typing import List



@dataclass()
class Exercise():
    name: str
    weight: List[str]
    day_the_week: List[str]


