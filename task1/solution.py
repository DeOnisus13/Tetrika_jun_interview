from functools import wraps


def strict(func):
    """
    Декоратор для проверки соответствия типов переданных в функцию аргументов.
    Также проверяет соответствие типа результата выполнения функции и ожидаемого типа.
    """

    @wraps(func)
    def inner(*args):
        valid_types = list(func.__annotations__.values())

        for i in range(len(args)):
            arg = args[i]
            arg_type = valid_types[i]
            if not isinstance(arg, arg_type):
                raise TypeError(f"Аргумент {arg} не соответствует требуемому типу. Должен быть тип {arg_type}.")

        result = func(*args)
        if not isinstance(result, valid_types[-1]):
            raise TypeError("Результат выполнения функции не соответствует требуемому типу.\n"
                            f"Ожидался тип {valid_types[-1]}. Результат - тип {type(result)}.")

        return func(*args)

    return inner
