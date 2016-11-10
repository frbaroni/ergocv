#!/usr/bin/python3
import flask
from ecv_core import ErgoCVCore

app = flask.Flask(__name__)

@app.route('/')
def index():
    return flask.render_template('app.html')

@app.route('/image', methods=['GET'])
def image():
    return ''

def run_gui(port, debug):
    app.config['DEBUG'] = debug
    app.run(port=port)
