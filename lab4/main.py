from graph import evaluate_lagrange, evaluate_newton, plot_polynomials
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def lagrange_polynomial(x_values, y_values):
    """
    Строит интерполяционный полином Лагранжа.
    :param x_values: Список значений x.
    :param y_values: Список значений y.
    :return: Строка, представляющая полином Лагранжа.
    """
    n = len(x_values)
    terms = []  # Для хранения членов полинома

    for i in range(n):
        if y_values[i] == 0:  # Пропускаем, если вклад нулевой
            continue

        # Построение базисного полинома L_i(x)
        numerator_terms = []  # Члены числителя
        denominator = 1  # Знаменатель

        for j in range(n):
            if i != j:
                numerator_terms.append(f"(x - {x_values[j]})")
                denominator *= (x_values[i] - x_values[j])

        # Базисный полином L_i(x)
        L_i = f"({' * '.join(numerator_terms)}) / {denominator}"
        terms.append(f"{y_values[i]} * {L_i}")

    # Полный полином Лагранжа
    L = " + ".join(terms)
    return L


def newton_polynomial(x_values, y_values):
    """
    Строит интерполяционный полином Ньютона.
    :param x_values: Список значений x.
    :param y_values: Список значений y.
    :return: Строка, представляющая полином Ньютона.
    """
    n = len(x_values)

    # Вычисление разделенных разностей
    divided_diff = [y_values[:]]
    for level in range(1, n):
        diffs = []
        for i in range(n - level):
            diff = (divided_diff[level - 1][i + 1] - divided_diff[level - 1][i]) / (x_values[i + level] - x_values[i])
            diffs.append(diff)
        divided_diff.append(diffs)

    # Формирование полинома Ньютона
    terms = []
    for level in range(n):
        if divided_diff[level][0] == 0:  # Пропускаем нулевые коэффициенты
            continue

        term = [f"{divided_diff[level][0]}"]
        for i in range(level):
            term.append(f"(x - {x_values[i]})")
        terms.append(" * ".join(term))

    # Полный полином Ньютона
    N = " + ".join(terms)
    return N


def input_points() -> tuple[list[float], list[float]]:
    """
    Ввод точек (x, y) с проверкой на корректность.
    :return: Кортеж из двух списков: x и y.
    """
    while True:
        try:
            print("Введите точки в формате: x1 y1, x2 y2, ...")
            points = input("Пример: -1 3, 2 0, 5 2\n").strip()

            # Разделение на пары (x, y)
            pairs = points.split(",")
            x = []
            y = []

            for pair in pairs:
                # Очистка пробелов и разделение значений
                values = list(map(float, pair.strip().split()))
                if len(values) != 2:
                    raise ValueError(f"Неправильный формат точки: '{pair}'. Используйте формат 'x y'.")

                xi, yi = values
                if xi in x:
                    raise ValueError(f"Повторяющееся значение x: {xi}. Все значения x должны быть уникальными.")

                x.append(xi)
                y.append(yi)

            return x, y

        except ValueError as e:
            print(f"Ошибка ввода: {e}")
            print("Попробуйте снова.\n")


def point_input(x,y):
    while True:
        try:
            # Выбор метода
            print("\nВыберите метод для расчета точки:")
            print("1. Лагранжа")
            print("2. Ньютона")
            method = input("Введите номер метода (1 или 2): ").strip()

            if method not in {"1", "2"}:
                raise ValueError("Неверный выбор метода. Введите 1 или 2.")

            # Ввод точки
            x_eval = float(input("Введите значение x, для которого хотите вычислить y: ").strip())

            # Вычисление результата
            if method == "1":
                y_eval = evaluate_lagrange(x, y, x_eval)
                print(f"\nЗначение полинома Лагранжа в точке x = {x_eval}: y = {y_eval:.2f}")
            else:
                y_eval = evaluate_newton(x, y, x_eval)
                print(f"\nЗначение полинома Ньютона в точке x = {x_eval}: y = {y_eval:.2f}")

            plt.scatter(x_eval, y_eval, color="blue", label=f"Точка ({x_eval}, {y_eval:.2f})", linewidths=6)
            plt.legend()
            plt.draw()
            plt.pause(0.3)

            # Спрашиваем, хочет ли пользователь продолжить
            continue_choice = input("\nХотите вычислить ещё одну точку? (да/нет): ").strip().lower()
            if continue_choice not in {"да", "yes", "y"}:
                print("Работа завершена.")
                break

        except ValueError as ve:
            print(f"Ошибка ввода: {ve}. Попробуйте снова.")
        except Exception as err:
            print(f"Произошла ошибка: {err}. Попробуйте снова.")


def program(x, y):
    # Построение полиномов
    lagrange = lagrange_polynomial(x, y)
    newton = newton_polynomial(x, y)

    # Вывод результатов
    print("Интерполяционный полином Лагранжа:")
    print(lagrange)

    print("\nИнтерполяционный полином Ньютона:")
    print(newton)

    plot_polynomials(x, y)
    print()
    point_input(x,y)



def test():
    # Ввод данных
    x_values = [-1, 2, 5]
    y_values = [4, 3, 4]
    # x_values = [-1, 0,0.5,1]
    # y_values = [0,2,9/8,0]
    program(x_values, y_values)


def main():
    x_values, y_values = input_points()
    program(x_values, y_values)


# Пример использования
if __name__ == "__main__":
    test()
