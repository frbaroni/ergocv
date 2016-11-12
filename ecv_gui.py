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
    mimetype="image/jpg"
    ergoCV.update()
    img = ergoCV.getImage('.jpg')
    if img is not None:
        response = flask.Response(img.tobytes(), mimetype=mimetype)
        response.headers['Last-Modified'] = datetime.datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
    else:
        return flask.send_file("./static/oops.jpg", mimetype=mimetype)

def run_gui(port, debug):
    app.config['DEBUG'] = debug
    camera_index = 0
    ergoCV.setTickDelay(60)
    ergoCV.start(camera_index)
    app.run(port=port)
