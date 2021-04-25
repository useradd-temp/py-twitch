from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Pagination:
    cursor: Optional[str]


@dataclass
class BitsCheermotesModel:
    @dataclass
    class data:
        @dataclass
        class tier:
            min_bits: int
            id: str
            color: str
            images: dict
            can_cheer: bool
            show_in_bits_card: bool
        
        prefix: str
        tiers: List[dict]
        tiers: List[tier]
        type: str
        order: int
        last_updated: str
        is_charitable: bool
    
    data: List[data]
