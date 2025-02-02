Here's the improved version of the code:

```python
import random
import pygame
import sys

# Initialize Pygame
pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Set the width and height of each block
BLOCK_SIZE = 30

# Set the width and height of the grid
GRID_WIDTH = 10
GRID_HEIGHT = 20

# Set the margin between the grid and the border
MARGIN = 20

# Set the size of the screen
SCREEN_WIDTH = GRID_WIDTH * BLOCK_SIZE + 2 * MARGIN
SCREEN_HEIGHT = GRID_HEIGHT * BLOCK_SIZE + 2 * MARGIN

# Create the screen
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set the font for the score
FONT = pygame.font.Font(None, 36)

# Define the shapes of the blocks
SHAPES = [
    [[1, 1, 1, 1]],  # Straight block
]

# Define the colors of the blocks
BLOCK_COLORS = [
    (255, 0, 0),  # Red
    (0, 255, 0),  # Green
    (0, 0, 255),  # Blue
    (255, 255, 0),  # Yellow
    (255, 0, 255),  # Magenta
    (0, 255, 255),  # Cyan
]

class Block:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(BLOCK_COLORS)
        self.x = GRID_WIDTH // 2
        self.y = 0

    def move_down(self):
        self.y += 1

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1

    def move_up(self):
        self.y -= 1

    def rotate(self):
        self.shape = [list(reversed(i)) for i in zip(*self.shape)]

class Game:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.block = Block()
        self.score = 0
        self.lines_cleared = 0
        self.game_over = False

    def draw_grid(self):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x] == 1:
                    pygame.draw.rect(SCREEN, WHITE, (x * BLOCK_SIZE + MARGIN, y * BLOCK_SIZE + MARGIN, BLOCK_SIZE, BLOCK_SIZE))

    def draw_block(self):
        for y, row in enumerate(self.block.shape):
            for x, val in enumerate(row):
                if val == 1:
                    pygame.draw.rect(SCREEN, self.block.color, ((self.block.x + x) * BLOCK_SIZE + MARGIN, (self.block.y + y) * BLOCK_SIZE + MARGIN, BLOCK_SIZE, BLOCK_SIZE))

    def check_collision(self):
        for y, row in enumerate(self.block.shape):
            for x, val in enumerate(row):
                if val == 1:
                    if self.block.x + x < 0 or self.block.x + x >= GRID_WIDTH:
                        return True
                    if self.block.y + y < 0 or self.block.y + y >= GRID_HEIGHT:
                        return True
                    if self.grid[self.block.y + y][self.block.x + x] == 1:
                        return True
        return False

    def update_grid(self):
        for y, row in enumerate(self.block.shape):
            for x, val in enumerate(row):
                if val == 1:
                    self.grid[self.block.y + y][self.block.x + x] = 1

    def clear_lines(self):
        lines_cleared = 0
        for y in range(GRID_HEIGHT):
            if all(self.grid[y]):
                del self.grid[y]
                self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
                lines_cleared += 1
        self.score += lines_cleared * lines_cleared
        self.lines_cleared += lines_cleared
        print(f"Line cleared! You cleared {lines_cleared} lines.")

    def draw_score(self):
        score_text = FONT.render(f'Score: {self.score} Lines Cleared: {self.lines_cleared}', True, WHITE)
        SCREEN.blit(score_text, (MARGIN, MARGIN))

    def check_game_over(self):
        for x in range(GRID_WIDTH):
            if self.grid[0][x] == 1:
                self.game_over = True
                print("Game Over!")

def main():
    clock = pygame.time.Clock()
    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.block.move_left()
                    if game.check_collision():
                        game.block.move_right()
                elif event.key == pygame.K_RIGHT:
                    game.block.move_right()
                    if game.check_collision():
                        game.block.move_left()
                elif event.key == pygame.K_DOWN:
                    game.block.move_down()
                    if game.check_collision():
                        game.block.move_up()
                elif event.key == pygame.K_UP:
                    game.block.move_up()
                    if game.check_collision():
                        game.block.move_down()
                elif event.key == pygame.K_SPACE:
                    game.block.rotate()
                    if game.check_collision():
                        game.block.rotate()
                        game.block.rotate()
                        game.block.rotate()

        SCREEN.fill(BLACK)

        game.draw_grid()
        game.draw_block()
        game.draw_score()

        if game.check_collision():
            game.update_grid()
            game.clear_lines()
            game.block = Block()

        game.block.move_down()
        if game.check_collision():
            game.block.move_up()

        game.check_game_over()
        if game.game_over:
            game_over_text = FONT.render('Game Over', True, WHITE)
            SCREEN.blit(game_over_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 18))
            pygame.display.flip()
            pygame.time.wait(2000)
            break

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()
```

The task description is: Create a basic tetris game with only straight blocks. Implementation requirements: Design a Tetris game board with falling straight blocks. Allow the player to move blocks left, right, and down, and rotate them. Clear lines when they are completely filled. Track and display the player's score. Based on this task description, I have improved the solution.