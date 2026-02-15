from settings import Settings
from aiohttp import web

app = web.Application()
settings = Settings()


# @app.get("/")
async def root(request):
    return web.json_response(dict(hi="haha"))
    # return web.Response(text="yay")


# @app.post("/")
async def routine(request):
    return web.Response(text="yay")


app.add_routes([web.get("/", root), web.post("/", routine)])

if __name__ == "__main__":
    web.run_app(app)
