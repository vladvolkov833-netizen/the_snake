
from random import randint

import pygame

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

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Экран объекта"""

    def __init__(self, position=None, body_color=None):
        """Инициализация объекта на поле."""
        self.position = position or (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = body_color or (255, 255, 255)

    def draw(self, surface: pygame.Surface):
        """Абстрактный метод для отрисовки объекта на экран."""
        pass

    def draw_cell(self, surface, position, color=None):
        """Отрисовывает ячейку на экран."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, color or self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Яблоко"""

    def __init__(self):
        """Инициализирует яблоко на игровом поле."""
        super().__init__(None, APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Установка случайного положения яблока на игровом поле."""
        self.position = (
            randint(0, SCREEN_WIDTH // GRID_SIZE - 1) * GRID_SIZE,
            randint(0, SCREEN_HEIGHT // GRID_SIZE - 1) * GRID_SIZE
        )

    def draw(self, surface):
        """Отрисовывает яблоко на поверхности."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Описание змейки."""

    def __init__(self):
        """Инициализирует начальное состояние змейки."""
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        super().__init__((center_x, center_y), SNAKE_COLOR)
        self.length = 2
        self.positions = [self.position]
        self.direction = LEFT
        self.next_direction = None

    def update_direction(self, new_direction):
        """Обновляет направление движения змейки."""
        if new_direction != (-self.direction[0], -self.direction[1]):
            self.next_direction = new_direction

    def move(self):
        """Обновляем местоположение змейки"""
        curnt_head_position = self.positions[0]
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None
        """ Рассчитываем новую позицию головы змейки"""

        x, y = self.direction
        new_head_x = (curnt_head_position[0] + (x * GRID_SIZE)) % SCREEN_WIDTH
        new_head_y = (curnt_head_position[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT
        new_head = (new_head_x, new_head_y)

        if len(self.positions) > 2 and new_head in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new_head)
            if len(self.positions) > self.length:
                self.positions.pop()

    def draw(self, surface):
        """Отрисовывает змейку на экране и убирает след."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

    def get_head_position(self):
        """Возвращает позицию головы змейки"""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние и продолжает игру ."""
        self.length = 1
        self.positions = [self.position]
        self.direction = LEFT
        self.next_direction = None


def main():
    """Основной цикл игры."""
    snake = Snake()
    apple = Apple()

    running = True
    while running:
        clock.tick(SPEED)
        handle_keys(snake)

        # Обновление позиции змеи
        snake.move()
        """Проверка столкновения с яблоком"""

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple = Apple()  # Создаём новое яблоко

        """Очистка экрана и отрисовка объектов"""

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw(screen)
        snake.draw(screen)

        pygame.display.update()


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш для управления змейкой."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


if __name__ == "__main__":
    main()
