import pygame
import sys
from backend import Board, generate_random_puzzle , solve_sudoku, is_valid_sudoku, is_valid_move
import numpy as np
import os

# Initialize Pygame
pygame.init()

# Set up the window
WINDOW_SIZE = 560
WINDOW = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Sudoku")

# Load background image
background_image = pygame.image.load("menu_background.png").convert()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

# Use a specific font for the buttons
button_font = pygame.font.SysFont("Jungle Adventurer", 40)  # Change "None" to specify the font name if desired

# Define a context manager to temporarily suppress prints
class SuppressPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')  # Redirect stdout to /dev/null

    def __exit__(self, exc_type, exc_value, traceback):
        sys.stdout.close()
        sys.stdout = self._original_stdout  # Restore original stdout

# Define buttons
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.border_color = WHITE  # Border color
        self.text_color = BLACK  # Text color

    def draw(self, surface, hovered):
        # Draw button border
        pygame.draw.rect(surface, self.border_color, self.rect, 2)  # 2 is the width of the border

        # Change button color when hovered
        if hovered:
            pygame.draw.rect(surface, self.hover_color, self.rect)
            self.text_color = WHITE  # Change text color to white when hovered
        else:
            pygame.draw.rect(surface, self.color, self.rect)
            self.text_color = BLACK  # Change text color to black when not hovered

        # Render text
        text_surface = button_font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)

    def change_text(self, text):
        self.text = text


