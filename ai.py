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

# Given a cell the function returns a list containing the neighboring cells and the given cell coordinates
def neighbors_inclusive(cell_row: int, cell_col: int, rows, cols) -> List[Coord]:
    neighbor_cells = []
    cols_before = 1
    cols_after = 1
    rows_before = 1
    rows_after = 1
    if cell_row == 0:
        rows_before = 0
    if cell_row == rows-1:
        rows_after = 0
    if cell_col == 0:
        cols_before = 0
    if cell_col == cols-1:
        cols_after = 0
    for row in range(cell_row - rows_before, cell_row + rows_after + 1):
        for col in range(cell_col - cols_before, cell_col + cols_after + 1):
            neighbor_cells.append((row,col))
    return neighbor_cells

# Given a cel teh function returns a list containing the neighboring cells and the given cell coordinates
def neighbors(cell_row: int, cell_col: int, rows, cols) -> List[Coord]:
    neighbor_cells = neighbors_inclusive(cell_row, cell_col, rows, cols)
    neighbor_cells.remove((cell_row,cell_col))
    return neighbor_cells

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


# Medium AI mode uses strategy to make a safe move
# If no safe moves are available then it chooses a random cell
def take_turn_medium(grid, bombs, revealed: Set[Coord], flagged: Set[Coord], flood_fill_fn):
    rows, cols = len(grid), len(grid[0])
    candidates = hidden_unflagged(rows, cols, revealed, flagged)
    if not candidates:
        return [], "No moves available"
    for cell in revealed: 
        # Iterate through the revealed cells
        r, c = cell
        neighbor_cells = neighbors(r, c, rows, cols) # find revealed cells neighbors
        flagged_neighbors = 0
        hidden_neighbors = []
        revealed_neighbors = 0
        for neighbor in neighbor_cells: # Check the neighboring cells
            if neighbor in flagged:
                flagged_neighbors += 1
            elif neighbor not in revealed:
                hidden_neighbors.append(neighbor)
            else:
                revealed_neighbors += 1
        if grid[r][c] == flagged_neighbors + len(hidden_neighbors): 
            # If number of hidden neigbor cells and flagged neigbor cells equals the number in the current cell then all hidden neigboring cells are mines so flag one
            if hidden_neighbors:
                return [("flag", hidden_neighbors[0])], f"Medium: strategic flag at {hidden_neighbors[0]}"
        if grid[r][c] == flagged_neighbors and revealed_neighbors + flagged_neighbors != 0:
            # If number of flagged neigbor cells is equal to the number in the current cell then all unflagged hidden neigbor cells are safe so reveal one
            if hidden_neighbors:
                move_row = hidden_neighbors[0][0]
                move_col = hidden_neighbors[0][1]
                if grid[move_row][move_col] == 0:
                    reveal = flood_fill_fn(grid, move_row, move_col)
                    return[("reveal", rc) for rc in reveal], f"Medium: strategic reveal at {hidden_neighbors[0]} (0 region)."
                return [("reveal", hidden_neighbors[0])], f"Medium: strategic reveal at {hidden_neighbors[0]}"
    # No safe move so pick a random cell
    pick = random.choice(candidates)
    return [("reveal", pick)], f"Medium: strategic reveal at {pick}"

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