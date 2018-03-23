import leather
from datetime import datetime
import pytz


def render_course_enrollments(data: list):
    items = []
    keys = []

    for d in data:
        if d['название курса'] not in keys:
            keys.append(d['название курса'])
            items.append({
                'y': d['название курса'],
                'x': 0
            })

    for course in [d['название курса'] for d in data]:
        for item in items:
            if item['y'] == course:
                item['x'] += 1

    def x(row, index):
        return row['x']

    def y(row, index):
        return row['y']

    chart = leather.Chart('Записи на курсы')
    chart.add_bars(items, x=x, y=y)

    filename = f"enrollments_graph_" \
               f"{datetime.now(tz=pytz.timezone('Europe/Moscow')).strftime('%d%m%Y_%H%M')}.svg"

    chart.to_svg(f'/data/{filename}')
    return filename



# import leather
#
# data = [
#         {'x': 10, 'q': {'y': ['One']}},
#         {'x': 7, 'q': {'y': ['Two']}}
# ]
#
# def x(row, index):
#     return row['x']
#
# def y(row, index):
#     return row['q']['y'][0]
#
# chart = leather.Chart('Data')
# chart.add_bars(data, x=x, y=y)
# chart.to_svg('./testsvg.svg')
