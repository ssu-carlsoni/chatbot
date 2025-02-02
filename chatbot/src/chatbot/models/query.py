from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Query:
    text: str
    embedding: Optional[List[float]] = None