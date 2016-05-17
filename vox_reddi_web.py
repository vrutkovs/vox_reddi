from os import path
import traceback
import sys

import asyncio
import aiohttp_mako
from aiohttp import web

from routes import routes, route_handler


async def init(loop, host, port):
    app = web.Application(loop=loop)

    for route in routes:
        app.router.add_route(route[0], route[1], route[2], name=route[3])

    static_path = path.join(path.dirname(__file__), "public")
    app.router.add_static('/static/', static_path, name='static')

    views_path = path.join(path.dirname(__file__), "views")
    aiohttp_mako.setup(app, input_encoding='utf-8', output_encoding='utf-8',
                       default_filters=['decode.utf8'], directories=[views_path])

    handler = app.make_handler()
    srv = await loop.create_server(handler, host, port)
    print("Server started at http://{}:{}".format(host, port))
    return srv, handler

port = 8080
host = '0.0.0.0'
if len(sys.argv) > 1:
    (host, port) = sys.argv[1].split(':')

loop = asyncio.get_event_loop()
srv, handler = loop.run_until_complete(init(loop, host, port))
try:
    loop.run_forever()
except KeyboardInterrupt:
    loop.run_until_complete(handler.finish_connections())
