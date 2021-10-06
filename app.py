import asyncio
import base64
import dash, cv2
import dash_html_components as html
import threading
from Camera import Camera

from dash.dependencies import Output, Input
from quart import Quart, websocket
from dash_extensions import WebSocket

"""Version 2"""
camera = Camera(cv2.VideoCapture(3))

server = Quart(__name__)
n_streams = 2

async def stream(camera, delay=None):
    while True:
        if delay is not None:
            await asyncio.sleep(delay)  # add delay if CPU usage is too high
        frame = camera.get_frame()
        await websocket.send(f"data:image/jpeg;base64, {base64.b64encode(frame).decode()}")


@server.websocket("/stream0")
async def stream0():
    camera = Camera(cv2.VideoCapture(3))
    await stream(camera)


# Create small Dash application for UI.
app = dash.Dash(__name__)
app.layout = html.Div(
    [html.Img(style={'width': '40%', 'padding': 10}, id=f"v{i}") for i in range(n_streams)] +
    [WebSocket(url=f"ws://127.0.0.1:5000/stream{i}", id=f"ws{i}") for i in range(n_streams)]
)
# Copy data from websockets to Img elements.
for i in range(n_streams):
    app.clientside_callback("function(m){return m? m.data : '';}", Output(f"v{i}", "src"), Input(f"ws{i}", "message"))

if __name__ == '__main__':
    threading.Thread(target=app.run_server).start()
    server.run()