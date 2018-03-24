import random
from datetime import datetime
import pytz


EDUCATION_LEVELS = {
    'p': 'ученая степень',
    'm': 'магистратура или специалитет',
    'b': 'бакалавриат',
    'a': 'незаконченное высшее образование',
    'hs': 'среднее',
    'jhs': 'незаконченное среднее',
    'el': 'начальное',
    'none': 'нет формального образования',
    'other': 'другое'
}


def object_to_text(arr: list,
                   replace_id=False,
                   replace_gender=False,
                   replace_none=False,
                   replace_education=False):
    try:
        lengths = {}
        line = ''
        items_count_string = ''

        num = 0
        if replace_id:
            for item in arr:    # type: dict
                num += 1
                item['номер'] = num
            items_count_string = f"Количество записей: {str(num)}\n"

        if replace_gender:
            for item in arr:    # type: dict
                item['пол'] = 'М' if item['пол'] == 'm' \
                    else 'Ж' if item['пол'] == 'f' \
                    else 'др.' if item['пол'] == 'l' or item['пол'] == 'o' else '-'

        if replace_none:
            for item in arr:    # type: dict
                for key in item.keys():
                    if item[key] is None or item[key] == 'None' or item[key] == 'none':
                        item[key] = '-'

        if replace_education:
            for item in arr:    # type: dict
                if item['образование'] in EDUCATION_LEVELS.keys():
                    item['образование'] = EDUCATION_LEVELS[item['образование']]

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

        result = f"Дата: {datetime.now(tz=pytz.timezone('Europe/Moscow')).strftime('%d.%m.%Y %H:%M')}\n" \
            f"{items_count_string}{result}"

        return result
    except Exception as e:
        print(e)
        return f"Generating error [{str(e)}]"


def random_token(len: int):
    dictionary = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    token = ''
    for num in range(len):
        token = f"{token}{dictionary[random.randrange(0, 62, 1)]}"
    return token


def html_image_wrapper(image):
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Графики</title>
    </head>
    <body>
        {image}
    </body>
    </html>
    """
    return html
