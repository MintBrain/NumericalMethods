import matplotlib.pyplot as plt
import numpy as np
from prettytable import PrettyTable

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
        return self.a * pow(x, 3) + self.b * pow(x, 2) + self.c * x + self.d

    def derivative(self, x: float) -> float:
        """Вычисление значения производной f'(x) = 3ax^2 + 2bx + c."""
        return 3 * self.a * pow(x, 2) + 2 * self.b * x + self.c


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
            # print(f'Итерация {counter}: a={a};\tb={b};\tmidpoint={midpoint};\tF(mid)={f_mid};\tprecision={precision}')

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

            if f_prime_x == 0:
                print(t)
                print("Производная равна нулю; метод Ньютона не применим.")

            precision = abs(f_x / f_prime_x)
            t.add_row([counter, x, f_x, f_prime_x, precision])

            if abs(f_x) < self.precision:
                print(t)
                print(f'Корень уравнения равен = {x}\n')
                return x  # Если достигли нужной точности, возвращаем корень

            x = x - f_x / f_prime_x
            counter += 1

            # Проверка, достигли ли мы требуемой точности
            if precision < self.precision:
                print(t)
                print(f'Корень уравнения равен = {x}\n')
                return x

        print(t)
        print("Метод Ньютона не сошелся за указанное число итераций.")

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
