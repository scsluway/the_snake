# Из модуля random импортируем функцию randint
# для расположения, в случайном порядке, иговых объектов.
from random import randint

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
    """Базовый класс для инициализации и наследования игровых объектов."""

    # Задаем позицию игрового объекта.
    position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    # Конструкор класса инициализирует игровой объект.
    # Также будет использован в дочерник классах.
    def __init__(self, body_color=(0, 0, 0), position=None):
        self.position = GameObject.position
        self.body_color = body_color

    def draw(self, surface):
        """
        Абстрактный метод, который предназначен
        для переопределения в дочерних классах.
        """
        pass


class Apple(GameObject):
    """
    Дочерний класс, который инициализирует игровой объект:
    задает позицию, цвет и отрисовывает на игровом поле 'яблоко'.
    """

    def __init__(self, body_color=APPLE_COLOR):
        super().__init__(body_color)
        self.randomize_position()  # Позиция яблока на игровом поле.
        self.body_color = APPLE_COLOR  # Цвет яблока.

    def randomize_position(self):
        """
        Метод устанавливает случайное положение яблока на игровом
        поле — задаёт атрибуту position новое значение.
        Координаты выбираются так,чтобы яблоко оказалось
        в пределах игрового поля.
        """
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self, surface):
        """
        Метод отрисовывает объект 'яблоко' на игровом интерфейсе
        и закрашивает края.
        """
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


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
        self.length = 1  # Длина змейки.

        # Список, содержащий позиции всех сегментов тела змейки.
        self.positions = [Snake.position]

        # Направление движения змейки. По умолчанию змейка движется вправо.
        self.direction = RIGHT

        # Следующее направление движения,
        # которое будет применено после обработки нажатия клавиши.
        self.next_direction = None

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
        # Определяю перменную, которая принимает новые координаты xd, yd.
        next_position = tuple(
            map(sum, zip(self.get_head_position(),
                         tuple(map(lambda x: x * 20, self.direction))))
        )
        # Переменная содержит обработку краев экрана.
        next_position = (
            next_position[0] % SCREEN_WIDTH, next_position[1] % SCREEN_HEIGHT
        )
        # Обновляем список секций змейки.
        self.positions.insert(0, next_position)
        if len(self.positions) > self.length:  # Проверка на съеденное яблоко.
            # Если яблоко не съедено - затираем последний элемент.
            self.last = self.positions.pop()
        else:
            self.last = 0  # Увеличиваем змейку на одну сейкцию.

    def draw(self, surface):
        """Метод  отрисовывает змейку на экране, затирая след."""
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """
        Возвращает позицию головы змейки
        (первый элемент в списке positions)
        """
        return self.positions[0]

    def reset(self, surface):
        """
        Сбрасывает змейку в начальное состояние
        после столкновения с собой.
        """
        # Проверка на совпадение координат головы
        # змейки с координатами каждой секции.
        if self.get_head_position() in self.positions[1:]:
            # Закрашиваем поле в цвет по умолчанию.
            last_rect = pygame.Rect(
                (0, 0),
                (SCREEN_WIDTH, SCREEN_HEIGHT)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)
            self.__init__()  # Переинициализируем змейку.


def handle_keys(game_object):
    """
    Обрабатывает нажатия клавиш,
    чтобы изменить направление движения змейки.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            # Определяем переменную как словарь.
            # Ключами являются числа, привязанные к клавишам клавиатуры.
            # Значения - кортежи направления движения.
            dict_keyboard = {
                f'{pygame.K_UP}': (UP, DOWN),
                f'{pygame.K_DOWN}': (DOWN, UP),
                f'{pygame.K_LEFT}': (LEFT, RIGHT),
                f'{pygame.K_RIGHT}': (RIGHT, LEFT)
            }
            # Переменная key принимает кортеж, если число нажатой кнопки
            # совпадает с ключем словоря, иначе получаем исходное направление.
            key = dict_keyboard.get(f'{event.key}', game_object.direction)
            # Проверяем является ли переменная key кортежем.
            if not isinstance(key[0], int) and game_object.direction != key[1]:
                # Перезаписываем направление движеиня.
                game_object.next_direction = key[0]


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
        snake.draw(screen)  # Отрисовывем змейку.
        apple.draw(screen)  # Отрисовывем яблоко.
        # Проверяем на съедение яблока змейкой.
        if apple.position == snake.get_head_position():
            apple_not_in_snake = True
            # Пока яблоко появляется в координатах сегментов змейки -
            # цикл продолжается.
            while apple_not_in_snake:
                apple.randomize_position()
                if apple.position not in snake.positions:
                    apple_not_in_snake = False
            snake.length += 1
        snake.reset(screen)  # Проверяем на столкновение змейки с собой.
        # Обновляет игровое поле на экране пользователя.
        pygame.display.update()


if __name__ == '__main__':
    main()
