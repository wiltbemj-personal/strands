# Strands Codebase Summary

Welcome to the **Strands** custom puzzle generator project! This repository contains a complete, self-contained system to generate and play custom clones of the popular NYT "Strands" game.

## Codebase Architecture
The project has the following directory structure:
- [index.html](file:///Users/wiltbemj/strands/index.html): The main hub directory listing available custom puzzles.
- [generate_puzzle.py](file:///Users/wiltbemj/strands/generate_puzzle.py): The core generation engine that processes puzzle configurations (YAML) into fully playable, interactive, and styled HTML files.
- **puzzles/**: Directory containing configuration files and their output HTML games.
  - [helens_birthday.yaml](file:///Users/wiltbemj/strands/puzzles/helens_birthday.yaml) / [helens_birthday.html](file:///Users/wiltbemj/strands/puzzles/helens_birthday.html): A puzzle celebrating Helen's birthday.
  - [moms_birthday.yaml](file:///Users/wiltbemj/strands/puzzles/moms_birthday.yaml) / [moms_birthday.html](file:///Users/wiltbemj/strands/puzzles/moms_birthday.html): A puzzle celebrating Mom's birthday.
- **words/**:
  - [common_words.txt](file:///Users/wiltbemj/strands/words/common_words.txt): A word list containing common English words (3-8 letters) to identify valid non-theme words and award hint credits.

---

## How the Generator Works

The generator script ([generate_puzzle.py](file:///Users/wiltbemj/strands/generate_puzzle.py)) automates the layout and rendering process:

1. **Input Parsing**: Reads a YAML configuration file containing:
   - `theme`: The user-visible clue or title.
   - `spangram`: A special theme word/phrase that spans the board from left to right.
   - `words`: The list of theme words.
   - `author` / `date`: Optional metadata for the completion screen.
2. **Strict Layout Constraint**: The sum of all letters in the theme words and the spangram must be exactly **48**.
   - The game board is a fixed 6x8 grid.
   - Every single cell in the grid must belong to a theme word or the spangram (no unused letters).
3. **Backtracking Placement Algorithm**:
   - The spangram is placed first using backtracking. It is forced to start at column 0 and end at column 7, touching both edges.
   - Theme words are then placed recursively in random order using a path-finding backtrack search.
   - If a valid layout is found, the script generates a standalone HTML page.
4. **Self-Contained Output**: The output HTML file contains:
   - The styled layout of the grid.
   - Embedded JSON representation of the puzzle placements.
   - Embedded JSON list of all valid non-theme dictionary words (for hints).

---

## Game Mechanics (Frontend)
The generated puzzle is highly polished and runs entirely client-side:
- **Interactive Board**: Drag or tap to chain letters together horizontally, vertically, or diagonally.
- **Visual Connectors**: An SVG path dynamically connects the selected cells in real-time.
- **Hints**:
  - Finding a valid dictionary word that isn't a theme word adds **1 hint credit**.
  - **3 hint credits** can be redeemed for a hint.
  - Clicking "Hint" highlights the cells of one random remaining theme word.
- **Win State**: When all theme words and the spangram are found, a win dialog pops up showing statistics (time taken, hints used) with a "Share Result" button.

---

## Preparing to Add New Puzzles

To add a new puzzle, we need to:
1. Define a list of theme words and a spangram such that the total length of all letters is **exactly 48**.
2. Make sure the spangram itself can stretch across the grid (usually at least 6-8 letters is recommended).
3. Write a YAML configuration file under the `puzzles/` directory.
4. Run the generator script using the Conda environment:
   ```bash
   /Users/wiltbemj/miniconda3/envs/strands/bin/python3 generate_puzzle.py puzzles/your_puzzle.yaml
   ```
5. Link the new puzzle in the landing page ([index.html](file:///Users/wiltbemj/strands/index.html)).
