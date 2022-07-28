from dataclasses import dataclass

@dataclass
class Cell:
    cell_id: int
    character: str
    user_id: int
    round_id: int
