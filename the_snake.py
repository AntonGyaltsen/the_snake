from random import choice, randint

import pygame

# Инициализация PyGame:
# @formatter:on
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет камня
ROCK_COLOR = (0, 0, 255)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Цвет джанк-фуд
FOOD_COLOR = (255, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Список для случайного выбора направления в методе reset()
directions = [UP, DOWN, LEFT, RIGHT]

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption("Змейка")

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Основной родительский класс, от которого наследуются остальные."""

    def __init__(self, body_color=BOARD_BACKGROUND_COLOR):
        self.body_color = body_color
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        """Инициализация атрибутов родительского класса"""

    def draw(self, surface):
        """Абстрактный метод отрисовки, который переопределяется
        в наследуемых игровых классах.
        """
        pass


class Apple(GameObject):
    """Игровой класс яблоко, наследуемый от родительского класса"""

    def __init__(self):
        """Имя атрибута в super() не нужно, потому что в суперклассе
        только один недефолтный параметр.
        """
        super().__init__(body_color=APPLE_COLOR)
        self.position = self.randomize_position()

    def randomize_position(self):
        """Метод для рандомизации позиции камня"""
        x = randint(0, (SCREEN_WIDTH // GRID_SIZE) - 1) * GRID_SIZE
        y = randint(0, (SCREEN_HEIGHT // GRID_SIZE) - 1) * GRID_SIZE
        return x, y

    def draw(self, surface):
        """Метод для отрисовки яблока"""
        rect = pygame.Rect((self.position[0], self.position[1]),
                           (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Rock(GameObject):
    """Игровой класс камень, наследуемый от родительского класса"""

    def __init__(self):
        """Имя атрибута в super() не нужно, потому что в суперклассе
        только один недефолтный параметр.
        """
        super().__init__(body_color=ROCK_COLOR)
        self.position = self.randomize_position()

    def randomize_position(self):
        """Метод для рандомизации позиции камня"""
        x = randint(0, (SCREEN_WIDTH // GRID_SIZE) - 1) * GRID_SIZE
        y = randint(0, (SCREEN_HEIGHT // GRID_SIZE) - 1) * GRID_SIZE
        return x, y

    def draw(self, surface):
        """Метод для отрисовки камня"""
        rect = pygame.Rect((self.position[0], self.position[1]),
                           (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class WrongFood(GameObject):
    """Игровой класс неправильная еда, наследуемый от родительского класса"""

    def __init__(self):
        """Имя атрибута в super() не нужно, потому что в суперклассе
        только один недефолтный параметр.
        """
        super().__init__(body_color=FOOD_COLOR)
        self.position = self.randomize_position()
        """Инициализация атрибутов наследуемого класса"""

    def randomize_position(self):
        """Метод для рандомизации позиции еды"""
        x = randint(0, (SCREEN_WIDTH // GRID_SIZE) - 1) * GRID_SIZE
        y = randint(0, (SCREEN_HEIGHT // GRID_SIZE) - 1) * GRID_SIZE
        return x, y

    def draw(self, surface):
        """Метод для отрисовки еды"""
        rect = pygame.Rect((self.position[0], self.position[1]),
                           (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Игровой класс змея, наследуемый от родительского класса"""

    def __init__(self):
        super().__init__(body_color=SNAKE_COLOR)
        self.reset()
        self.next_direction: tuple = None
        self.last: tuple = None  # Позиция последнего элемента
        """Инициализация атрибутов наследуемого класса"""

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку"""
        if self.next_direction:
            self.direction: tuple = self.next_direction
            self.next_direction = None

    def get_head_position(self) -> tuple:
        """Метод для получения позиции головы"""
        return self.positions[0]

    def move(self):
        """Основной метод движения"""
        current_head_position: tuple = self.get_head_position()
        dx, dy = self.direction
        new_head_position: tuple = (
            (current_head_position[0] + dx * GRID_SIZE) % SCREEN_WIDTH,
            (current_head_position[1] + dy * GRID_SIZE) % SCREEN_HEIGHT,
        )

        if new_head_position in self.positions[2:]:
            self.reset()
        self.positions.insert(0, new_head_position)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self, surface):
        """Метод draw класса Snake"""
        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)
        for position in self.positions:
            rect = pygame.Rect((position[0], position[1]),
                               (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]), (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Сброс змейки в начальное состояние"""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice(directions)
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(gameobject):
    """Обработка нажатия клавиш"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and gameobject.direction != DOWN:
                gameobject.next_direction = UP
            elif event.key == pygame.K_DOWN and gameobject.direction != UP:
                gameobject.next_direction = DOWN
            elif event.key == pygame.K_LEFT and gameobject.direction != RIGHT:
                gameobject.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and gameobject.direction != LEFT:
                gameobject.next_direction = RIGHT


def main():
    """Основная функция игры с вечным циклом"""
    snake = Snake()
    apple = Apple()
    rock = Rock()
    junkfood = WrongFood()

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        rock.draw(screen)
        junkfood.draw(screen)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.positions[0] == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position()
        elif snake.positions[0] in snake.positions[2:]:
            snake.reset()
        elif snake.positions[0] == rock.position:
            snake.reset()
            rock.position = rock.randomize_position()
        elif snake.positions[0] == junkfood.position:
            if len(snake.positions) > 1:
                snake.length -= 1
                junkfood.position = junkfood.randomize_position()
                snake.last = snake.positions.pop()
            else:
                snake.reset()

        pygame.display.update()


if __name__ == "__main__":
    main()
