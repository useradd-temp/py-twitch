from .base import *


@dataclass
class GameData:
    id: str
    name: str
    box_art_url: str = ""


@dataclass
class GamesModel:
    data: List[GameData]
