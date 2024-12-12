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


def cubic_spline_interpolation(x_values, y_values, query_point):
    """
    Интерполяция кубическим сплайном.
    :param x_values: Список значений x (должен быть отсортирован).
    :param y_values: Список значений y, соответствующих x.
    :param query_point: Точка, для которой требуется значение.
    :return: Интерполированное значение в query_point.
    """
    n = len(x_values) - 1  # Количество интервалов
    h = [x_values[i + 1] - x_values[i] for i in range(n)]

    # Вычисление коэффициентов уравнений для второй производной
    alpha = [0] * (n + 1)
    for i in range(1, n):
        alpha[i] = (3 / h[i]) * (y_values[i + 1] - y_values[i]) - (3 / h[i - 1]) * (y_values[i] - y_values[i - 1])

    # Решение трёхдиагональной системы
    l = [1] + [0] * n
    mu = [0] * (n + 1)
    z = [0] * (n + 1)

    for i in range(1, n):
        l[i] = 2 * (x_values[i + 1] - x_values[i - 1]) - h[i - 1] * mu[i - 1]
        mu[i] = h[i] / l[i]
        z[i] = (alpha[i] - h[i - 1] * z[i - 1]) / l[i]

    l[n] = 1
    z[n] = 0

    c = [0] * (n + 1)
    b = [0] * n
    d = [0] * n
    a = y_values[:-1]

    for j in range(n - 1, -1, -1):
        c[j] = z[j] - mu[j] * c[j + 1]
        b[j] = (y_values[j + 1] - y_values[j]) / h[j] - h[j] * (c[j + 1] + 2 * c[j]) / 3
        d[j] = (c[j + 1] - c[j]) / (3 * h[j])

    # Найти соответствующий интервал для query_point
    for i in range(n):
        if x_values[i] <= query_point <= x_values[i + 1]:
            dx = query_point - x_values[i]
            return a[i] + b[i] * dx + c[i] * dx ** 2 + d[i] * dx ** 3

    raise ValueError("Точка вне диапазона интерполяции.")


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
