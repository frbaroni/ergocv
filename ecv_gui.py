#!/usr/bin/python3
import datetime
import flask
from ecv_threaded import ErgoCVThreaded

MIMEEXT = '.jpg'
MIMETYPE = "image/jpg"

app = flask.Flask(__name__)
ergoCV = ErgoCVThreaded()


@app.route('/')
def index():
    return flask.render_template('app.html')


@app.route('/camera/indexes')
def camera_indexes():
    indexes = ergoCV.loadCameras()
    return flask.jsonify(cameras=indexes)


@app.route('/camera/preview/<int:index>')
def camera_preview(index):
    img = ergoCV.cameraPreview(index, MIMEEXT)
    return imageResponse(img)


@app.route('/image', methods=['GET'])
def image():
    ergoCV.update()
    img = ergoCV.getImage(MIMEEXT)
    return imageResponse(img)


def imageResponse(image):
    if image is not None:
        response = flask.Response(image.tobytes(), mimetype=MIMETYPE)
        response.headers['Last-Modified'] = datetime.datetime.now()
        response.headers[
            'Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
    else:
        return flask.send_file("./static/oops.jpg", mimetype=MIMETYPE)


def run_gui(port, debug):
    app.config['DEBUG'] = debug
    ergoCV.setTickDelay(60)
    ergoCV.start()
    app.run(port=port)
