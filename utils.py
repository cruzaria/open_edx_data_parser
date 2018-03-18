import random
from datetime import datetime
import pytz


def object_to_text(arr: list, add_date=False):
    lengths = {}
    line = ''

    for key in arr[0].keys():
        if key not in lengths.keys():
            lengths[key] = len(key)

    for item in arr:    # type: dict
        for key in item.keys():
            if len(str(item[key])) > lengths[key]:
                lengths[key] = len(str(item[key]))

    for key in lengths.keys():
        line = f"{line}{'#' * lengths[key]}#"

    result = ''
    for key in arr[0].keys():
        result = f"{result}{key}{' ' * (lengths[key] - len(key))}|"

    result = f"{result}\n{line}\n"

    for item in arr:    # type: dict
        for key in arr[0].keys():
            result = f"{result}{str(item[key])}{' ' * (lengths[key] - len(str(item[key])))}|"
        result = f"{result}\n"

    if add_date:
        result = f"{datetime.now(tz=pytz.timezone('Europe/Moscow')).strftime('%d.%m.%Y %H:%M')}\n{result}"

    return result


def random_token(len: int):
    dictionary = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    token = ''
    for num in range(len):
        token = f"{token}{dictionary[random.randrange(0, 62, 1)]}"
    return token
