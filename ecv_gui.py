#!/usr/bin/python3
import datetime
import flask
from ecv_threaded import ErgoCVThreaded

app = flask.Flask(__name__)
ergoCV = ErgoCVThreaded()

@app.route('/')
def index():
    return flask.render_template('app.html')

@app.route('/image', methods=['GET'])
def image():
    result, img = ergoCV.getImage('.jpg')
    response = flask.Response(img.tobytes(), mimetype="image/jpg")
    response.headers['Last-Modified'] = datetime.datetime.now()
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

def run_gui(port, debug):
    app.config['DEBUG'] = debug
    camera_index = 0
    ergoCV.start(camera_index)
    app.run(port=port)
