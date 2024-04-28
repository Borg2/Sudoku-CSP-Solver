import numpy as np
import random

def is_valid_row(grid, row, value):
    # Check if placing a value in a row is valid
    return value not in grid[row]

def is_valid_column(grid, col, value):
    # Check if placing a value in a column is valid
    return value not in grid[:, col]

def is_valid_subgrid(grid, row, col, value):
    # Check if placing a value in a 3x3 subgrid is valid
    subgrid_row_start = (row // 3) * 3
    subgrid_col_start = (col // 3) * 3
    subgrid_values = grid[subgrid_row_start:subgrid_row_start + 3, subgrid_col_start:subgrid_col_start + 3]
    return value not in subgrid_values

def is_valid_move(grid, row, col, value):
    # Check if placing a value in a cell is a valid move
    return (
            is_valid_row(grid, row, value) and
            is_valid_column(grid, col, value) and
            is_valid_subgrid(grid, row, col, value)
    )

class Board:
    def __init__(self):
        # Initialize an empty Sudoku grid
        self.grid = np.zeros((9, 9), dtype=int)

    def set_value(self, row, col, value):
        # Set the value of a cell in the Sudoku grid
        self.grid[row][col] = value

    def get_value(self, row, col) -> int:
        # Get the value of a cell in the Sudoku grid
        return self.grid[row][col]

    def generate_empty_sudoko(self):
        self.grid = np.zeros((9, 9), dtype=int)
        return self.grid
    
def get_domain_values(grid,row,col):
    domain_values = [num for num in range(1,10) if is_valid_move(grid, row, col, num)]
    return domain_values
    
def next_empty_cell(grid):
    min_remaining_values = float('inf')
    cell_position = None
    for i in range(9):
        for j in range(9):
            if grid[i,j] == 0:  # Access the value using array indexing
                remaining_values = len(get_domain_values(grid, i, j))
                if remaining_values < min_remaining_values:
                    min_remaining_values = remaining_values
                    cell_position = (i, j)
    return cell_position


def count_constrained_values(grid, row, col, num):
    count = 0
    for i in range(9):
        if i != col and not is_valid_move(grid, row, i, num):
            count += 1
        if i != row and not is_valid_move(grid, i, col, num):
            count += 1
    for i in range(row - row % 3, row - row % 3 + 3):
        for j in range(col - col % 3, col - col % 3 + 3):
            if (i != row or j != col) and not is_valid_move(grid, i, j, num):
                count += 1
    return count

def forward_checking(grid, row, col, num):
    original_board = np.copy(grid)  # Make a copy of the board before making changes

    # Make the assignment
    grid[row][col] = num

    # Check consistency with peers
    for i in range(9):
        if i != col and grid[row][i] == num:  # Check for conflicts in the same row
            grid = original_board  # Revert the assignment
            return False
        if i != row and grid[i][col] == num:  # Check for conflicts in the same column
            grid = original_board  # Revert the assignment
            return False
    for i in range(row - row % 3, row - row % 3 + 3):
        for j in range(col - col % 3, col - col % 3 + 3):
            if (i != row or j != col) and grid[i][j] == num:  # Check for conflicts in the same 3x3 subgrid
                grid = original_board  # Revert the assignment
                return False

    return True  # No conflicts found

def apply_arc_consistency(grid):
    queue = []
    domains = [[list(range(1, 10)) for _ in range(9)] for _ in range(9)]
    steps = []  # List to store the steps of arc consistency

    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                domains[i][j] = [grid[i][j]]
                queue.append((i, j))

    def revise(xi, xj):
        revised = False
        removed_values = []
        for value in domains[xi[0]][xi[1]]:
            if isinstance(domains[xj[0]][xj[1]], list) and value in domains[xj[0]][xj[1]]:
                domains[xi[0]][xi[1]].remove(value)
                removed_values.append(value)
                revised = True
        if revised:
            steps.append(((xi[0], xi[1]), (xj[0], xj[1]), removed_values))
            print(f"Revised: {removed_values} removed from ({xi[0]}, {xi[1]})'s domain due to ({xj[0]}, {xj[1]})")
        return revised

    while queue:
        xi, xj = queue.pop(0)
        print(f"Processing cell ({xi}, {xj})")
        for i in range(9):
            if i != xi and revise((i, xj), (xi, xj)):
                if len(domains[i][xj]) == 0:
                    return None, steps
                queue.append((i, xj))
        for j in range(9):
            if j != xj and revise((xi, j), (xi, xj)):
                if len(domains[xi][j]) == 0:
                    return None, steps
                queue.append((xi, j))

    return domains, steps

def backtracking(grid):
    empty_cell = next_empty_cell(grid)
    print(f"MRV is {empty_cell}")
    if empty_cell is None:
        return True

    row, col = empty_cell
    domain_values = get_domain_values(grid, row, col)
    domain_values.sort(key=lambda num: count_constrained_values(grid, row, col, num))

    print(f"Attempting to fill cell ({row}, {col}) with domain values: {domain_values}")

    for num in domain_values:
        print(f"Trying value {num} for cell ({row}, {col})")
        if is_valid_move(grid, row, col, num):
            grid[row][col] = num
            print("Applying forward checking")
            if apply_arc_consistency(grid) is not None:
                print("Forward checking successful")
                if backtracking(grid):
                    return True

            print(f"Value {num} for cell ({row}, {col}) leads to conflict. Backtracking...")
            grid[row][col] = 0
        else:
            print(f"Value {num} is not valid for cell ({row}, {col}). Skipping...")

    print(f"No valid value found for cell ({row}, {col}). Backtracking...")
    return False

import numpy as np

def solve_sudoku(grid):
    board_copy = np.copy(grid)  # Create a copy of the grid using np.copy

    if not backtracking(board_copy):
        print("The puzzle is unsolvable.")
        return None

    domains, steps = apply_arc_consistency(board_copy)
    if domains is None:
        print("Arc consistency failed. The puzzle might be unsolvable.")
        return None

    # Create a new Board instance to store the solved puzzle
    solved_board = Board()

    # Fill the solved values into the Board instance
    for i in range(9):
        for j in range(9):
            if isinstance(domains[i][j], list) and len(domains[i][j]) == 1:
                solved_board.set_value(i, j, domains[i][j][0])

    return solved_board

def is_valid_sudoku(grid):
    def is_valid_row(row):
        seen = set()
        for num in grid[row]:
            if num != 0:
                if num in seen:
                    return False
                seen.add(num)
        return True

    def is_valid_column(col):
        seen = set()
        for row in range(9):
            num = grid[row][col]
            if num != 0:
                if num in seen:
                    return False
                seen.add(num)
        return True

    def is_valid_subgrid(start_row, start_col):
        seen = set()
        for row in range(start_row, start_row + 3):
            for col in range(start_col, start_col + 3):
                num = grid[row][col]
                if num != 0:
                    if num in seen:
                        return False
                    seen.add(num)
        return True

    for i in range(9):
        if not is_valid_row(i) or not is_valid_column(i):
            return False

    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            if not is_valid_subgrid(i, j):
                return False

    return True

def generate_random_puzzle(difficulty_level):
    # Create an empty Sudoku board
    board = Board()

    # Determine the range of numbers to remove based on the difficulty level
    if difficulty_level == 1:
        num_cells_to_keep = 15 # Hard
    elif difficulty_level == 2:
        num_cells_to_keep = 20  # Medium
    elif difficulty_level == 3:
        num_cells_to_keep = 30  # Easy

    # Fill random places of the puzzle
    for _ in range(num_cells_to_keep):
        row, col, num = np.random.randint(9), np.random.randint(9), np.random.randint(9)  # Randomize row, col, and num
        while not is_valid_move(board.grid, row, col, num + 1):  # Check if move is valid
            row, col, num = np.random.randint(9), np.random.randint(9), np.random.randint(9)
        board.set_value(row, col, num + 1)

    return board

