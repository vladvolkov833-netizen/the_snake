from random import randint

import pygame as pg

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

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс для всех объектов игры."""

    def __init__(self, body_color=SNAKE_COLOR):
        """Инициализирует объект игры."""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = body_color

    def draw(self):
        """Абстрактный метод для отрисовки объекта на экран."""

    def draw_cell(self, position, color=None):
        """Отрисовывает ячейку на экран."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color or self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Яблоко"""

    def __init__(self, taken_positions=[]):
        """Инициализирует яблоко на игровом поле."""
        super().__init__(APPLE_COLOR)
        self.randomize_position(taken_positions or [])

    def randomize_position(self, taken_positions):
        """Установка случайного положения яблока на игровом поле."""
        while True:
            self.position = (
                randint(0, SCREEN_WIDTH // GRID_SIZE - 1) * GRID_SIZE,
                randint(0, SCREEN_HEIGHT // GRID_SIZE - 1) * GRID_SIZE
            )
            if self.position not in taken_positions:
                break

    def draw(self, screen):
        """Отрисовывает яблоко на поверхности."""
        self.draw_cell(self.position, self.body_color)


class Snake(GameObject):
    """Описание змейки."""

    def __init__(self):
        """Инициализирует начальное состояние змейки."""
        super().__init__(SNAKE_COLOR)
        self.reset()

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def move(self):
        """Обновляем местоположение змейки."""
        head_x, head_y = self.get_head_position()

        self.position = (
            (head_x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        )

    # Обновление позиций
        self.positions.insert(0, self.position)
        if len(self.positions) > self.length:
            last_position = self.positions.pop()
            self.draw_cell(last_position, BOARD_BACKGROUND_COLOR)
        else:
            last_position = None

    def draw(self, screen):
        """Отрисовывает змейку на экране и убирает след."""
        for position in self.positions:
            self.draw_cell(position, self.body_color)

    def reset(self):
        """Сбрасывает змейку в начальное состояние и продолжает игру."""
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None

    def update_direction(self, new_direction):
        """Обновляет направление движения змеи."""
        self.direction = new_direction


def main():
    """Основной цикл игры."""
    snake = Snake()
    apple = Apple(snake.positions)
    while True:
        clock.tick(SPEED)
        handle_keys(snake)

        # Обновление позиции змейки
        snake.move()

        # Проверка столкновения со яблоком
        if snake.get_head_position() == apple.position:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.length += 1
            apple.randomize_position(snake.positions)

        # Проверка на столкновение со своим телом
        elif snake.get_head_position() in snake.positions[2:]:
            snake.reset()
            apple.randomize_position(snake.positions)

        # Отрисовка объектов
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw(screen)
        snake.draw(screen)
        pg.display.update()


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш для управления змейкой."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.direction = RIGHT


if __name__ == '__main__':
    main()
