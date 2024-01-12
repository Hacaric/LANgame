import socketio
from aiohttp import web

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

async def index(request):
    """Serve the client-side application."""
    with open('index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

@sio.event
async def connect(sid, environ, auth):
    print('connect ', sid)
    await sio.emit('my event', {'data': 'foobar'})

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    web.run_app(app)
