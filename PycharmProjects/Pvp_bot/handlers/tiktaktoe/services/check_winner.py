from typing import List
from handlers.tiktaktoe.models.cell import Cell


def check_winner(cells: List[Cell]):
    if cells[0].user_id == cells[4].user_id == cells[8].user_id != None:
        return (True, cells[0].user_id)
    if cells[2].user_id == cells[4].user_id == cells[6].user_id != None:
        return (True, cells[2].user_id)
    if cells[0].user_id == cells[1].user_id == cells[2].user_id != None:
        return (True, cells[0].user_id)
    if cells[3].user_id == cells[4].user_id == cells[5].user_id != None:
        return (True, cells[3].user_id)
    if cells[6].user_id == cells[7].user_id == cells[8].user_id != None:
        return (True, cells[6].user_id)
    if cells[0].user_id == cells[3].user_id == cells[6].user_id != None:
        return (True, cells[0].user_id)
    if cells[1].user_id == cells[4].user_id == cells[7].user_id != None:
        return (True, cells[1].user_id)
    if cells[2].user_id == cells[5].user_id == cells[8].user_id != None:
        return (True, cells[2].user_id)
    return (False, 0)