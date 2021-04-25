from .base import *


@dataclass
class ChannelsCommercialModel:
    length: int
    message: str
    retry_after: int
