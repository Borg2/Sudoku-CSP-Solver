import numpy as np
import random
import copy

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

    def is_valid_move(self, row, col, value):
        # Check if placing a value in a cell is a valid move
        return (
                self.is_valid_row(row, value) and
                self.is_valid_column(col, value) and
                self.is_valid_subgrid(row, col, value)
        )

    def is_valid_row(self, row, value):
        # Check if placing a value in a row is valid
        return value not in self.grid[row]

    def is_valid_column(self, col, value):
        # Check if placing a value in a column is valid
        return value not in self.grid[:, col]

    def is_valid_subgrid(self, row, col, value):
        # Check if placing a value in a 3x3 subgrid is valid
        subgrid_row_start = (row // 3) * 3
        subgrid_col_start = (col // 3) * 3
        subgrid_values = self.grid[subgrid_row_start:subgrid_row_start + 3, subgrid_col_start:subgrid_col_start + 3]
        return value not in subgrid_values

    def generate_full_sudoku(self):
        def solve_sudoku(grid):
            for i in range(9):
                for j in range(9):
                    if grid[i][j] == 0:
                        random.shuffle(numbers)
                        for num in numbers:
                            if self.is_valid_move(i, j, num):
                                grid[i][j] = num
                                if solve_sudoku(grid):
                                    return True
                                grid[i][j] = 0
                        return False
            return True

        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        solve_sudoku(self.grid)

    def generate_sudoku_puzzle(self,difficulty_level):
        self.generate_full_sudoku()
        if difficulty_level == 1:
            num_cells_to_keep = 15 # Hard
        elif difficulty_level == 2:
            num_cells_to_keep = 20  # Medium
        elif difficulty_level == 3:
            num_cells_to_keep = 30  # Easy

        # Remove numbers to create the puzzle
        remaining_cells = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(remaining_cells)
        for _ in range(81 - num_cells_to_keep):
            row, col = remaining_cells.pop()
            self.grid[row][col] = 0

        return self.grid

    def generate_empty_sudoko(self):
        self.grid = np.zeros((9, 9), dtype=int)
        return self.grid

class CSP:
    def __init__(self) -> None:
        variables = np.empty((9,9), dtype=tuple)
        for i in range(9):
            for j in range(9):
                variables[i, j] = (i, j)
        self.variables = variables
        self.domain = {}
        self.constraints = []

    def create_domain_list(self, puzzle: Board)->dict:
        self.domain = {}
        for i in range(9):
            for j in range(9):
                x = puzzle.get_value(i,j)
                if x != 0:
                    self.domain[(i,j)] = [x]
                else:
                    self.domain[(i,j)] = [num for num in range(1,10) if puzzle.is_valid_move( i,j, num)]
        return self.domain            


    def create_constraints(self) -> list:
        self.constraints = []

        # Row and Column constraints
        for i in range(9):
            for j in range(9):
                for k in range(j + 1, 9):
                    # Add row constraint
                    self.constraints.append((self.variables[i, j], self.variables[i, k]))
                    # Add column constraint
                    self.constraints.append((self.variables[j, i], self.variables[k, i]))

        # Subgrid constraints
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                for ii in range(3):
                    for jj in range(3):
                        for di in range(3):
                            for dj in range(3):
                                if (ii != di or jj != dj):
                                    self.constraints.append((self.variables[i + ii, j + jj], self.variables[i + di, j + dj]))

        return self.constraints

    def count_constraint_violations(self, row, col, value):
        count = 0
        for neighbor in self.get_neighbors((row, col)):
            if neighbor != (row, col) and value in self.domain[neighbor]:
                count += 1
        return count

    def revise(self, arc) -> bool:
        revised = False
        x1, x2 = arc
        if x1 in self.domain:
            for x in list(self.domain[x1]):
                if not any(self.is_consistent(x, y) for y in self.domain[x2]):
                    print(f"Removing {x} from the domain of {x1}")
                    self.domain[x1].remove(x)
                    revised = True
    
        return revised

    def get_neighbors(self, cell):
        row, col = cell
        neighbors = []

        # Find neighbors in the same row
        for i in range(9):
            if i != col:
                neighbors.append((row, i))

        # Find neighbors in the same column
        for j in range(9):
            if j != row:
                neighbors.append((j, col))

        # Find neighbors in the same 3x3 subgrid
        subgrid_row_start = (row // 3) * 3
        subgrid_col_start = (col // 3) * 3
        for i in range(subgrid_row_start, subgrid_row_start + 3):
            for j in range(subgrid_col_start, subgrid_col_start + 3):
                if (i, j) != cell:
                    neighbors.append((i, j))

        return neighbors
    def is_consistent(self, x1, x2):
        return x1 != x2

    def arc_algorithm(self) -> bool:
        queue = self.constraints[:]
        while queue:
            arc = queue.pop(0)
            x1, x2 = arc
            if self.revise(arc):
                if len(self.domain[x1]) == 0:
                    print(f"Domain of {x1} is empty after revision.")
                    return False
                print(f"Revised domain of {x1}: {self.domain[x1]}")
                for neighbor in self.get_neighbors(x1):
                    if neighbor != x2:
                        queue.append((neighbor, x1))
        return True

    def get_empty_cell(self,grid):
        min_remaining_values=float("inf")
        cell_posistion=None
        for i in range(9):
            for j in range(9):
                if grid[i,j] == 0:
                    remaining_values = len(self.domain[i,j])
                    if remaining_values < min_remaining_values:
                        min_remaining_values = remaining_values
                        cell_posistion=(i,j)
        return cell_posistion
    
    def backtrack(self, puzzle:Board):
        #MRV
        empty_cell = self.get_empty_cell(puzzle.grid)
        if empty_cell == None:
            return True

        row,col=empty_cell
        #LCV
        domain_values=sorted(self.domain[row, col], key=lambda value: self.count_constraint_violations(row, col, value))

        for value in domain_values:
            if puzzle.is_valid_move( row, col, value):
                puzzle.grid[row, col] = value
                print(f"Placing value {value} at {row},{col}")
                self.domain[row,col]=[value]
                arc_consistency=self.arc_algorithm()
                if arc_consistency:
                    result = self.backtrack(puzzle)
                    if result:
                        return True
                puzzle.grid[row,col]=0
                print(f"resseting value {value} at {row},{col} after backtrack failure")
                self.create_domain_list(puzzle)

        return False

    def solve_sudoku(self, puzzle: Board):
        self.create_domain_list(puzzle)
        self.create_constraints()
        self.arc_algorithm()
        puzzle_copy=copy.deepcopy(puzzle)
        result=self.backtrack(puzzle_copy)
        if result:
            return puzzle_copy
        return None

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
