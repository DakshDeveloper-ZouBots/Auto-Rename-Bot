from aiohttp import web
routes = web.RouteTableDef()
@routes.get("/")
async def root(request):
    return web.json_response({"status": "active", "brand": "Wzgram"})
async def web_server():
    app = web.Application()
    app.add_routes(routes)
    return app
