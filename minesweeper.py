import pygame 
import random
import time
import os
from ai import take_turn  

pygame.init()
pygame.mixer.init()

# Load sound effects
SOUND_DIR = "Music_soundeffects"
background_music = pygame.mixer.Sound(os.path.join(SOUND_DIR, "Backgroundmusic.wav"))
select_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, "selectSpace.mp3"))
flag_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, "placedFlag.mp3"))
bomb_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, "bomb.mp3"))
win_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, "win.mp3"))
lose_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, "lose.mp3"))

# Set volumes
background_music.set_volume(0.05)  # Lower volume for background music
select_sound.set_volume(0.05)
flag_sound.set_volume(0.05)
bomb_sound.set_volume(1.0)
win_sound.set_volume(0.05)
lose_sound.set_volume(0.05)

def get_bomb_count():
    """
    Display a popup to get the number of bombs from the user (10-20).
    Returns the selected number of bombs.
    """
    # Create a centered dialog window
    screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
    
    # Semi-transparent overlay (like game over popup)
    overlay = pygame.Surface((BOARD_WIDTH, BOARD_HEIGHT))
    overlay.set_alpha(128)
    overlay.fill((0, 0, 0))
    
    # Popup dimensions (matching game over popup)
    popup_width = 300
    popup_height = 200
    popup_x = (BOARD_WIDTH - popup_width) // 2
    popup_y = (BOARD_HEIGHT - popup_height) // 2
    
    # Create popup rectangle
    popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
    
    # Initialize fonts (matching game over popup style)
    title_font = pygame.font.Font(None, 36)
    button_font = pygame.font.Font(None, 24)
    input_text = ""
    
    # Confirm button (styled like game over popup buttons)
    confirm_rect = pygame.Rect(popup_x + popup_width//2 - 50, popup_y + 140, 100, 40)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try:
                        bombs = int(input_text)
                        if 10 <= bombs <= 20:
                            return bombs
                    except ValueError:
                        pass
                    input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.unicode.isdigit() and len(input_text) < 2:  # Limit to 2 digits
                    input_text += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if confirm_rect.collidepoint(event.pos):
                        try:
                            bombs = int(input_text)
                            if 10 <= bombs <= 20:
                                return bombs
                        except ValueError:
                            pass
        
        # Draw semi-transparent overlay
        screen.fill((255, 255, 255))
        screen.blit(overlay, (0, 0))
        
        # Draw popup background
        pygame.draw.rect(screen, (255, 255, 255), popup_rect)
        pygame.draw.rect(screen, (0, 0, 0), popup_rect, 3)
        
        # Draw title
        title_text = title_font.render("Select Number of Bombs", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(popup_x + popup_width//2, popup_y + 40))
        screen.blit(title_text, title_rect)
        
        # Draw input box
        input_box_rect = pygame.Rect(popup_x + 75, popup_y + 80, 150, 40)
        pygame.draw.rect(screen, (240, 240, 240), input_box_rect)
        pygame.draw.rect(screen, (0, 0, 0), input_box_rect, 2)
        
        # Draw input text
        if input_text:
            text_surface = title_font.render(input_text, True, (0, 0, 0))
        else:
            text_surface = button_font.render("10-20", True, (128, 128, 128))
        text_rect = text_surface.get_rect(center=input_box_rect.center)
        screen.blit(text_surface, text_rect)
        
        # Draw confirm button (green like "Play Again")
        pygame.draw.rect(screen, (0, 200, 0), confirm_rect)
        pygame.draw.rect(screen, (0, 0, 0), confirm_rect, 2)
        confirm_text = button_font.render("Confirm", True, (255, 255, 255))
        confirm_text_rect = confirm_text.get_rect(center=confirm_rect.center)
        screen.blit(confirm_text, confirm_text_rect)
        
        pygame.display.flip()

BOARD_WIDTH: int = 530
BOARD_HEIGHT: int = 620
UI_HEIGHT: int = 120
NUM_BOMBS: int = get_bomb_count()

def generate_bombs(rows: int, cols: int, bomb_count: int) -> set[tuple[int, int]]:
    """
    Returns a set of (row, col) positions for bombs.
    Clamps bomb_count to the number of cells.
    """
    total = rows * cols
    bomb_count = max(0, min(bomb_count, total))
    choices = random.sample(range(total), bomb_count)  # unique cells
    return {(i // cols, i % cols) for i in choices}

def ensure_safe_start(grid: list[list[int]], start_row: int, start_col: int, bomb_positions: set[tuple[int, int]]) -> tuple[list[list[int]], set[tuple[int, int]]]:
    """
    Ensures the first click in minesweeper is safe and opens up an area.
    Moves bombs if needed.
   """
    rows, cols = len(grid), len(grid[0])
    protected_area = set()
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            r, c = start_row + dr, start_col + dc
            if 0 <= r < rows and 0 <= c < cols:
                protected_area.add((r, c))
    bombs_to_move = bomb_positions & protected_area #set union
    if bombs_to_move:
        all_positions = {(r, c) for r in range(rows) for c in range(cols)}
        available_positions = all_positions - bomb_positions - protected_area
        new_bomb_positions = bomb_positions.copy()
        for bomb_pos in bombs_to_move:
            if available_positions:
                new_pos = available_positions.pop()
                new_bomb_positions.remove(bomb_pos)
                new_bomb_positions.add(new_pos)
                grid[bomb_pos[0]][bomb_pos[1]] = 0
                grid[new_pos[0]][new_pos[1]] = -1
        generate_numbers(grid) #this could be optimized to only update affected areas
        return grid, new_bomb_positions
    return grid, bomb_positions


def flood_fill(grid: list[list[int]], start_row: int, start_col: int) -> set[tuple[int, int]]:
    """
    Floodfill algorithm that reveals cells with 0 bombs around them, and stops at cells with numbers.
    """
    if not grid or not grid[0]:
        return set()
    #define helper variables and preallocations
    rows = len(grid)
    cols = len(grid[0])
    if (start_row < 0 or start_row >= rows or 
        start_col < 0 or start_col >= cols or 
        grid[start_row][start_col] == -1):
        return set()
    to_reveal = set()
    to_visit = [(start_row, start_col)]
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),           (0, 1),
                  (1, -1),  (1, 0),  (1, 1)]
    # flood
    while to_visit:
        row, col = to_visit.pop()
        if (row < 0 or row >= rows or col < 0 or col >= cols or
            (row, col) in to_reveal):
            continue
        if grid[row][col] == -1:
            continue
        to_reveal.add((row, col))
        if grid[row][col] > 0:
            continue
        if grid[row][col] == 0:
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                if (0 <= new_row < rows and 0 <= new_col < cols and
                    (new_row, new_col) not in to_reveal):
                    to_visit.append((new_row, new_col))
    return to_reveal

def generate_numbers(grid):
    """
    Fill in the grid with numbers based on how mnay bombs its near
    """
    rows = len(grid)
    cols = len(grid[0])
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),           (0, 1),
                  (1, -1),  (1, 0),  (1, 1)]
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] != -1:
                bomb_count = 0
                for di, dj in directions:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < rows and 0 <= nj < cols:
                        if grid[ni][nj] == -1:
                            bomb_count += 1
                grid[i][j] = bomb_count

