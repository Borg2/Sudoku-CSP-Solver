# Sudoku CSP solver
Welcome to Sudoku Game! This Python program allows you to play Sudoku puzzles and solve them using different algorithms. You can also generate Sudoku puzzles of varying difficulty levels.

## Features
* Board Class: Manages the Sudoku grid, including setting and getting cell values, validating moves, and generating Sudoku puzzles.
* CSP Class: Implements Constraint Satisfaction Problem (CSP) algorithms for solving Sudoku puzzles, including arc consistency and backtracking.
* Sudoku Solver: Provides functions to solve Sudoku puzzles using backtracking and CSP algorithms.
* Validation: Includes functions to validate whether a Sudoku grid is valid.
## Modes
### AI Solver Mode
In this mode, the program generates a Sudoku puzzle and solves it automatically using advanced algorithms like CSP, MRV, LCV, and arc consistency.
### Manual input Mode
This mode enables users to input a Sudoku puzzle manually and then allows the AI to solve it using the same algorithms as in the AI Solver Mode.
### Interactive Mode
Interactive Mode lets users play Sudoku interactively. The program generates a Sudoku puzzle, and users can attempt to solve it. If a move is invalid or leads to a dead-end, the AI will reject it and suggest alternatives.
## Usage
1-Choose the desired mode by executing the appropriate command.<br>
2-Follow the on-screen instructions to play Sudoku.<br>
3-Enjoy the game and challenge yourself!
## Code Structure
* Board Class: Manages the Sudoku grid, including cell values and puzzle generation.
* CSP Class: Implements CSP algorithms for solving Sudoku puzzles.
* Sudoku Solver Functions: Includes functions for solving Sudoku puzzles using backtracking and CSP algorithms.
* Validation Functions: Contains functions to validate the correctness of Sudoku grids.
