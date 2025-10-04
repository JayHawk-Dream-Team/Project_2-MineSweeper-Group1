'''
ai.py
ai solver logic
Authors: Jonathan Johnston, Yoseph Ephrem, Mahdi Essawi
Created: 2025-09-23
Last Modified: 2025-10-03
Functions:
take_turn_easy: ai chooses a random cell to reveal
take_turn_medium: ai uses strategies to pick a safe cell
take_turn_hard: ai uses the same strategies as medium plus the 1-2-1
take_turn: checks current ai mode and calls the corresponding function
various helper functions for the take turn ai functions
'''

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

'''
Helper function for 1-2-1 rule that determines if a given horizontal 1-2-1 strip of cells meet the criteria for the 1-2-1 rule
takes the cell with 2 in it and checks if the cells on either the top or bottom are already revealed so that what is on the other side can be deduced
returns a string that tells which side of the 1-2-1 strip has cells that can safely be revealed
'''
def valid_horizontal_1_2_1(revealed: set[Coord], r: int, c: int, rows: int) -> str:
    if  r == 0:
        return "bottom" # 1-2-1 is on the top edge so mines must be on the bottom
    if r == rows-1:
        return "top" # 1-2-1 is on the bottomd edgs so mines be on the top
    if (r-1,c-1) in revealed and (r-1,c) in revealed and (r-1,c+1) in revealed:
        return "bottom"
    elif (r+1, c-1) in revealed and (r+1,c) in revealed and (r+1,c+1) in revealed:
        return "top"
    else:
        return "not valid"

'''
Helper function for 1-2-1 rule that determines if a given vertical 1-2-1 strip of cells meet the criteria for the 1-2-1 rule
takes the cell with 2 in it and checks if the cells on either the left or right are already revealed so that what is on the other side can be deduced
returns a string that tells which side of the 1-2-1 strip has cells that can safely be revealed
'''
def valid_vertical_1_2_1(revealed: set[Coord], r: int, c: int, cols: int) -> str:
    if  c == 0:
        return "right" # 1-2-1 is on the left edge so mines must be on the right side
    if c == cols-1:
        return "left" # 1-2-1 is on the right edgs so mines must be on the left side
    if (r-1,c-1) in revealed and (r,c-1) in revealed and (r+1,c-1) in revealed:
        return "right"
    elif (r+1, c+1) in revealed and (r,c+1) in revealed and (r-1,c+1) in revealed:
        return "left"
    else:
        return "not valid"

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


# Uses the same strategies as medium but also uses the 1-2-1 rule
def take_turn_hard(grid, bombs, revealed: Set[Coord], flagged: Set[Coord], flood_fill_fn):
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
        vertical_1_2_1 = []
        horizontal_1_2_1 = []
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
                return [("flag", hidden_neighbors[0])], f"Hard: flag at {hidden_neighbors[0]}"
        if grid[r][c] == flagged_neighbors and revealed_neighbors + flagged_neighbors != 0:
            # If number of flagged neigbor cells is equal to the number in the current cell then all unflagged hidden neigbor cells are safe so reveal one
            if hidden_neighbors:
                move_row = hidden_neighbors[0][0]
                move_col = hidden_neighbors[0][1]
                if grid[move_row][move_col] == 0:
                    reveal = flood_fill_fn(grid, move_row, move_col)
                    return[("reveal", rc) for rc in reveal], f"Hard: reveal at {hidden_neighbors[0]} (0 region)."
                return [("reveal", hidden_neighbors[0])], f"Hard: reveal at {hidden_neighbors[0]}"
        if grid[r][c] != 2: # if current cell does not hold a 2 skip the 1-2-1 check
            continue
        if 0 < c < cols-1 and (r, c-1) in revealed and (r, c+1) in revealed and grid[r][c-1] == 1 and grid[r][c+1] == 1: # checks if there is a 1-2-1 horizontal pattern
            side = valid_horizontal_1_2_1(revealed, r, c, rows)  # determines if anything can be deduced about the current 1-2-1 configuration and if so returns the side that the mines are on
            if side == "bottom":
                if (r+1, c-1) not in revealed and (r+1, c-1) not in flagged:
                    return [("flag", (r+1, c-1))], f"Hard: flag at {(r+1,c-1)}" # flag left bottom cell if not already flagged
                if (r+1, c) not in revealed:
                    return [("reveal", (r+1, c))], f"Hard: reveal at {(r+1,c)}" # reveal middle bottom cell if not already revealed
                if (r+1, c+1) not in revealed and (r+1, c+1) not in flagged:
                    return [("flag", (r+1, c+1))], f"Hard: flag at {(r+1,c+1)}" # flag right bottom cell if not already flagged
            elif side == "top":
                if (r-1, c-1) not in revealed and (r-1, c-1) not in flagged:
                    return [("flag", (r-1, c-1))], f"Hard: flag at {(r-1,c-1)}" # flag left top cell if not already flagged
                if (r-1, c) not in revealed:
                    return [("reveal", (r-1, c))], f"Hard: reveal at {(r-1,c)}" # reveal middle top cell if not already revealed
                if (r-1, c+1) not in revealed and (r-1, c+1) not in flagged:
                    return [("flag", (r-1, c+1))], f"Hard: flag at {(r-1,c+1)}" # reveal right top cell if not already flagged
        if 0 < r < rows-1 and (r-1, c) in revealed and (r+1, c) in revealed and grid[r-1][c] == 1 and grid[r+1][c] == 1: # checks if there is a 1-2-1 vertical pattern
            side = valid_vertical_1_2_1(revealed, r, c, cols) # determines if anything can be deduced about the current 1-2-1 configuration and if so returns the side that the mines are on
            if side == "right":
                if (r-1, c+1) not in revealed and (r-1, c+1) not in flagged:
                    return [("flag", (r-1, c+1))], f"Hard: flag at {(r-1,c+1)}" # flag the top right cell if not already flagged
                if (r, c+1) not in revealed:
                    return [("reveal", (r, c+1))], f"Hard: reveal at {(r,c+1)}" # reveal the middle right cell if not already revealed
                if (r+1, c+1) not in revealed and (r+1, c+1) not in flagged:
                    return [("flag", (r+1, c+1))], f"Hard: flag at {(r+1,c+1)}" # flag the bottom right cell if not already flagged
            elif side == "left":
                if (r-1, c-1) not in revealed and (r-1, c-1) not in flagged:
                    return [("flag", (r-1, c-1))], f"Hard: flag at {(r-1,c-1)}" # flag the top left cell if not already flagged
                if (r, c-1) not in revealed:
                    return [("reveal", (r, c-1))], f"Hard: reveal at {(r,c-1)}" # reveal the middle left cell if not already revealed
                if (r+1, c-1) not in revealed and (r+1, c-1) not in flagged:
                    return [("flag", (r+1, c-1))], f"Hard: flag at {(r+1,c-1)}" # flag the bottom left cell if not already flagged
    # no safe moves so pick a random cell to reveal
    pick = random.choice(candidates)
    return [("reveal", pick)], f"Hard: strategic reveal at {pick}"


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