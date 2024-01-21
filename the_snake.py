from random import randint

import pygame as pg

# Инициализация PyGame:
pg.init()

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

# Задаем позицию игрового объекта.
POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Направления движений.
KEYBOARD = {
    (LEFT, pg.K_UP): UP,
    (RIGHT, pg.K_UP): UP,
    (UP, pg.K_LEFT): LEFT,
    (DOWN, pg.K_LEFT): LEFT,
    (UP, pg.K_RIGHT): RIGHT,
    (DOWN, pg.K_RIGHT): RIGHT,
    (LEFT, pg.K_DOWN): DOWN,
    (RIGHT, pg.K_DOWN): DOWN
}


class GameObject:
    """Базовый класс для инициализации и наследования игровых объектов."""

    # Конструкор класса инициализирует игровой объект.
    # Также будет использован в дочерник классах.
    def __init__(self, body_color=BORDER_COLOR):
        self.position = POSITION
        self.body_color = body_color

    def create_rect(self, position, body_color=APPLE_COLOR):
        """Отрисоывает одну ячейку для игровых объектов."""
        rect = pg.Rect(
            position,
            (GRID_SIZE, GRID_SIZE)
        )
        pg.draw.rect(screen, body_color, rect)
        return rect

    def draw(self, surface):
        """
        Абстрактный метод, который предназначен
        для переопределения в дочерних классах.
        """
        raise NotImplementedError('Метод для реализации в дочерних классах.')


class Apple(GameObject):
    """
    Дочерний класс, который инициализирует игровой объект:
    задает позицию, цвет и отрисовывает на игровом поле 'яблоко'.
    """

    def __init__(self, body_color=APPLE_COLOR):
        super().__init__(body_color)
        self.randomize_position()  # Позиция яблока на игровом поле.

    def randomize_position(self, occupied_cells=POSITION):
        """
        Метод устанавливает случайное положение яблока на игровом
        поле — задаёт атрибуту position новое значение.
        Координаты выбираются так,чтобы яблоко оказалось
        в пределах игрового поля.
        """
        # Пока яблоко появляется в координатах сегментов змейки -
        # цикл продолжается.
        while self.position in occupied_cells:
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self, surface):
        """
        Метод отрисовывает объект 'яблоко' на игровом интерфейсе
        и закрашивает края.
        """
        rect = self.create_rect(self.position)
        pg.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """
    Дочерний класс Snake используется для создания игрового объекта.

    Основное применение:
    создает объект "Змейка",
    задает цвет, длину, позицию, направление и
    дополняется секциями для увелечения размера объекта.
    """

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color)
        self.reset()

    def update_direction(self):
        """Метод обновленяет направление после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """
        Обновляет позицию змейки (координаты каждой секции),
        добавляя новую голову в начало списка positions
        и удаляя последний элемент,
        если длина змейки не увеличилась.
        """
        head = self.get_head_position()  # Текущая позиция головы змейки.
        new_x = head[0] + self.direction[0] * GRID_SIZE  # Новая ось x.
        new_y = head[1] + self.direction[1] * GRID_SIZE  # Новая ось y.
        # Новая позиция головы с учетом обработки краев экрана.
        next_position = (new_x % SCREEN_WIDTH,
                         new_y % SCREEN_HEIGHT)

        # Обновляем список секций змейки.
        self.positions.insert(0, next_position)
        if len(self.positions) > self.length:  # Проверка на съеденное яблоко.
            # Если яблоко не съедено - затираем последний элемент.
            self.last = self.positions.pop()
        else:
            self.last = 0  # Увеличиваем змейку на одну сейкцию.

    def draw(self, surface):
        """Метод  отрисовывает змейку на экране, затирая след."""
        # Отрисовка головы змейки
        rect = self.create_rect(self.get_head_position(), self.body_color)
        pg.draw.rect(surface, BORDER_COLOR, rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = self.create_rect(self.last, self.body_color)
            pg.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """
        Возвращает позицию головы змейки
        (первый элемент в списке positions)
        """
        return self.positions[0]

    def reset(self):
        """
        Сбрасывает змейку в начальное состояние
        после столкновения с собой.
        """
        self.length = 1  # Длина змейки.

        # Список, содержащий позиции всех сегментов тела змейки.
        self.positions = [self.position]

        # Направление движения змейки. По умолчанию змейка движется вправо.
        self.direction = RIGHT

        # Следующее направление движения,
        # которое будет применено после обработки нажатия клавиши.
        self.next_direction = None


def handle_keys(game_object):
    """
    Обрабатывает нажатия клавиш,
    чтобы изменить направление движения змейки.
    """
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            key = KEYBOARD.get(
                (game_object.direction, event.key), game_object.direction
            )
            game_object.next_direction = key


def main():
    """
    Обновляет состояние объектов: змейка обрабатывает нажатия клавиш
    и двигается в соответствии с выбранным направлением.
    Если съедено яблоко, змейка увеличивается на один сегмент.
    """
    # Тут создаем экземпляры класса.
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)

        # Тут описываем логику игры.
        handle_keys(snake)  # Обрабатываем нажатие клавиш.
        snake.update_direction()  # Обновляем направление.
        snake.move()  # Перемещаем в выбранное направление.
        apple.draw(screen)  # Отрисовывем яблоко.
        snake.draw(screen)  # Отрисовывем змейку.
        # Проверяем на съедение яблока змейкой.
        if apple.position == snake.get_head_position():
            apple.randomize_position(snake.positions)
            snake.length += 1
        if snake.get_head_position() in snake.positions[2:]:
            snake.reset()  # Проверяем на столкновение змейки с собой.
            screen.fill(BOARD_BACKGROUND_COLOR)
        # Обновляет игровое поле на экране пользователя.
        pg.display.update()


if __name__ == '__main__':
    main()
