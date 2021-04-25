from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Pagination:
    cursor: Optional[str]
