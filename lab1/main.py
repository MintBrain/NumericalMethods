
from lab1.input import get_precision, choose_equation_type, get_coefficients, get_user_equation, get_method
from lab1.funcs import Func, Solver


def get_func(equation_type) -> Func:
    while True:
        try:
            if equation_type == 1:
                func = Func(*get_coefficients())
            elif equation_type == 2:
                func = get_user_equation()
            return func
        except Exception as e:
            print(f'Ошибка {e}')
            print('Попробуйте ввести данные заново.')



def main():
    equation_type = choose_equation_type()
    func = get_func(equation_type)

    precision = get_precision()
    solver = Solver(func, precision)

    method, *params = get_method()

    print()
    if method == 1:
        solver.bisection_method(*params)
    elif method == 2:
        solver.newton_method(params)
    elif method == 3:
        solver.bisection_method(*params[0])
        solver.newton_method(*params[1])


def test():
    solver = Solver(1,0,2,2)
    solver.bisection_method(a=-2, b=2)
    solver.newton_method(0)


if __name__ == '__main__':
    main()
