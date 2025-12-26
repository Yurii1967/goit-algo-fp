# Дерево Піфагора
import turtle
import math


def pythagoras_tree(t: turtle.Turtle, x: float, y: float, angle: float, side: float, level: int):
    """
    Малює "Дерево Піфагора" рекурсивно.
    Кожен крок: квадрат + 2 квадрати-діти під кутами 45° і 45° (класична версія).
    """
    if level == 0 or side < 1:
        return

    # Перейти в точку (x, y), встановити кут
    t.penup()
    t.goto(x, y)
    t.setheading(angle)
    t.pendown()

    # Намалювати квадрат зі стороною side
    for _ in range(4):
        t.forward(side)
        t.left(90)

    # Обчислення ключових точок
    # Стартова точка (x,y) — нижній лівий кут квадрата (за напрямом angle)
    # Після квадрату нам потрібні координати верхніх кутів.
    # Вектор "вправо" (вздовж нижньої сторони) та "вгору" (перпендикуляр)
    rad = math.radians(angle)
    ux, uy = math.cos(rad), math.sin(rad)              # одиничний вектор вправо
    vx, vy = -math.sin(rad), math.cos(rad)             # одиничний вектор вгору

    # Верхній лівий кут (x + v*side)
    top_left = (x + vx * side, y + vy * side)
    # Верхній правий кут (x + u*side + v*side)
    top_right = (x + ux * side + vx * side, y + uy * side + vy * side)

    # Довжина сторін дочірніх квадратів для кута 45°:
    child_side = side / math.sqrt(2)

    # Лівий дочірній квадрат "росте" з top_left під кутом angle + 45
    pythagoras_tree(
        t,
        x=top_left[0],
        y=top_left[1],
        angle=angle + 45,
        side=child_side,
        level=level - 1
    )

    # Правий дочірній квадрат "росте" з точки, яка лежить на "дахові":
    # У класичній побудові правий квадрат стартує не з top_right, а з вершини трикутника.
    # Але для простої/красивої версії часто використовують старт з top_right.
    # Це дає симпатичне дерево та чітку рекурсію.
    pythagoras_tree(
        t,
        x=top_right[0],
        y=top_right[1],
        angle=angle - 45,
        side=child_side,
        level=level - 1
    )


def main():
    try:
        level = int(input("Введіть рівень рекурсії (наприклад 1..12): ").strip())
    except ValueError:
        print("Потрібно ввести ціле число.")
        return

    if level < 0:
        print("Рівень рекурсії має бути >= 0.")
        return

    screen = turtle.Screen()
    screen.title("Фрактал: Дерево Піфагора (рекурсія)")
    screen.setup(width=1000, height=800)
    screen.tracer(0)  # прискорення (малюємо без анімації)

    t = turtle.Turtle(visible=False)
    t.speed(0)
    t.pensize(1)

    # Початкові параметри
    start_side = 140
    start_x = -start_side / 2
    start_y = -300
    start_angle = 0  # квадрат стоїть горизонтально

    pythagoras_tree(t, start_x, start_y, start_angle, start_side, level)

    screen.update()
    screen.mainloop()


if __name__ == "__main__":
    main()
