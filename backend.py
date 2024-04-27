import numpy as np
import random


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

    def generate_sudoku_puzzle(self):
        self.generate_full_sudoku()

        # Remove numbers to create the puzzle
        remaining_cells = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(remaining_cells)
        for _ in range(81 - 15):
            row, col = remaining_cells.pop()
            self.grid[row][col] = 0

        return self.grid

    def generate_empty_sudoko(self):
        self.grid = np.zeros((9, 9), dtype=int)
        return self.grid

class CSP:
    def __init__(self, variables) -> None:
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
                    self.domain[(i,j)] = [1,2,3,4,5,6,7,8,9] 
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

    def revise(self, arc) -> bool:
        revised = False
        x1, x2 = arc
        if x1 in self.domain:
            for x in list(self.domain[x1]):
                if not any(self.is_consistent(x, y) for y in self.domain[x2]):
                    self.domain[x1].remove(x)
                    revised = True
    
        return revised


    def is_consistent(self, x1, x2):
        return x1 != x2

    def arc_algorithm(self) -> bool:
        queue = self.constraints[:]
        while queue:
            arc = queue.pop(0)
            x1, x2 = arc
            if self.revise(arc):
                if len(self.domain[x1]) == 0:
                    return False
                for i in range(9):
                    for j in range(9):
                        if (i, j) != x1 and (i, j) != x2:
                            queue.append(((i, j), x1))
        return True, self.domain

    def resultant_grid(self):
        result = Board()
        for key, value in self.domain.items():
            i,j = key
            if len(value) == 1:
                result.grid[i,j] = value[0]
        return result

                   


    


