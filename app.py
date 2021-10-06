from flask import Flask, render_template, Response
import cv2
from Camera import Camera
from VideoStream import VideoStream
from queue import Queue
import os

# Initialize the Flask app
app = Flask(__name__)

framesNormalQue = Queue(maxsize=0)
print('Queue created')

camera = Camera(cv2.VideoCapture(3), framesNormalQue)
camera.start()
print('Camera thread started')

stream = VideoStream(framesNormalQue)
print('Streams created')

stream.start()
print('Normal stream thread started')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_stream')
def video_stream():
    global stream
    return Response(stream.gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


# d = os.getcwd()


# camera = cv2.VideoCapture(3)

# def gen_livestream():  

#     while True:
#         success, frame = camera.read()
#         ret, buffer = cv2.imencode('.jpg', frame)
#         frame = buffer.tobytes()
#         yield (b'--frame\r\n'
#                 b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') 

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/video_feed')
# def video_feed():
#     return Response(gen_livestream(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)