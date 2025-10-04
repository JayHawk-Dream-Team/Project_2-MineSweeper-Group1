# Minesweeper Updates – Project 2

Coming from Team 16, the group that built "The Greatest Game of Minesweeper" comes an update of another team's work.

## Overview of new things

Firstly, before adding new features, we had to make that Project 1's goals were achieved. Upon investigation, we found a few things lacking.

Hence, we added:

- Row Labels
- Column Labels
- Bomb Selection
  
New Features added as part of Project 2 are:
- Sound effects and background music
- Auto Solve 
- Selectable AI modes ( Off, Easy, Medium and Hard)

## Quick Start
```bash
git clone https://github.com/JayHawk-Dream-Team/Project_2-MineSweeper-Group1
cd Project_2-MineSweeper-Group1
python -m venv .venv
source .venv/bin/activate 
pip install pygame
python minesweeper.py
```
---
## Features
- Configurable bomb count
- Visual board with coordinate labels (A–J, 1–10)
- Right click flag placement
- Automatic expansion of zero regions 
- Auto solver 
- AI mode cycling button (Off → Easy → Medium → Hard)
- Easy AI
- Medium AI
- Hard AI
- Sound effects for: select, flag, bomb, win, lose, background music

---
## AI Overview
`ai.py` exposes a `take_turn(mode, grid, bombs, revealed, flagged, flood_fill_fn)` returning a list of actions and a status message.

Action tuple format:
```
("reveal" | "flag", (row, col))
```

---
## Controls
| Action | Input |
|--------|-------|
| Reveal cell | Left click |
| Place/remove flag | Right click |
| Cycle AI mode | Click "AI: <Mode>" button |
| Auto Solver | Click "Auto Solve" button |
| Confirm bomb count | Enter / Confirm button after typing (10–20) |
| Play Again (after end) | Click green "Play Again" |
| Quit (after end) | Click red "Quit" |

## References
- Course project 2 for EECS 581. Original requirements: https://people.eecs.ku.edu/~saiedian/581/Proj/proj2
- JayHawk Dream Team Project 1 Submission: https://github.com/JayHawk-Dream-Team/EECS581MineSweeper

## Beautiful Pictures (Gameplay Screenshots) 

## Version as of 27 September, 2025
<img width="642" height="760" alt="Screenshot 2025-09-27 at 3 49 33 PM" src="https://github.com/user-attachments/assets/0e0707ed-5def-4c7e-87eb-7baf80694c2c" />
<img width="642" height="760" alt="Screenshot 2025-09-27 at 3 49 42 PM" src="https://github.com/user-attachments/assets/0bb2c6d9-22c0-4068-9e16-a064bcad8e2b" />
<img width="642" height="760" alt="Screenshot 2025-09-27 at 3 49 56 PM" src="https://github.com/user-attachments/assets/7c9dd5a9-2188-4b95-9c2b-afa7bdc01947" />

## Initial Verion From Other Team

<img width="612" height="740" alt="Screenshot 2025-09-27 at 3 52 08 PM" src="https://github.com/user-attachments/assets/8416db22-25f7-4cbe-8054-680401535795" />

<img width="612" height="740" alt="Screenshot 2025-09-27 at 3 52 42 PM" src="https://github.com/user-attachments/assets/508ab582-cb4f-4501-998d-c4c4b0ff1a5b" />
