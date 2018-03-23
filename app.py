import asyncio
from aiohttp import web
import aiohttp_jinja2
import jinja2

from web import api


def app(l=None):
    loop = l or asyncio.get_event_loop()
    app = web.Application(loop=loop)

    app.router.add_get('/', api.admin_panel)
    app.router.add_post('/auth', api.authorization)
    app.router.add_get('/admin/enrollment_data', api.get_enrollment_data)
    app.router.add_get('/admin/users', api.get_users_data)

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