def draw_game_over_popup(screen, width, height, game_won=False):
    """Draw a game over popup with play again and quit buttons"""
    # Semi-transparent overlay
    overlay = pygame.Surface((width, height))
    overlay.set_alpha(128)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    
    # Popup background
    popup_width = 300
    popup_height = 200
    popup_x = (width - popup_width) // 2
    popup_y = (height - popup_height) // 2
    
    popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
    pygame.draw.rect(screen, (255, 255, 255), popup_rect)
    pygame.draw.rect(screen, (0, 0, 0), popup_rect, 3)
    
    # Title
    title_font = pygame.font.Font(None, 36)
    title_text = "You Won!" if game_won else "Game Over!"
    title_color = (0, 128, 0) if game_won else (255, 0, 0)
    title_surface = title_font.render(title_text, True, title_color)
    title_rect = title_surface.get_rect(center=(popup_x + popup_width//2, popup_y + 50))
    screen.blit(title_surface, title_rect)
    
    # Buttons
    button_font = pygame.font.Font(None, 24)
    
    # Play Again button
    play_again_rect = pygame.Rect(popup_x + 20, popup_y + 100, 100, 40)
    pygame.draw.rect(screen, (0, 200, 0), play_again_rect)
    pygame.draw.rect(screen, (0, 0, 0), play_again_rect, 2)
    play_again_text = button_font.render("Play Again", True, (255, 255, 255))
    play_again_text_rect = play_again_text.get_rect(center=play_again_rect.center)
    screen.blit(play_again_text, play_again_text_rect)
    
    # Quit button
    quit_rect = pygame.Rect(popup_x + 180, popup_y + 100, 100, 40)
    pygame.draw.rect(screen, (200, 0, 0), quit_rect)
    pygame.draw.rect(screen, (0, 0, 0), quit_rect, 2)
    quit_text = button_font.render("Quit", True, (255, 255, 255))
    quit_text_rect = quit_text.get_rect(center=quit_rect.center)
    screen.blit(quit_text, quit_text_rect)
    
    return play_again_rect, quit_rect

def auto_solve(revealed, flagged, bombs, board_rows, board_columns):
    """
    Automatically solve the puzzle using knowledge of bomb positions
    """
    # First, flag all bombs
    for bomb_pos in bombs:
        if bomb_pos not in flagged:
            flagged.add(bomb_pos)
    
    # Then reveal all safe cells
    for row in range(board_rows):
        for col in range(board_columns):
            if (row, col) not in bombs and (row, col) not in revealed:
                revealed.add((row, col))
    return True

def main():
    # Grid size
    board_rows = 10
    board_columns = 10
    cell_size = (BOARD_WIDTH - 30) // board_columns # Minus 30 for the label margin

    screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
    pygame.display.set_caption("Minesweeper")
    
    # Start background music on loop
    background_music.play(-1)  # -1 means loop indefinitely

    # Create a 2D grid
    grid = [[0 for _ in range(board_columns)] for _ in range(board_rows)]

    # Place bombs and mark grid with -1
    bombs = generate_bombs(board_rows, board_columns, NUM_BOMBS)
    for r, c in bombs:
        grid[r][c] = -1
    generate_numbers(grid)
    pygame.font.init()
    font = pygame.font.Font(None, cell_size // 2)
    print(f"💣 Bombs placed: {len(bombs)} / {NUM_BOMBS}  ✅  Grid: {board_rows}x{board_columns} 🧩")

    revealed = set()  # track revealed cells as (row, col) pairs
    flagged = set()   # track flagged cells as (row, col) pairs
    first_click = True
    ai_mode = 'off'  # off|easy|medium|hard 
    running = True
    game_over = False
    game_won = False
    start_time = time.time()
    game_started = False
    ai_action_queue = [] #list of pending steps for AI to perform
    ai_animating = False    
    ai_last_step_time = 0   
    AI_STEP_MS = 500  #delay between AI steps 
    ai_highlight_cell = None  
    ai_highlight_type = None    
    
    while running:
        screen.fill((255, 255, 255))  # white background
        
        # Draw title
        title_font = pygame.font.Font(None, 48)
        title_surface = title_font.render("MINESWEEPER", True, (0, 0, 0))
        title_rect = title_surface.get_rect(center=(BOARD_WIDTH//2, 30))
        screen.blit(title_surface, title_rect)
        
        # Draw timer
        if game_started and not game_over:
            elapsed_time = int(time.time() - start_time)
            timer_font = pygame.font.Font(None, 24)
            timer_surface = timer_font.render(f"Time: {elapsed_time}s", True, (0, 0, 0))
            screen.blit(timer_surface, (10, 60))
        
        # Draw bomb count and flag count
        bomb_font = pygame.font.Font(None, 24)
        remaining_bombs = NUM_BOMBS - len(flagged)
        bomb_surface = bomb_font.render(f"Bombs: {remaining_bombs}", True, (0, 0, 0))
        screen.blit(bomb_surface, (BOARD_WIDTH - 100, 60))  # Moved up
        
        button_width = 100
        button_height = 30
        spacing = 20
        total_width = button_width * 2 + spacing
        start_x = (BOARD_WIDTH - total_width) // 2
        y = 50

        # Auto Solve button
        solve_button_rect = pygame.Rect(start_x, y, button_width, button_height)
        pygame.draw.rect(screen, (100, 200, 100), solve_button_rect)
        pygame.draw.rect(screen, (0, 0, 0), solve_button_rect, 2)
        solve_text = bomb_font.render("Auto Solve", True, (0, 0, 0))
        solve_text_rect = solve_text.get_rect(center=solve_button_rect.center)
        screen.blit(solve_text, solve_text_rect)

        # AI Mode button
        ai_button_rect = pygame.Rect(start_x + button_width + spacing, y, button_width, button_height)
        pygame.draw.rect(screen, (180, 180, 220), ai_button_rect)
        pygame.draw.rect(screen, (0, 0, 0), ai_button_rect, 2)
        ai_text = bomb_font.render(f"AI: {ai_mode.capitalize()}", True, (0, 0, 0))
        ai_text_rect = ai_text.get_rect(center=ai_button_rect.center)
        screen.blit(ai_text, ai_text_rect)
        if ai_animating and not game_over:
            banner_font = pygame.font.Font(None, 24)
            banner = banner_font.render("AI Turn...", True, (50, 50, 50))
            banner_rect = banner.get_rect(center=(BOARD_WIDTH//2, 90))
            screen.blit(banner, banner_rect)

        if ai_animating and not game_over:
            now = pygame.time.get_ticks()
            if ai_action_queue and now - ai_last_step_time >= AI_STEP_MS:
                act, (rr, cc) = ai_action_queue.pop(0)
                ai_last_step_time = now
                ai_highlight_cell = (rr, cc)
                ai_highlight_type = act
                if act == 'flag':
                    if (rr, cc) not in revealed and (rr, cc) not in flagged:
                        flagged.add((rr, cc))
                        flag_sound.play()
                elif act == 'reveal':
                    if (rr, cc) not in flagged:
                        if grid[rr][cc] == -1:
                            # AI hit a bomb: reveal and trigger loss
                            revealed.add((rr, cc))
                            game_over = True
                            # brief visual cue followed by sounds
                            bomb_sound.play(); pygame.time.wait(300)
                            lose_sound.play()
                        else:
                            new2 = flood_fill(grid, rr, cc)
                            if new2:
                                select_sound.play()
                            revealed.update(new2)
                # If queue emptied or game ended, finalize and check win
                if (not ai_action_queue) or game_over:
                    ai_animating = False
                    if not game_over:
                        total_safe_cells = board_rows * board_columns - NUM_BOMBS
                        if len(revealed) == total_safe_cells:
                            game_won = True
                            game_over = True
                            win_sound.play()

        # --- INPUT (mouse clicks) ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                
                # Check if clicking on game over popup buttons
                if game_over:
                    play_again_rect, quit_rect = draw_game_over_popup(screen, BOARD_WIDTH, BOARD_HEIGHT, game_won)
                    if play_again_rect.collidepoint(mx, my):
                        # Reset game
                        grid = [[0 for _ in range(board_columns)] for _ in range(board_rows)]
                        bombs = generate_bombs(board_rows, board_columns, NUM_BOMBS)
                        for r, c in bombs:
                            grid[r][c] = -1
                        generate_numbers(grid)
                        revealed = set()
                        flagged = set()
                        first_click = True
                        game_over = False
                        game_won = False
                        game_started = False
                        ai_action_queue = [] #reset ai highlight
                        ai_animating = False
                        ai_last_step_time = 0
                        ai_highlight_cell = None
                        ai_highlight_type = None

                        continue
                    elif quit_rect.collidepoint(mx, my):
                        running = False
                        continue
                
                # Check auto-solve button click (centered layout)  
                button_width = 100
                button_height = 30
                spacing = 20
                total_width = button_width * 2 + spacing
                start_x = (BOARD_WIDTH - total_width) // 2
                y = 50
                solve_button_rect = pygame.Rect(start_x, y, button_width, button_height)
                ai_button_rect = pygame.Rect(start_x + button_width + spacing, y, button_width, button_height)

                if not game_over and solve_button_rect.collidepoint(mx, my):
                    if not first_click:
                        ai_animating = False
                        ai_action_queue = []
                        ai_highlight_cell = None
                        ai_highlight_type = None
                        ai_last_step_time = 0

                        if auto_solve(revealed, flagged, bombs, board_rows, board_columns):
                            game_won = True
                            game_over = True
                            win_sound.play()

                            if not game_over:
                                total_safe_cells = board_rows * board_columns - NUM_BOMBS
                                if len(revealed) == total_safe_cells:
                                    game_won = True
                                    game_over = True
                                    win_sound.play()
                    continue

                button_width = 100
                button_height = 30
                spacing = 20
                total_width = button_width * 2 + spacing
                start_x = (BOARD_WIDTH - total_width) // 2 #center the buttons
                y = 50
                solve_button_rect = pygame.Rect(start_x, y, button_width, button_height)
                ai_button_rect = pygame.Rect(start_x + button_width + spacing, y, button_width, button_height)

                if ai_button_rect.collidepoint(mx, my):
                    modes = ['off', 'easy', 'medium', 'hard']
                    try:
                        i = modes.index(ai_mode.lower())
                    except ValueError:
                        i = 0
                    ai_mode = modes[(i + 1) % len(modes)]
                    continue 

                # Game board clicks (only if not game over)
                if not game_over and my > UI_HEIGHT and mx > LABEL_MARGIN:
                    col = (mx - LABEL_MARGIN) // cell_size
                    row = (my - UI_HEIGHT) // cell_size
                    if 0 <= row < board_rows and 0 <= col < board_columns:
                        # Right click for flagging
                        if event.button == 3:  # Right click
                            if (row, col) not in revealed:
                                if (row, col) in flagged:
                                    flagged.remove((row, col))
                                    flag_sound.play()
                                else:
                                    flagged.add((row, col))
                                    flag_sound.play()
                        # Left click for revealing
                        elif event.button == 1:  # Left click
                            if (row, col) not in flagged:  # Can't reveal flagged cells
                                if first_click:
                                    grid, bombs = ensure_safe_start(grid, row, col, bombs)
                                    first_click = False
                                    game_started = True
                                    start_time = time.time()
                                if (row, col) not in revealed: # only start if it's not already revealed
                                    if grid[row][col] == -1:
                                        revealed.add((row, col))
                                        game_over = True
                                        bomb_sound.play()
                                        pygame.time.wait(500)
                                        bomb_sound.play()
                                        pygame.time.wait(500)
                                        bomb_sound.play()
                                        pygame.time.wait(500) # Wait for bomb sound
                                        lose_sound.play()
                                    else:
                                        # New Check added
                                        #if (row, col) not in revealed:   # only process if not already revealed
                                        select_sound.play()
                                        new_reveals = flood_fill(grid, row, col)
                                        revealed.update(new_reveals)
                                        
                                        # Check for win condition
                                        total_safe_cells = board_rows * board_columns - NUM_BOMBS
                                        if len(revealed) == total_safe_cells:
                                            game_won = True
                                            game_over = True
                                            win_sound.play()
                                        if not game_over and ai_mode.lower() != 'off' and not first_click and new_reveals:
                                            actions, _ = take_turn(ai_mode, grid, bombs, revealed, flagged, flood_fill)  
                                            ai_action_queue = list(actions)  
                                            ai_animating = True            
                                            ai_last_step_time = pygame.time.get_ticks() - AI_STEP_MS  # trigger first step ASAP 
                                            ai_highlight_cell = None     
                                            ai_highlight_type = None        
                                            # Post-AI win check 
                                            if not game_over:  
                                                total_safe_cells = board_rows * board_columns - NUM_BOMBS  
                                                if len(revealed) == total_safe_cells:  
                                                    game_won = True  
                                                    game_over = True 
                                                    win_sound.play()


        # Create a constant for the label margin
        LABEL_MARGIN = 30
        
        # Draw column titles (A-J)
        label_font = pygame.font.Font(None, 28) 
        
        # Draw a light gray background for the column letters
        col_letter_bg = pygame.Rect(LABEL_MARGIN, UI_HEIGHT - LABEL_MARGIN, BOARD_WIDTH - LABEL_MARGIN, LABEL_MARGIN)
        pygame.draw.rect(screen, (240, 240, 240), col_letter_bg)
        
        # Draw column labels (A-J)
        for col in range(board_columns):
            letter = chr(65 + col)  # Convert 0-9 to A-J
            text_surface = label_font.render(letter, True, (0, 0, 0))
            x = LABEL_MARGIN + col * cell_size + cell_size // 2  # Center of the column, offset by margin
            text_rect = text_surface.get_rect(center=(x, UI_HEIGHT - 15))
            screen.blit(text_surface, text_rect)
        
        # Draw row labels background (1-10)
        row_label_bg = pygame.Rect(0, UI_HEIGHT, LABEL_MARGIN, BOARD_HEIGHT - UI_HEIGHT)
        pygame.draw.rect(screen, (240, 240, 240), row_label_bg)
        
        # Draw row labels (1-10)
        for row in range(board_rows):
            number = str(row + 1)  # Convert 0-9 to 1-10
            text_surface = label_font.render(number, True, (0, 0, 0))
            y = UI_HEIGHT + row * cell_size + cell_size // 2  # Center of the row
            text_rect = text_surface.get_rect(center=(LABEL_MARGIN // 2, y))
            screen.blit(text_surface, text_rect)

        #draw board
        for row in range(board_rows):
            for col in range(board_columns):
                x = col * cell_size + LABEL_MARGIN  # Offset for row labels
                y = row * cell_size + UI_HEIGHT  # Offset for UI
                rect = pygame.Rect(x, y, cell_size, cell_size)
                if (row, col) in revealed:
                    if grid[row][col] == -1:
                        pygame.draw.rect(screen, (255, 100, 100), rect)
                        center = rect.center
                        pygame.draw.circle(screen, (0, 0, 0), center, cell_size // 4)
                    else:
                        # safe cell revealed: light gray
                        pygame.draw.rect(screen, (230, 230, 230), rect)
                        number = grid[row][col]
                        if number > 0:
                            number_colors = {
                                1: (0, 0, 255),
                                2: (0, 128, 0),
                                3: (255, 0, 0),
                                4: (128, 0, 128),
                                5: (128, 0, 0),
                                6: (64, 224, 208),
                                7: (0, 0, 0),
                                8: (128, 128, 128),
                            }
                            color = number_colors.get(number, (0, 0, 0))
                            text_surface = font.render(str(number), True, color)
                            text_rect = text_surface.get_rect(center=rect.center)
                            screen.blit(text_surface, text_rect)
                else:
                    # Unrevealed cells - draw as covered
                    pygame.draw.rect(screen, (200, 200, 200), rect)
                    # Draw flag if cell is flagged
                    if (row, col) in flagged:
                        # Draw a simple flag using pygame shapes
                        flag_size = cell_size // 3
                        flag_x = rect.centerx - flag_size // 2
                        flag_y = rect.centery - flag_size // 2
                        
                        # Flag pole (vertical line)
                        pygame.draw.line(screen, (139, 69, 19), 
                                       (flag_x, flag_y), 
                                       (flag_x, flag_y + flag_size), 3)
                        
                        # Flag (triangle)
                        flag_points = [
                            (flag_x, flag_y),
                            (flag_x + flag_size, flag_y + flag_size // 3),
                            (flag_x, flag_y + 2 * flag_size // 3)
                        ]
                        pygame.draw.polygon(screen, (255, 0, 0), flag_points)


                if ai_highlight_cell == (row, col):
                    pygame.draw.rect(screen, (255, 255, 0), rect, 3)  # yellow border
                    if ai_highlight_type == 'reveal' and grid[row][col] == -1:
                        # If AI revealed a bomb, add a red inner border cue
                        inner = rect.inflate(-6, -6)
                        pygame.draw.rect(screen, (255, 0, 0), inner, 3)

                # cell border
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)
    
        # Draw game over popup if game is over
        if game_over:
            draw_game_over_popup(screen, BOARD_WIDTH, BOARD_HEIGHT, game_won)
        #update display
        pygame.display.flip()
    # Stop background music and quit
    background_music.stop()
    pygame.quit()

main()
