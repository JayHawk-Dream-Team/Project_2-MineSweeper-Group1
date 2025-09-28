import random
from typing import List, Tuple, Set

Coord = Tuple[int, int] #use tuples for the coordinates and actions for ai
Action = Tuple[str, Coord] 

def hidden_unflagged(rows: int, cols: int, revealed: Set[Coord], flagged: Set[Coord]) -> List[Coord]:
    #find hidden or unflagged cells
    return [
        (r, c) #for each cell at row r, col c
        for r in range(rows) #loop through all rows and columns
        for c in range(cols)       
        if (r, c) not in revealed #include only if the cell is not revealed or flagged
        and (r, c) not in flagged       
    ]

def take_turn_easy(grid, bombs, revealed: Set[Coord], flagged: Set[Coord], flood_fill_fn):
    #easy mode chooses randomly to reveal
    rows, cols = len(grid), len(grid[0])
    candidates = hidden_unflagged(rows, cols, revealed, flagged) #find all options to possibly pick from
    if not candidates:
        return [], "No moves available."
    pick = random.choice(candidates) #select randomly
    r, c = pick
    if grid[r][c] == 0: #if cell is safe reveal with flood fill
        reveals = flood_fill_fn(grid, r, c)
        return [("reveal", rc) for rc in reveals], f"Easy: random reveal at {pick} (0 region)."
    return [("reveal", pick)], f"Easy: random reveal at {pick}."

#modes to be implemented
def take_turn_medium(grid, bombs, revealed: Set[Coord], flagged: Set[Coord], flood_fill_fn):
    return [],

def take_turn_hard(grid, bombs, revealed: Set[Coord], flagged: Set[Coord], flood_fill_fn):
    rows, cols = len(grid), len(grid[0])

    candidates = [
        (r, c)
        for r in range(rows)
        for c in range(cols)
        if (r, c) not in revealed
        and (r, c) not in flagged
        and (r, c) not in bombs
    ]

    if not candidates:
        return [], "No safe moves available."

    # pick a random safe hidden cell
    pick = random.choice(candidates)
    r, c = pick

    if grid[r][c] == 0:
        reveal = flood_fill_fn(grid, r, c)
        return [("reveal", rc) for rc in reveal], f"Hard: Smart reveal at {pick} (0 region)."
    
    return [("reveal", pick)], f"Hard: Smart reveal at {pick}."



def take_turn(mode: str, grid, bombs, revealed: Set[Coord], flagged: Set[Coord], flood_fill_fn):
    #mode director function
    mode = (mode or "off").lower()
    if mode == "easy":
        return take_turn_easy(grid, bombs, revealed, flagged, flood_fill_fn)
    if mode == "medium":
        return take_turn_medium(grid, bombs, revealed, flagged, flood_fill_fn)
    if mode == "hard":
        return take_turn_hard(grid, bombs, revealed, flagged, flood_fill_fn)
    return [], "AI off."