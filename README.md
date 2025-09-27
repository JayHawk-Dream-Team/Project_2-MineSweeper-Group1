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
- Auto Solve (instant solve using bomb knowledge)
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
- Auto solver (flags all bombs + reveals all safe cells)
- AI mode cycling button (Off → Easy → Medium → Hard)
- Easy AI: chooses a random hidden, unflagged cell and reveals (with flood fill when 0)
- **Medium AI: TODO**
- **Hard AI: TODO**
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
| Auto Solve instantly | Click "Auto Solve" button |
| Confirm bomb count | Enter / Confirm button after typing (10–20) |
| Play Again (after end) | Click green "Play Again" |
| Quit (after end) | Click red "Quit" |


## Time Taken

| Name                 | Expected Time        | Actual Time            |
|----------------------|----------------------|------------------------|
| Carlos Mbendera      | 2–3 hours            | 1 hour                 |
| Yoseph Ephrem        | 1 hour 30 min        | 2 hours 30 min         |
| Cole DuBois          | 1 hour               | 2 hours 30 min         |
| Blake Ebner          | 45 min               | 45 min                 |
| Mahdi Essawi         | PENDING              | PENDING                |
| Jonathan Johnston    | PENDING              | PENDING                |


### Time Estimation Method

These times exclude meetings and research.

Similar to Project 1, to calculate the expected amount of time for work, we allowed each individual to approximate their own respective hours as we believed that due our own personal difference in experience and technical history that we’d be our best estimates since the workload was divided depending on what everyone’s strengths were. 

### Time Tracking Tools

Similar to Project 1, we used GitHub extensively and [GitHub Projects]([url](https://github.com/orgs/JayHawk-Dream-Team/projects/3)) to keep track of our roles, tasks and timelines of each other's work.

By observing [our GitHub Project](https://github.com/orgs/JayHawk-Dream-Team/projects/3), you shall notice that we had a planning board to separate tasks into 3 sections, Todo, In Progress, Done. This made it possible for everyone to be synchronized on the status of components they may be dependent on.

Additionally, we also had used the Roadmap feature to get a rough timeline of when everything was needed on an iteration by iteration basis. In this case, each iteration was a week.

A new addition for this project is that we also used a simple list view. This was because the tasks we had were a lot smaller than project 1.

## Screenshots As of September 27, 2025 of GitHub Project

<img width="1840" height="1112" alt="Screenshot 2025-09-27 at 4 15 33 PM" src="https://github.com/user-attachments/assets/3f91b6d1-ab05-4e62-a412-561c572b962f" />
<img width="1840" height="1112" alt="Screenshot 2025-09-27 at 4 15 31 PM" src="https://github.com/user-attachments/assets/a9c5f0ec-7fa9-4435-a476-761f3fa3d090" />
<img width="1840" height="1112" alt="Screenshot 2025-09-27 at 4 15 41 PM" src="https://github.com/user-attachments/assets/ec3c922c-c926-4130-8f91-4ce81d383bc7" />

## Project Arch

<img width="952" height="760" alt="Screenshot 2025-09-27 at 4 05 51 PM" src="https://github.com/user-attachments/assets/e6a0c375-71a4-42cb-9ae2-5ecffcedd204" />


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
