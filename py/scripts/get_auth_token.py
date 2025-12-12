import os
from aiohttp import web, ClientSession
from aiohttp.web_runner import GracefulExit
from asyncio import Event
from yarl import URL
from uuid import uuid4
import base64

print("Starting script")
client_id = os.environ.get("CLIENT_ID")

client_secret = os.environ.get("CLIENT_SECRET")
if not client_id:
    raise EnvironmentError("CLIENT_ID must be set")
if not client_secret:
    raise EnvironmentError("CLIENT_SECRET must be set")

async def auth(request):
    base: URL = URL("https://ticktick.com/oauth/authorize")
    scopes: list[str] = ["tasks:write", "tasks:read"]
    state: str = str(uuid4())
    global client_id
    redirect_uri:str = "http://localhost:8080/login"
    response_type:str = "code"

    url =  base.with_query(dict(
        client_id=client_id,
        scope=" ".join(scopes),
        state=state,
        redirect_uri=redirect_uri,
        response_type=response_type
    ))
                            

    raise web.HTTPFound(url)

async def login(request):
    try:
        code=  request.query.get('code')
        state=  request.query.get('state')
    except:
        return web.HTTPInternalServerError()
    global client_id
    global client_secret

    authorization = 'Basic ' + base64.b64encode(f"{client_id}:{client_secret}".encode('ascii')).decode('ascii')

    base: URL = URL('https://ticktick.com/oauth/token')
    url = base.with_query(dict(
        code=code,
        grant_type="authorization_code",
        redirect_uri="http://localhost:8080/login"
    ))

    headers={"Content-Type": "application/x-www-form-urlencoded",
             'Authorization': authorization}

    async with ClientSession() as session:
        async with session.post(url, headers=headers) as response:
            
            print(response.status)
            print(await response.text())
            js = await response.json()
            access_token = js["access_token"]
            print(f"Token: {access_token}")

    raise GracefulExit()
    request.app['shutdown_event'].set()
    return web.Response(text="ok", status=200)


app = web.Application()

app.add_routes([
    web.get("/auth", auth),
    web.get('/login', login)
])

if __name__ == '__main__':
    print(f"The server is starting, please visit http://0.0.0.0:8080/auth in your browser and proceed with authentication")
    app["shutdown_event"] = Event()

    web.run_app(app)

    print("Ending script")
    


