import pygame
import sys
from backend import Board, generate_sudoku_puzzle

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


def draw_sudoku_grid(window, current_puzzle):
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
            if current_puzzle[i][j] != 0:
                text_surface = button_font.render(str(current_puzzle[i][j]), True, BLACK)
                text_rect = text_surface.get_rect(center=(50 + j * cell_size + cell_size // 2,
                                                          50 + i * cell_size + cell_size // 2))
                window.blit(text_surface, text_rect)


def mode1_window():
    pygame.init()
    WINDOW = pygame.display.set_mode((640, 680))
    pygame.display.set_caption("Sudoku Solver")

    def generate_new_puzzle():
        grid = generate_sudoku_puzzle()
        return grid

    generate_button = Button(50, 600, 350, 60, "Generate Puzzle", GRAY, RED, generate_new_puzzle)
    solve_button = Button(440, 600, 150, 60, "Solve", GRAY, RED, lambda: print("This will solve later"))
    current_puzzle = generate_new_puzzle()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if generate_button.is_hovered(pos):
                        current_puzzle = generate_new_puzzle()
                    elif solve_button.is_hovered(pos):
                        solve_button.action()

        WINDOW.fill(WHITE)

        # Draw Sudoku grid
        draw_sudoku_grid(WINDOW, current_puzzle)

        # Draw buttons
        generate_button.draw(WINDOW, generate_button.is_hovered(pygame.mouse.get_pos()))
        solve_button.draw(WINDOW, solve_button.is_hovered(pygame.mouse.get_pos()))

        pygame.display.update()


mode1_button = Button(100, 150, 350, 60, "Mode 1: AI Solver", GRAY, RED, mode1_window)
mode2_button = Button(100, 250, 350, 60, "Mode 2: User Input", GRAY, RED, lambda: print("Mode 2 selected"))
mode3_button = Button(70, 350, 430, 60, "Mode 3: Interactive Game", GRAY, RED, lambda: print("Mode 3 selected"))
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
