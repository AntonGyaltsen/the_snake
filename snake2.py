from random import choice, randint
import pygame

# Initialization of PyGame:
pygame.init()

# Constants for screen and grid sizes:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Movement directions:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Colors:
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Snake speed:
SPEED = 10

# List for random direction selection in reset():
directions = [UP, DOWN, LEFT, RIGHT]

# Setting up the game window:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Snake Game')

# Clock setup:
clock = pygame.time.Clock()

# Game object classes:
class GameObject:
    def __init__(self, body_color, position=((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))):
        self.body_color = body_color
        self.position = position

    def draw(self, surface):
        pass

class Apple(GameObject):
    def __init__(self):
        super().__init__(APPLE_COLOR)
        self.position = self.randomize_position()

    def randomize_position(self):
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        return x, y

    def draw(self, surface):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

class Snake(GameObject):
    def __init__(self):
        super().__init__(body_color=SNAKE_COLOR, position=[(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)])
        self.positions = [self.position]
        self.length = 1
        self.direction = choice(directions)
        self.next_direction = None

    def update_direction(self):
        if self.next_direction and self.next_direction != (-self.direction[0], -self.direction[1]):
            self.direction = self.next_direction
        self.next_direction = None

    def move(self):
        x, y = self.direction
        new_head = ((self.positions[0][0] + (x * GRID_SIZE)) % SCREEN_WIDTH,
                    (self.positions[0][1] + (y * GRID_SIZE)) % SCREEN_HEIGHT)
        if new_head in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new_head)
            if len(self.positions) > self.length:
                self.positions.pop()

    def grow(self):
        self.length += 1

    def reset(self):
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.length = 1
        self.direction = choice(directions)

    def draw(self, surface):
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

# Main game function:
def main():
    snake = Snake()
    apple = Apple()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != DOWN:
                    snake.next_direction = UP
                elif event.key == pygame.K_DOWN and snake.direction != UP:
                    snake.next_direction = DOWN
                elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                    snake.next_direction = LEFT
                elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                    snake.next_direction = RIGHT

        snake.update_direction()
        snake.move()

        if snake.positions[0] == apple.position:
            snake.grow()
            apple.position = apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.update()
        clock.tick(SPEED)

if __name__ == '__main__':
    main()
