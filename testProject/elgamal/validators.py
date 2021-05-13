from typing import Union

ErrorMessage = str


def validate_keys(
        keys: Union[
            list[int],
            ]) -> tuple[bool, Union[ErrorMessage, None]]:
    if len(keys) in (1, 3, 4):
        is_valid = True
        error = None
    else:
        is_valid = False
        error = 'Неправильный формат ключей. Проверьте кол-во элементов!'
    return is_valid, error