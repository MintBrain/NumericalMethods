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
    x_values, y_values = x, y

    while True:
        try:
            query_point = float(input("Введите точку для интерполяции (или 'q' для выхода): "))
            if query_point < min(x_values) or query_point > max(x_values):
                print("Точка вне диапазона входных данных.")
                continue

            result = cubic_spline_interpolation(x_values, y_values, query_point)
            print(f"Интерполированное значение в точке {query_point}: {result}")
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
    test()
