from dataclasses import dataclass
from typing import List

@dataclass
class Variant:
    id: int
    title: str
    variants_beat: List["Variant"]

