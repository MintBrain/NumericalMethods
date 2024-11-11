import matplotlib.pyplot as plt
import numpy as np
from prettytable import PrettyTable
import matplotlib

# matplotlib.use("TkAgg")


def midpoint_of_interval(a: float, b: float) -> float:
    return (a + b) / 2.0


class Func:
    def __init__(self, a: float, b: float, c: float, d: float):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.check()

    def check(self):
        # Проверка, что a не равно 0
        if self.a == 0:
            raise ValueError("Коэффициент 'a' не может быть равен нулю для кубического уравнения.")

        # Проверка на бесконечные значения
        if (self.a == float('inf') or self.a == float('-inf') or
            self.b == float('inf') or self.b == float('-inf') or
            self.c == float('inf') or self.c == float('-inf') or
            self.d == float('inf') or self.d == float('-inf')):
            raise ValueError("Коэффициенты не могут быть бесконечными.")

    def __call__(self, x: float) -> float:
        """Вычисление значения функции f(x) = ax^3 + bx^2 + cx + d."""
        return (self.a * pow(x, 3)) + (self.b * pow(x, 2)) + (self.c * x) + self.d

    def derivative(self, x: float) -> float:
        """Вычисление значения производной f'(x) = 3ax^2 + 2bx + c."""
        return (3 * self.a * pow(x, 2)) + (2 * self.b * x) + self.c

    def derivative2(self, x: float) -> float:
        """Вычисление значения производной f''(x) = 6ax + 2b."""
        return (6 * self.a * x) + (2 * self.b)


class Solver:
    def __init__(self, func: Func, precision: float = 0.01) -> None:
        self.func = func
        self.precision = precision

    def bisection_method(self, a: float, b: float, max_iterations=1000) -> float:
        print(f'Вычисление методом деления отрезка пополам')
        if self.func(a) == 0:
            print(f'a = {a} - корень уравнения')
            return a
        elif self.func(b) == 0:
            print(f'b = {b} - корень уравнения')
            return b

        if self.func(a) * self.func(b) >= 0:
            print("Функция должна менять знак на концах интервала [a, b].")
            return 0

        counter = 0
        _root = 0
        t = PrettyTable(['Iteration', 'a', 'b', 'midpoint', 'F(mid)', 'precision'])
        while True:
            precision = (b - a) / 2.0
            midpoint = midpoint_of_interval(a, b)
            f_mid = self.func(midpoint)

            t.add_row([counter, a, b, midpoint, f_mid, precision])

            if f_mid == 0 or precision <= self.precision:
                _root = midpoint
                break

            if self.func(a) * f_mid < 0: # Определяем, в какой половине функции есть корень
                b = midpoint
            else:
                a = midpoint

            counter += 1
            if counter > max_iterations:
                print(f'Достигнут лимит ({max_iterations}) итераций')
                break

        print(t)
        print(f'Корень уравнения равен = {_root}\n')
        return _root

    def newton_method(self, initial_guess: float, max_iterations: int = 1000) -> float:
        print("Вычисление методом Ньютона")
        x = initial_guess
        counter = 0
        t = PrettyTable(['Iteration', 'x', 'F(x)', "F'(x)", 'precision'])

        while counter < max_iterations:
            f_x = self.func(x)
            f_prime_x = self.func.derivative(x)

            if f_prime_x == 0.0:
                print(t)
                print("Производная равна нулю; метод Ньютона не применим.")
                return 0

            precision = abs(f_x / f_prime_x)
            t.add_row([counter, x, f_x, f_prime_x, precision])

            if abs(f_x) < self.precision and precision <= self.precision:
                print(t)
                print(f'Корень уравнения равен = {x}\n')
                return x  # Если достигли нужной точности, возвращаем корень

            x = x - f_x / f_prime_x
            counter += 1

        print(t)
        print("Метод Ньютона не сошелся за указанное число итераций.")

    def plot_function(self) -> None:
        # Создаем массив x с диапазоном, например, от -10 до 10
        x = np.linspace(-10, 10, 500)
        y = self.func(x)

        # Построение графика функции
        plt.plot(x, y, label=f'$f(x) = {self.func.a}x^3 + {self.func.b}x^2 + {self.func.c}x + {self.func.d}$')
        plt.axhline(0, color='black', linewidth=0.5)  # Ось X
        plt.axvline(0, color='black', linewidth=0.5)  # Ось Y

        # Настройка графика
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.title('Graph of the Function')
        plt.legend()
        plt.grid(True)
        plt.ylim(-10, 10)  # Устанавливаем пределы по оси Y для лучшего отображения
        plt.xlim(-10, 10)  # Устанавливаем пределы по оси X
        plt.show()

    def plot(self) -> None:
        x = np.linspace(-5, 5, 400)

        # Определим функции
        y1 = self.func.a * pow(x,3)
        y2 = -self.func.b * pow(x,2) - self.func.c * x - self.func.d

        # Построим график
        plt.figure(figsize=(10, 6))
        plt.plot(x, y1, label=rf"$y = {self.func.a}x^3$", color='blue')
        plt.plot(x, y2, label=rf"$y = {-self.func.b:+}x^2 {-self.func.c:+}x {-self.func.d:+}$", color='red')
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title("Графики функций")
        plt.axhline(0, color='black', linewidth=0.5)
        plt.axvline(0, color='black', linewidth=0.5)
        plt.legend()
        plt.grid(True)
        plt.show()