def draw_sudoku_grid(window, grid):
    # Draw Sudoku grid
    cell_size = 60
    bold_line_width = 4  # Adjust the width of the bold lines as needed
    # Draw bold lines around subgrids
    for i in range(3):
        for j in range(3):
            pygame.draw.rect(window, BLACK, (50 + j * 3 * cell_size, 50 + i * 3 * cell_size,
                                             3 * cell_size, 3 * cell_size), bold_line_width)

    for i in range(9):
        for j in range(9):
            pygame.draw.rect(window, BLACK, (50 + j * cell_size, 50 + i * cell_size, cell_size, cell_size), 1)
            if grid[i, j] != 0:
                text_surface = button_font.render(str(grid[i, j]), True, BLACK)
                text_rect = text_surface.get_rect(center=(50 + j * cell_size + cell_size // 2,
                                                          50 + i * cell_size + cell_size // 2))
                window.blit(text_surface, text_rect)


def mode1_window():
    pygame.init()
    WINDOW = pygame.display.set_mode((640, 680))
    pygame.display.set_caption("Sudoku Solver")

    def generate_new_puzzle(difficulty_level):
        puzzle = generate_random_puzzle(difficulty_level)
        return puzzle
    
    def solve_puzzle(puzzle):
        return solve_sudoku(puzzle.grid)

    difficulty_level = 3 # 3 -> EASY      2 -> MEDIUM    1 -> HARD
    current_puzzle = generate_new_puzzle(difficulty_level) 
    generate_button = Button(50, 600, 350, 60, "Generate Puzzle", GRAY, RED, generate_new_puzzle)
    solve_button = Button(440, 600, 150, 60, "Solve", GRAY, RED, solve_sudoku)  # Placeholder lambda for now

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if generate_button.is_hovered(pos):
                        current_puzzle = generate_new_puzzle(difficulty_level)
                    elif solve_button.is_hovered(pos):
                        current_puzzle = solve_puzzle(current_puzzle)

        WINDOW.fill(WHITE)

        # Draw Sudoku grid
        draw_sudoku_grid(WINDOW, current_puzzle.grid)

        # Draw buttons
        generate_button.draw(WINDOW, generate_button.is_hovered(pygame.mouse.get_pos()))
        solve_button.draw(WINDOW, solve_button.is_hovered(pygame.mouse.get_pos()))

        pygame.display.update()


def mode2_window():
    pygame.init()
    WINDOW = pygame.display.set_mode((640, 680))
    pygame.display.set_caption("Sudoku Solver")

    def generate_empty_puzzle():
        puzzle = Board()
        puzzle.grid = puzzle.generate_empty_sudoko()
        return puzzle
    
    def solver(current_puzzle):
        # First, check validity
        if not is_valid_sudoku(current_puzzle.grid):
            print("Invalid Puzzle")
            # Reset the puzzle
            return generate_empty_puzzle()
        
        # Solve the puzzle
        solved_puzzle = solve_sudoku(current_puzzle.grid)
        if solved_puzzle is None:
            print("Unsolvable Puzzle")
        else:
            print("Puzzle Solved!")
            return solved_puzzle

    reset_button = Button(50, 600, 350, 60, "Reset Puzzle", GRAY, RED, generate_empty_puzzle)
    solve_button = Button(440, 600, 150, 60, "Solve", GRAY, RED, solver)
    current_puzzle = generate_empty_puzzle()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if reset_button.is_hovered(pos):
                        current_puzzle = generate_empty_puzzle()
                    elif solve_button.is_hovered(pos):
                        current_puzzle = solver(current_puzzle)
                    else:
                        x, y = pos[0], pos[1]
                        row = (y - 50) // 60
                        column = (x - 50) // 60
            elif event.type == pygame.KEYDOWN:
                if current_puzzle is not None:  # Check if puzzle exists
                    if event.key in range(pygame.K_1,
                                          pygame.K_9 + 1):  # Check if the pressed key is a number between 1 and 9
                        if row is not None and column is not None:  # Check if a cell is clicked
                            number = int(pygame.key.name(event.key))
                            current_puzzle.set_value(row, column, number)

        WINDOW.fill(WHITE)

        # Draw Sudoku grid
        draw_sudoku_grid(WINDOW, current_puzzle.grid)

        # Draw buttons
        reset_button.draw(WINDOW, reset_button.is_hovered(pygame.mouse.get_pos()))
        solve_button.draw(WINDOW, solve_button.is_hovered(pygame.mouse.get_pos()))

        pygame.display.update()

def mode3_window():
    pygame.init()
    WINDOW = pygame.display.set_mode((640, 680))
    pygame.display.set_caption("Interactive Game!")

    def generate_new_puzzle(difficulty_level):
        while True:
            puzzle = generate_random_puzzle(difficulty_level)
            with SuppressPrints():
                solved_puzzle = solve_sudoku(puzzle.grid)
            if solved_puzzle is not None:
                return puzzle

    def is_valid_input(row, col, num):
        # Get the solved puzzle using the solve_sudoku function
        with SuppressPrints():
            solved_puzzle = solve_sudoku(current_puzzle.grid)

        # Check if the user's input matches the corresponding cell in the solved puzzle
        if solved_puzzle is not None and solved_puzzle.get_value(row, col) == num:
            current_puzzle.set_value(row, col, num)
            return True
        else:
            print(f"Can't place {num} in ({row},{col}) as it is an invalid move!")
            return False

    difficulty_level = 3        # 3 -> EASY      2 -> MEDIUM    1 -> HARD
    generate_button = Button(120, 600, 400, 60, "Generate New Puzzle", GRAY, RED, generate_new_puzzle)
    current_puzzle = generate_new_puzzle(difficulty_level)
    selected_cell = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if generate_button.is_hovered(pos):
                        current_puzzle = generate_new_puzzle(difficulty_level)
                    else:
                        x, y = pos[0], pos[1]
                        row = (y - 50) // 60
                        column = (x - 50) // 60
                        selected_cell = (row, column)
            elif event.type == pygame.KEYDOWN:
                if selected_cell is not None and current_puzzle.get_value(selected_cell[0], selected_cell[1]) == 0:
                    if event.key in range(pygame.K_1, pygame.K_9 + 1):
                        number = int(pygame.key.name(event.key))
                        if is_valid_input(selected_cell[0], selected_cell[1], number):
                            selected_cell = None

        WINDOW.fill(WHITE)

        # Draw Sudoku grid
        draw_sudoku_grid(WINDOW, current_puzzle.grid)

        # Draw buttons
        generate_button.draw(WINDOW, generate_button.is_hovered(pygame.mouse.get_pos()))

        pygame.display.update()

mode1_button = Button(100, 150, 350, 60, "Mode 1: AI Solver", GRAY, RED, mode1_window)
mode2_button = Button(100, 250, 350, 60, "Mode 2: User Input", GRAY, RED, mode2_window)
mode3_button = Button(70, 350, 430, 60, "Mode 3: Interactive Game", GRAY, RED, mode3_window)
exit_button = Button(150, 450, 240, 60, "Exit", GRAY, RED, sys.exit)

buttons = [mode1_button, mode2_button, mode3_button, exit_button]


def draw_start_menu():
    WINDOW.blit(background_image, (0, 0))  # Draw background image
    for button in buttons:
        hovered = button.is_hovered(pygame.mouse.get_pos())  # Check if the button is being hovered over
        button.draw(WINDOW, hovered)  # Pass the hovered state to the draw method


def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    for button in buttons:
                        if button.is_hovered(pos):
                            button.action()

        draw_start_menu()
        pygame.display.update()


if __name__ == "__main__":
    main()
