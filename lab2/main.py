from tabulate import tabulate


def check(a,b,x):
    res = 0
    for i,_a in enumerate(a[0]):
        res += _a*x[i]
    print("Проверка:")
    if res == b[0]:
        print("Корни верны")
    else:
        print("Корни не верны")
    print()


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


def _input() -> tuple[list[list[float]], list[float]]:
    while True:
        try:
            # Ввод количества переменных
            n = int(input("Введите количество переменных: "))
            if n <= 0:
                print("Количество переменных должно быть положительным.")
                continue
            break
        except ValueError:
            print("Ошибка: введите целое положительное число для количества переменных.")

    a = []
    b = []
    print(f"Введите {n + 1} коэффициентов системы уравнений.")

    for i in range(n):
        while True:
            try:
                # Ввод строки коэффициентов для одного уравнения
                row = list(map(float, input(f"Коэффициенты уравнения {i + 1} (через пробел): ").split()))

                # Проверка на корректное количество значений (n коэффициентов и один свободный член)
                if len(row) != n + 1:
                    print(
                        f"Ошибка: уравнение {i + 1} должно содержать {n + 1} значений ({n} коэффициентов и свободный член).")
                    continue

                # Разделение строки на коэффициенты и свободный член
                a.append(row[:-1])
                b.append(row[-1])
                break

            except ValueError:
                print("Ошибка: введите числовые значения для коэффициентов и свободного члена.")

    return a, b


def test():
    n = 4
    a = [[2, 1, 1, 1],
         [2, 2, 2, 3],
         [2, 2, 3, 4],
         [2, 2, 3, 5]]
    b = [2, 1, 0, -1]

    print("\nНачальная система уравнений:")
    print(tabulate([row + [b[i]] for i, row in enumerate(a)], headers=[f"x{j + 1}" for j in range(n)] + ["b"]))
    print()

    solution = gauss_elimination(a, b)

    print("Решение:")
    for i in range(n):
        print(f"x{i + 1} = {solution[i]}")


def main():
    a, b = _input()

    print("\nНачальная система уравнений:")
    print(tabulate([row + [b[i]] for i, row in enumerate(a)], headers=[f"x{j + 1}" for j in range(len(a))] + ["b"]))
    print()
    _a = [[n for n in x] for x in a]
    _b = [x + 0 for x in b]
    try:
        solution = gauss_elimination(_a, _b)
    except Exception as e:
        print("Решение не найдено")
        return
    check(a,b,solution)

    print("Решение:")
    for i in range(len(a)):
        print(f"x{i + 1} = {solution[i]}")


if __name__ == "__main__":
    main()
