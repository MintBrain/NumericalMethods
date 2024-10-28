import matplotlib.pyplot as plt
import numpy as np


# ax3 + bx2 + cx + d = 0
class Solver:
    def __init__(self, a: float, b: float, c: float, d: float, precision: float = 0.01) -> None:
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.precision = precision

    def func(self, x: float) -> float:
        return self.a * x ** 3 + self.b*x**2 + self.c * x + self.d

    def bisection_method(self, a: float, b: float) -> float:
        if self.func(a) == 0:
            return a
        elif self.func(b) == 0:
            return b

        if self.func(a) * self.func(b) >= 0:
            raise ValueError("Функция должна менять знак на концах интервала [a, b].")

        while (b - a) / 2.0 > self.precision:
            midpoint = (a + b) / 2.0
            f_mid = self.func(midpoint)

            # Проверка, достигли ли мы корня с требуемой точностью
            if abs(f_mid) < self.precision:
                return midpoint

            # Определяем, в какой половине функции есть корень
            if self.func(a) * f_mid < 0:
                b = midpoint
            else:
                a = midpoint

        return (a + b) / 2.0

    def plot_function(self, a: float, b: float) -> None:
        # Создаем массив x в пределах от a до b
        x = np.linspace(a, b, 500)
        y = self.func(x)

        # Ищем корень для обозначения его на графике
        root = self.bisection_method(a, b)

        # Построение графика функции
        plt.plot(x, y, label=f'$f(x) = {self.a}x^3 + {self.b}x^2 + {self.c}x + {self.d}$')
        plt.axhline(0, color='black', linewidth=0.5)  # Ось X
        plt.axvline(0, color='black', linewidth=0.5)  # Ось Y

        # Обозначение найденного корня на графике
        plt.plot(root, self.func(root), 'ro', label=f'Root ≈ {root:.4f}')

        # Настройка графика
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.title('Graph of the function and the root found by Bisection Method')
        plt.legend()
        plt.grid(True)
        plt.show()


def get_parameters_from_input():
    def input_float(prompt: str) -> float:
        while True:
            try:
                return float(input(prompt))
            except ValueError:
                print("Ошибка: введите число.")

    print("Введите параметры для функции f(x) = ax^3 + bx^2 + cx + d.")
    a = input_float("Введите значение a: ")
    b = input_float("Введите значение b: ")
    c = input_float("Введите значение c: ")
    d = input_float("Введите значение d: ")
    precision = input_float("Введите точность (например, 0.001): ")

    print("\nВведите интервал для метода бисекции.")
    while True:
        left = input_float("Введите левую границу интервала a: ")
        right = input_float("Введите правую границу интервала b: ")
        if left >= right:
            print("Ошибка: левая граница должна быть меньше правой.")
        else:
            break

    return a, b, c, d, precision, left, right


if __name__ == '__main__':
    a, b, c, d, precision, left, right = get_parameters_from_input()
    solver = Solver(a, b, c, d, precision)

    try:
        root = solver.bisection_method(left, right)
        print(f"Найденный корень: {root}")
        solver.plot_function(left, right)
    except ValueError as e:
        print(f"Ошибка: {e}")


if __name__ == '__main__':
    solver = Solver(2, 2)
    solver.plot_function(-2, 2)


