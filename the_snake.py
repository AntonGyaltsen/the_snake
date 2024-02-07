from random import choice, randint

import pygame

# Инициализация PyGame:
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
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    def __init__(self, body_color, position=((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))):
        self.body_color = body_color
        self.position = position

    def draw(self, surface):
        pass


class Apple(GameObject):
    def __init__(self):
        # Имя атрибута в super() не нужно, потому что в суперклассе только один недефолтный параметр.
        super().__init__(APPLE_COLOR)
        self.position = self.randomize_position()

    def randomize_position(self):
        x = randint(0, (SCREEN_WIDTH // GRID_SIZE) - 1) * GRID_SIZE
        y = randint(0, (SCREEN_HEIGHT // GRID_SIZE) - 1) * GRID_SIZE
        return x, y

    # Метод draw класса Apple
    def draw(self, surface):
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

class Rock(GameObject):
    def __init__(self):
        # Имя атрибута в super() не нужно, потому что в суперклассе только один недефолтный параметр.
        super().__init__(ROCK_COLOR)
        self.position = self.randomize_position()

    def randomize_position(self):
        x = randint(0, (SCREEN_WIDTH // GRID_SIZE) - 1) * GRID_SIZE
        y = randint(0, (SCREEN_HEIGHT // GRID_SIZE) - 1) * GRID_SIZE
        return x, y

        # Метод draw класса Rock

    def draw(self, surface):
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

class WrongFood(GameObject):
    def __init__(self):
        # Имя атрибута в super() не нужно, потому что в суперклассе только один недефолтный параметр.
        super().__init__(FOOD_COLOR)
        self.position = self.randomize_position()

    def randomize_position(self):
        x = randint(0, (SCREEN_WIDTH // GRID_SIZE) - 1) * GRID_SIZE
        y = randint(0, (SCREEN_HEIGHT // GRID_SIZE) - 1) * GRID_SIZE
        return x, y

        # Метод draw класса WrongFood

    def draw(self, surface):
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    def __init__(self, positions=[((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))], length=1,
                 direction=RIGHT, next_direction=None, last=None):
        super().__init__(body_color=SNAKE_COLOR)
        self.positions: list = positions
        self.length: int = length
        self.direction: tuple = direction
        self.next_direction: tuple = next_direction
        self.last: tuple = last  # Позиция последнего элемента

        # Метод обновления направления после нажатия на кнопку

    def update_direction(self):
        if self.next_direction:
            self.direction: tuple = self.next_direction
            self.next_direction = None

    def get_head_position(self) -> tuple:
        return self.positions[0]

    def move(self):
        # Возвращает кортеж, представляющий позицию головы, например (180, 140).
        current_head_position: tuple = self.get_head_position()
        dx, dy = self.direction
        # Например, одно движение вправо это (1, 0), то есть для x смещение будет 20. При x = 640, 640 % 640 = 0
        # то есть змейка появится слева. Аналогично с y. current_head_position[0] извлекает x-координату из кортежа.
        # new_head_position тоже кортеж (x, y)
        new_head_position: tuple = ((current_head_position[0] + dx * GRID_SIZE) % SCREEN_WIDTH,
                                    (current_head_position[1] + dy * GRID_SIZE) % SCREEN_HEIGHT)

        # Проверка на коллизию
        if new_head_position in self.positions[2:]:
            self.reset()
        self.positions.insert(0, new_head_position)

        # Проверка на движение или поглощение яблока. При поглощении яблока length увеличивается
        # и тогда хвост оставляется. self.last получает значение для передачи в метод затирания последнего элемента.
        if len(self.positions) > self.length:
            self.last = self.positions.pop()



    # Метод draw класса Snake
    def draw(self, surface):
        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)
        for position in self.positions:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    # Сброс змейки в начальное состояние
    def reset(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = choice(directions)
        screen.fill(BOARD_BACKGROUND_COLOR)


def main():
    # Тут нужно создать экземпляры классов.
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

        # Функция обработки действий пользователя
        def handle_keys(snake):
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

        # Тут опишите основную логику игры.

        handle_keys(snake)

        # Обновление направления движения змейки.
        snake.update_direction()
        # Само движение.
        snake.move()

        # Проверка на поглощение яблока, столкновение с собой или с камнем.
        if snake.positions[0] == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position()
        elif snake.positions[0] in snake.positions[2:]:
            snake.reset()
        elif snake.positions[0] == rock.position:
            snake.reset()
            rock.position = rock.randomize_position()
        elif snake.positions[0] == junkfood.position:
            if len(snake.positions) > 1: # Проверяем сколько сегментов у змеи
                snake.length -= 1
                junkfood.position = junkfood.randomize_position()
                snake.last = snake.positions.pop()
            else: # Сброс если сегмент только один
                snake.reset()


        pygame.display.update()



if __name__ == '__main__':
    main()
