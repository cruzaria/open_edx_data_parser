import asyncio
from aiohttp import web
import pymysql
import os
from datetime import datetime
import aiohttp_jinja2
import jinja2
import pytz

from utils import object_to_text, random_token


USER_TOKEN = random_token(16)

config = {
    'host': os.environ['OE_MYSQL_HOST'],
    'user': os.environ['OE_MYSQL_USER'],
    'pass': os.environ['OE_MYSQL_PASS'],
    'db': os.environ['OE_MYSQL_DB'],
    'token': os.environ['OE_TOKEN']
}


async def get_enrollment_data(request):
    if 'TOKEN' in request.cookies.keys():
        if request.cookies['TOKEN'] == USER_TOKEN:
            connection = pymysql.connect(
                host=config['host'],
                user=config['user'],
                password=config['pass'],
                db=config['db'],
                charset='utf8',
                cursorclass=pymysql.cursors.DictCursor
            )
            try:
                with connection.cursor() as cursor:
                    sql = "SELECT sc.id AS `номер`, " \
                          "coc.display_name AS `название курса`, " \
                          "sc.created AS `дата записи`, " \
                          "au.username AS `логин`, " \
                          "au.first_name AS `имя`, " \
                          "au.last_name AS `фамилия`, " \
                          "au.email AS email " \
                          "FROM student_courseenrollment AS sc " \
                          "INNER JOIN auth_user AS au " \
                          "ON sc.user_id = au.id " \
                          "INNER JOIN course_overviews_courseoverview AS coc " \
                          "ON sc.course_id = coc.id"
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    result = object_to_text(result, replace_id=True)
                    filename = f"course_enrollment" \
                               f"{datetime.now(tz=pytz.timezone('Europe/Moscow')).strftime('%d%m%Y_%H%M')}.txt"
                    with open(os.path.join('/data', filename), 'w') as f:
                        f.write(result)
                        f.close()
                    headers = {
                        "Content-Disposition": f"attachment; filename={filename}"
                    }
                    return web.Response(body=open(os.path.join('/data', filename), 'rb').read(), headers=headers)
            except Exception as e:
                web.Response(body=str(e))
            finally:
                connection.close()

    response = aiohttp_jinja2.render_template('login.jinja2', request, {})
    response.headers['Content-Language'] = 'ru'
    return response


async def authorization(request: web.Request):
    json = await request.json()
    token = json['token']
    if token:
        if token == config['token']:
            headers = {
                'Set-Cookie': f'TOKEN={USER_TOKEN}'
            }
            return web.Response(body="{'result': True}", headers=headers)
    return web.Response(body="{'result': False}")


async def admin_panel(request: web.Request):
    if 'TOKEN' in request.cookies.keys():
        if request.cookies['TOKEN'] == USER_TOKEN:
            response = aiohttp_jinja2.render_template('admin.jinja2', request, {})
            response.headers['Content-Language'] = 'ru'
            return response
    response = aiohttp_jinja2.render_template('login.jinja2', request, {})
    response.headers['Content-Language'] = 'ru'
    return response


def app(l=None):
    loop = l or asyncio.get_event_loop()
    app = web.Application(loop=loop)

    app.router.add_get('/', admin_panel)
    app.router.add_post('/auth', authorization)
    app.router.add_get('/admin/enrollment_data', get_enrollment_data)

    return app


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    app = app(loop)
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('/app/pages'))
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
