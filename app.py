import asyncio
from aiohttp import web
import pymysql
import os
from datetime import datetime

from utils import object_to_text


config = {
    'host': os.environ['OE_MYSQL_HOST'],
    'user': os.environ['EO_MYSQL_USER'],
    'pass': os.environ['OE_MYSQL_PASS'],
    'db': os.environ['OE_MYSQL_DB']
}


connection = pymysql.connect(
    host=config['host'],
    user=config['user'],
    password=config['pass'],
    db=config['db'],
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor
)


async def get_enrollment_data(request):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT `sc.id` AS `id`, `sc.course_id` AS `course_id`, `sc.created` AS `create_date`, `au.username` AS `username`, `au.first_name` AS `first_name`, `au.last_name` AS `last_name`, `au.email` AS `email` FROM `student_courseenrollment` AS `sc` INNER JOIN `auth_user` AS `au` ON `sc.user_id` = `au.id`"
            cursor.execute(sql)
            result = cursor.fetchall()
            result = object_to_text(result)
            filename = f"{datetime.now().strftime('%d%M%Y_%H%m')}.txt"
            with open(os.path.join('/data', filename), 'w') as f:
                f.write(result)
                f.close()
            return web.FileResponse(os.path.join('/data', filename))
    finally:
        connection.close()


def app(l=None):
    loop = l or asyncio.get_event_loop()
    app = web.Application(loop=loop)

    app.router.add_get('/admin/enrollment_data', get_enrollment_data)

    return app


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    app = app(loop)
    handler = app.make_handler()
    f = loop.create_server(handler, '0.0.0.0', 8899)
    srv = loop.run_until_complete(f)
    print('serving on', srv.sockets[0].getsockname())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        srv.close()
        loop.run_until_complete(srv.wait_closed())
        loop.close()
