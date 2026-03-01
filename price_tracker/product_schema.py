from dataclasses import dataclass
from typing import List

@dataclass
class product:
    pid: int
    name: str
    visual_price:str
    price:float
    url:str
@dataclass
class Log:
    id: int
    name: str
    last_price:float
    new_price:float
    url:str
    log_msg:str

