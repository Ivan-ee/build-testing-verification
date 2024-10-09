import math

errInvalidCf = "Переданы неправильные коэфиценты"
errInvalidArg = "Коэффициент a не должен быть равен 0"
errNoRoots = "Уравнение корней не имеет"


def find_quadratic_roots(a, b, c):
    """Возвращает корни квадратного уравнения для a != 0.

    Примеры:

    >>> find_quadratic_roots(0, -3, 2)
    Traceback (most recent call last):
    ...
    ValueError: Коэффициент a не должен быть равен 0

    >>> find_quadratic_roots(2, -3, 2)
    Traceback (most recent call last):
    ...
    ValueError: Уравнение корней не имеет

    >>> find_quadratic_roots(0, 0, 0)
    Traceback (most recent call last):
    ...
    ValueError: Все коэффициенты равны 0, уравнение не определено

     >>> find_quadratic_roots("ds", 0, -1)
    Traceback (most recent call last):
    ...
    ValueError: Переданы неверные коэфиценты

    >>> find_quadratic_roots(1, -3, 2)
    (2.0, 1.0)
    """

    if type(a) != int or type(b) != int or type(c) != int:
        raise ValueError(errInvalidCf)

    if a == 0:
        raise ValueError(errInvalidArg)

    discriminant = b ** 2 - 4 * a * c

    if discriminant < 0:
        raise ValueError(errNoRoots)

    root1 = (-b + math.sqrt(discriminant)) / (2 * a)
    root2 = (-b - math.sqrt(discriminant)) / (2 * a)

    return root1, root2


if __name__ == '__main__':
    # import doctest
    #
    # doctest.testmod()

    a = 1
    b = -3
    c = 2

    assert find_quadratic_roots(a, b, c) == (2.0, 1.0)

    try:
        find_quadratic_roots(0, b, c)
    except ValueError as e:
        assert str(e) == errInvalidArg

    try:
        find_quadratic_roots(a, "tri", c)
    except ValueError as e:
        assert str(e) == errInvalidCf

    try:
        find_quadratic_roots(2, -3, 2)
    except ValueError as e:
        assert str(e) == errNoRoots
