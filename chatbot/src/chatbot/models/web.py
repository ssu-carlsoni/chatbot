from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class WebDocument:
    url: str = ""
    title: str = ""
    raw_content: str = ""
    llm_content: str = ""
    vector_content: str = ""
    metadata: Dict[str, str] = field(default_factory=dict)
    embedding: Optional[List[float]] = None