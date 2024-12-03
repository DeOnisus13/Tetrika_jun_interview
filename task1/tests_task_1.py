import pytest

from task1.solution import strict


@strict
def sum_int_to_int(a: int, b: int) -> int:
    return a + b


@strict
def sum_int_to_str_true(a: int, b: int) -> str:
    return str(a + b)


@strict
def sum_int_to_str_false(a: int, b: int) -> str:
    return a + b


@strict
def sum_float_to_float(a: float, b: float) -> float:
    return a + b


@strict
def sum_float_to_str_false(a: float, b: float) -> str:
    return a + b


@strict
def concate_strings(a: str, b: str) -> str:
    return a + b


@strict
def boolean_check(a: bool, b: bool) -> str:
    if a or not a and b or not b:
        return "It's boolean type"
    return "Type don't match"


def test_strict_ok():
    """
    Тесты без выдачи ошибок.
    """
    assert sum_int_to_int(1, 2) == 3
    assert sum_int_to_str_true(1, 2) == "3"
    assert sum_float_to_float(1.2, 3.4) == 4.6
    assert concate_strings("Hello", "World") == "HelloWorld"
    assert boolean_check(True, False) == "It's boolean type"


def test_strict_errors():
    """
    Тесты с ошибками.
    """
    with pytest.raises(TypeError) as err:
        assert sum_int_to_int(1, 2.4)
    assert str(err.value) == "Аргумент 2.4 не соответствует требуемому типу. Должен быть тип <class 'int'>."

    with pytest.raises(TypeError) as err:
        assert sum_float_to_float(1, 2.4)
    assert str(err.value) == "Аргумент 1 не соответствует требуемому типу. Должен быть тип <class 'float'>."

    with pytest.raises(TypeError) as err:
        assert concate_strings("Hi", 25)
    assert str(err.value) == "Аргумент 25 не соответствует требуемому типу. Должен быть тип <class 'str'>."

    with pytest.raises(TypeError) as err:
        assert sum_int_to_str_false(1, 2)
    assert str(err.value) == "Результат выполнения функции не соответствует требуемому типу.\nОжидался тип <class 'str'>. Результат - тип <class 'int'>."

    with pytest.raises(TypeError) as err:
        assert sum_float_to_str_false(1.2, 2.3)
    assert str(err.value) == "Результат выполнения функции не соответствует требуемому типу.\nОжидался тип <class 'str'>. Результат - тип <class 'float'>."
