import asyncio
from aiohttp import web, MsgType
from aiohttp_mako import template

import version
from vox_reddi_py3 import start_parsing_votes_for_post


class RouteHandler:
    def __init__(self):
        pass

    @template('home.mako')
    async def index(self, request):
        return {'version': version.version}

    @template('result.mako')
    async def post(self, request):
        post_id = request.match_info['post_id']
        ws_url = request.app.router['ws'].url(parts={'post_id': post_id})
        return {'post_id': post_id,
                'ws_url': ws_url}

    async def ws(self, request):
        post_id = request.match_info['post_id']
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        async for msg in ws:
            if msg.tp == MsgType.text:
                await start_parsing_votes_for_post(post_id, ws)
        return ws

route_handler = RouteHandler()
routes = [
    ('GET', '/',                   route_handler.index, 'root'),
    ('GET', '/post/{post_id}/',    route_handler.post, 'post'),
    ('GET', '/post/{post_id}/ws/', route_handler.ws, 'ws'),
]
