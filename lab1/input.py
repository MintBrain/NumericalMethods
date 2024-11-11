from funcs import Func

def get_coefficients():
    while True:
        try:
            a = float(input("Введите коэффициент a для x^3: "))
            if a == 0:
                print("Коэффициент 'a' не может быть равен нулю. Пожалуйста, введите значение, отличное от нуля.")
                continue

            b = float(input("Введите коэффициент b для x^2: "))
            c = float(input("Введите коэффициент c для x: "))
            d = float(input("Введите свободный член d: "))
            return a, b, c, d
        except ValueError:
            print("Ошибка ввода, пожалуйста, введите числовые значения.")

def get_precision() -> float:
    while True:
        try:
            precision = float(input("Введите точность для вычислений (например: 0.01): "))
            if precision <= 0:
                print('Значение должно быть больше 0')
                continue
            return precision
        except ValueError:
            print("Ошибка ввода, пожалуйста, введите числа.")

def get_bisection_params(func: Func) -> tuple[float, float]:
    """Запрашивает у пользователя границы интервала для метода бисекции."""
    while True:
        try:
            a = float(input("Введите начальное значение интервала (a): "))
            b = float(input("Введите конечное значение интервала (b): "))
            if a >= b:
                print("Начало интервала должно быть меньше конца. Попробуйте снова.")
                continue

            if func(a)*func(b) >= 0:
                print("Функция должна менять знак на концах интервала [a, b].")
                continue

            return a, b
        except ValueError:
            print("Ошибка ввода, пожалуйста, введите числа.")

def get_newton_params(func: Func) -> tuple[float]:
    """Запрашивает у пользователя начальное приближение для метода Ньютона."""
    while True:
        try:
            initial_guess = float(input("Введите начальное приближение для метода Ньютона: "))

            if func(initial_guess)*func.derivative2(initial_guess) <= 0:
                print("Сходимость для приближения не выполняется.")
                continue

            return initial_guess,
        except ValueError:
            print("Ошибка ввода, пожалуйста, введите число.")

def get_method(func: Func):
    """Запрашивает у пользователя выбор метода и возвращает его номер и параметры для него."""
    print("Выберите метод для нахождения корня уравнения:")
    print("1. Метод бисекции")
    print("2. Метод Ньютона")
    print("3. Оба метода")

    while True:
        try:
            method = int(input("Введите номер метода (1, 2 или 3): "))
            if method == 1:
                params = get_bisection_params(func)
                return method, params
            elif method == 2:
                params = get_newton_params(func)
                return method, params
            elif method == 3:
                bisection_params = get_bisection_params(func)
                newton_params = get_newton_params(func)
                return method, bisection_params, newton_params
            else:
                print("Пожалуйста, выберите один из вариантов (1, 2 или 3).")
        except ValueError:
            print("Ошибка ввода, пожалуйста, введите номер метода (1, 2 или 3).")
