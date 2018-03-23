import pygal


def render_course_enrollments(data: list):
    items = {}
    for item in data:
        if item['название курса'] not in items.keys():
            items[item['название курса']] = 1
        else:
            items[item['название курса']] += 1

    bar_chart = pygal.HorizontalBar()
    bar_chart.title = 'Количество записей на курсы'
    for item in items:
        bar_chart.add(item, items[item])

    return bar_chart.render()
