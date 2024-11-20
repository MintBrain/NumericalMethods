from prettytable import PrettyTable


def print_init_table(n, a, b, c, d):
    # Вывод таблицы коэффициентов
    table = PrettyTable()
    table.field_names = ["i", "a[i]", "b[i]", "c[i]", "d[i]"]
    for i in range(n):
        table.add_row([i + 1, round(a[i], 3), round(b[i], 3), round(c[i], 3), round(d[i], 3)])
    print("\nИзначальная таблица коэффициентов:")
    print(table)


def print_result_table(n, U, V, X):
    # Создание таблицы результатов
    table = PrettyTable()
    table.field_names = ["i", "U[i]", "V[i]", "X[i]"]
    for i in range(n):
        table.add_row([i + 1, round(U[i], 3), round(V[i], 3), round(X[i], 3)])

    print("\nИтоговая таблица коэффициентов:")
    print(table)


def check(x, a, b, c, d):
    n = len(d)
    r = [0] * n  # Вектор невязок

    for i in range(n):
        _a = a[i] * x[i - 1] if i > 0 else 0
        _c = c[i] * x[i + 1] if i < n - 1 else 0
        r[i] = d[i] - _a - (b[i] * x[i]) - _c

    print("\nВектор невязок:", [round(_r, 3) for _r in r])

    _result = all([round(_r, 1) == 0 for _r in r])
    if _result:
        print('Проверка: Решение верно')
    else:
        print('Проверка: Решение не верно')
    return r


def solve_tridiagonal(a: list[float], b: list[float], c: list[float], d: list[float]) -> list[float]:
    n = len(d)
    if len(a) != n or len(b) != n or len(c) != n:
        raise ValueError("Размеры векторов a, b, c, d должны совпадать.")

    # Прямой ход
    U: list[float] = [0] * n
    V: list[float] = [0] * n

    # Инициализация для первого элемента
    U[0] = -c[0] / b[0]
    V[0] = d[0] / b[0]

    for i in range(1, n):
        denominator = a[i] * U[i - 1] + b[i]
        if denominator == 0:
            raise ZeroDivisionError("Обнаружена нулевая диагональ, система неразрешима.")
        U[i] = -c[i] / denominator
        V[i] = (d[i] - a[i] * V[i - 1]) / denominator

    # Обратный ход
    x: list[float] = [0] * n
    x[-1] = V[-1]

    for i in range(n - 2, -1, -1):
        x[i] = U[i] * x[i + 1] + V[i]

    print_result_table(n, U, V, x)

    return x


def _input() -> tuple[list[float], list[float], list[float], list[float]]:
    while True:
        try:
            # Ввод числа уравнений
            n = int(input("Введите число уравнений (n >= 2): "))
            if n < 2:
                print("Число уравнений должно быть >= 2.")
                continue
            break

        except ValueError:
            print("Введите корректное целое число для числа уравнений.")

    print("\nВведите коэффициенты трехдиагональной матрицы.")
    print("Формат ввода для каждой строки: a b c d")
    print("где a, b, c — коэффициенты, d — правая часть (a для первой строки и c для последней строки = 0).")

    # Инициализация коэффициентов
    a: list[float] = [0] * n
    b: list[float] = [0] * n
    c: list[float] = [0] * n
    d: list[float] = [0] * n

    # Ввод коэффициентов построчно
    for i in range(n):
        while True:
            try:
                row = input(f"Уравнение {i + 1}: ").split()
                if len(row) != 4:
                    raise ValueError("Должно быть ровно 4 значения: a b c d.")
                row = list(map(float, row))
                a[i], b[i], c[i], d[i] = row
                # Проверка граничных условий
                if i == 0 and a[i] != 0:
                    print("a[0] должно быть равно 0. Исправьте ввод.")
                    continue
                if i == n - 1 and c[i] != 0:
                    print("c[n-1] должно быть равно 0. Исправьте ввод.")
                    continue
                break
            except ValueError as ve:
                print(f"Ошибка ввода: {ve}. Попробуйте еще раз.")

    print_init_table(n, a, b, c, d)

    return a, b, c, d


def test():
    # Коэффициенты трехдиагональной матрицы
    a = [0, -1.7, 1.4, -1]  # поддиагональ (a[0] = 0)
    b = [1.25, 2.87, 4.7, 5]  # главная диагональ
    c = [-0.2, -1, -2, 0]  # наддиагональ (c[-1] = 0)
    d = [2.3, 4, 3.5, 1.4]  # правая часть

    print_init_table(len(d), a, b, c, d)
    solution = solve_tridiagonal(a, b, c, d)
    check(solution, a, b, c, d)

    # print(717126 / 314285)
    # print(173552 / 62857)
    # print(14217 / 314285)
    # print(454216 / 1571425)


def main():
    args = _input()
    solution = solve_tridiagonal(*args)
    check(solution, *args)


if __name__ == '__main__':
    test()
