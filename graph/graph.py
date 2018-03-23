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

    all_keys = [d['название курса'] for d in data]

    for course in all_keys:
        for item in items:
            if item['y'] == course:
                item['x'] += 1

    items = [items[d:d+10] for d in range(0, len(items), 10)]

    def x(row, index):
        return row['x']

    def y(row, index):
        return row['y']

    chart_grid = leather.Grid()

    charts = []
    for item in items:
        charts.append(leather.Chart('Записи на курсы'))
        charts[-1].add_bars(item, x=x, y=y)
        chart_grid.add_one(charts[-1])

    # chart = leather.Chart('Записи на курсы')
    # chart.add_bars(items, x=x, y=y)

    filename = f"enrollments_graph_" \
               f"{datetime.now(tz=pytz.timezone('Europe/Moscow')).strftime('%d%m%Y_%H%M')}.svg"

    chart_grid.to_svg(f'/data/{filename}')

    # chart.to_svg(f'/data/{filename}')
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
