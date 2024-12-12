import matplotlib.pyplot as plt
import numpy as np


def plot_cubic_spline(x_values, y_values, cubic_spline_fn, num_points=100):
    """
    Строит график кубического сплайна.
    :param x_values: Список значений x (должен быть отсортирован).
    :param y_values: Список значений y, соответствующих x.
    :param cubic_spline_fn: Функция для интерполяции (например, cubic_spline_interpolation).
    :param num_points: Количество точек для построения плавной кривой.
    """
    # Подготовить данные для графика
    x_dense = np.linspace(x_values[0], x_values[-1], num_points)
    y_dense = [cubic_spline_fn(x_values, y_values, x) for x in x_dense]

    # Построить график
    plt.figure(figsize=(8, 6))
    plt.plot(x_dense, y_dense, label="Кубический сплайн", color="blue")
    plt.scatter(x_values, y_values, color="red", label="Исходные точки")  # Маркеры исходных точек
    plt.title("Интерполяция кубическим сплайном")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid(True)
    plt.ion()
    plt.show()
    plt.pause(0.2)


def verify_cubic_spline(cubic_spline_fn, x_values, y_values):
    """
    Проверяет корректность кубического сплайна.
    :param cubic_spline_fn: Функция для интерполяции (например, cubic_spline_interpolation).
    :param x_values: Список значений x.
    :param y_values: Список значений y.
    :return: True, если проверка пройдена, иначе False.
    """
    for x, y in zip(x_values, y_values):
        interpolated_value = cubic_spline_fn(x_values, y_values, x)
        if not abs(interpolated_value - y) < 1e-6:  # Допустимая погрешность
            print(f"Ошибка: в точке x = {x}, ожидается y = {y}, получено {interpolated_value}")
            return False

    print("Проверка успешно пройдена: все узловые точки совпадают.")
    return True


def gauss_elimination(a: list[list[float]], b: list[float]):
    n = len(b)
    # Прямой ход метода Гаусса
    for i in range(n):
        # Поиск максимального элемента для избежания вырождения
        max_row = i
        for k in range(i + 1, n):
            if abs(a[k][i]) > abs(a[max_row][i]):
                max_row = k
        # Поменять строки местами
        a[i], a[max_row] = a[max_row], a[i]
        b[i], b[max_row] = b[max_row], b[i]

        # Обнуление элементов ниже текущего
        for k in range(i + 1, n):
            factor = a[k][i] / a[i][i]
            for j in range(i, n):
                a[k][j] -= factor * a[i][j]
            b[k] -= factor * b[i]

        # Отображение промежуточных шагов
        print(f"Шаг {i + 1}:")
        print(tabulate([row + [b[i]] for i, row in enumerate(a)], headers=[f"x{j + 1}" for j in range(n)] + ["b"]))
        print()

    # Обратный ход
    x: list[float] = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = b[i]
        for j in range(i + 1, n):
            x[i] -= a[i][j] * x[j]
        x[i] /= a[i][i]

    return x


def cubic_spline_interpolation(x_points, y_points, x_new):
    # Количество данных точек
    n = len(x_points) - 1

    # Шаги между точками
    h = [x_points[i + 1] - x_points[i] for i in range(n)]

    # Матрица A и правая часть b для решения системы
    A = [[0, 0, 0] for _ in range(n+1)]  # создаём (n+1) строк для A
    b = [0] * (n + 1)

    # Граничные условия (вторые производные на концах равны 0)
    A[0] = [1, 0, 0]  # Для первого узла
    A[n] = [0, 1, 0]  # Для последнего узла
    b[0] = 0
    b[n] = 0

    # Заполнение системы для c_i (вторые производные)
    for i in range(1, n):
        A[i][0] = h[i - 1]
        A[i][1] = 2 * (h[i - 1] + h[i])
        A[i][2] = h[i]
        b[i] = 3 * ((y_points[i + 1] - y_points[i]) / h[i] - (y_points[i] - y_points[i - 1]) / h[i - 1])

    # Решение системы для c_i с помощью метода прогонки
    c = gauss_elimination(A, b)  # Обратите внимание на n+1 здесь

    # Вычисление коэффициентов b_i и d_i
    b_coeff = [0] * n
    d_coeff = [0] * n

    for i in range(n):
        b_coeff[i] = (y_points[i + 1] - y_points[i]) / h[i] - h[i] * (c[i + 1] + 2 * c[i]) / 3
        d_coeff[i] = (c[i + 1] - c[i]) / (3 * h[i])

    # Находим нужный интервал для точки x_new
    for i in range(n):
        if x_points[i] <= x_new < x_points[i + 1]:
            break

    # Вычисляем значение сплайна в точке x_new
    dx = x_new - x_points[i]
    y_new = (y_points[i] + b_coeff[i] * dx + c[i] * dx ** 2 + d_coeff[i] * dx ** 3)

    return y_new


# Ввод данных
def input_points():
    while True:
        try:
            n = int(input("Введите количество точек: "))
            if n < 2:
                print("Должно быть как минимум две точки.")
                continue

            x_values = []
            y_values = []

            print("Введите точки в формате x y (через пробел):")
            for _ in range(n):
                x, y = map(float, input().split())
                x_values.append(x)
                y_values.append(y)

            if sorted(x_values) != x_values:
                print("Значения x должны быть отсортированы.")
                continue

            return x_values, y_values
        except ValueError:
            print("Некорректный ввод. Попробуйте снова.")


def program(x, y):
    print("Кубическая интерполяция сплайнами")

    # Проверка корректности
    is_valid = verify_cubic_spline(cubic_spline_interpolation, x, y)
    if is_valid:
        print("Сплайн корректен.")
    else:
        print("В сплайне есть ошибки.")
        return

    plot_cubic_spline(x, y, cubic_spline_interpolation)

    while True:
        try:
            query_point = float(input("Введите точку для интерполяции (или 'q' для выхода): "))
            if query_point < min(x) or query_point > max(x):
                print("Точка вне диапазона входных данных.")
                continue

            result = cubic_spline_interpolation(x, y, query_point)
            print(f"Интерполированное значение в точке {query_point}: {result}")

            plt.scatter(query_point, result, color="blue", label=f"Точка ({query_point}, {result:.2f})", linewidths=6)
            plt.legend()
            plt.draw()
            plt.pause(0.3)
        except ValueError:
            print("Выход из программы.")
            break


def test():
    x = [1, 1.2, 1.4, 1.6, 1.8, 2]
    y = [1.2, 2, 3, 3.8, 5, 6.1]

    program(x, y)


def main():
    x, y = input_points()
    program(x, y)


if __name__ == "__main__":
    try:
        test()
    except Exception as e:
        print('Ошибка выполнения программы')
        print(e)
