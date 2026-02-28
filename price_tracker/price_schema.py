from dataclasses import dataclass
from typing import List

@dataclass
class product:
    id: int
    name: str
    visual_price:str
    price:float
    url:str

class Log:
    id: int
    name: str
    last_min_price:int
    url:str
    log_msg:str
