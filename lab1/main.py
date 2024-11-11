from input import get_precision, get_coefficients, get_method
from funcs import Func, Solver


def get_func() -> Func:
    while True:
        try:
            return Func(*get_coefficients())
        except Exception as e:
            print(f'Ошибка {e}')
            print('Попробуйте ввести данные заново.')


def main():
    func = get_func()
    precision = get_precision()
    solver = Solver(func, precision)
    solver.plot()
    method, *params = get_method(func)

    print()
    if method == 1:
        solver.bisection_method(*params)
    elif method == 2:
        solver.newton_method(params)
    elif method == 3:
        solver.bisection_method(*params[0])
        solver.newton_method(*params[1])


def test():
    solver = Solver(Func(1,0,6,-1))
    solver.plot()
    solver.plot_function()
    solver.bisection_method(a=-2, b=2)
    solver.newton_method(1)


if __name__ == '__main__':
    test()
