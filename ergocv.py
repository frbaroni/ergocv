#!/usr/bin/python3
import sys
import getopt
import flask
import ecv

DEFAULT_PORT = 35275 # Flask in Phone Keypad

app = flask.Flask(__name__)
@app.route('/')
def index():
    return flask.render_template('app.html')

ergoCv = ecv.ErgoCV()

def usage():
    print("""Usage: python3 ergocv.py [options]
    Options:
        -p port, --port port  change the port number, default to {0}
        -f, --flask-debug     enable flask debug
        -e, --ecv-debug       enable ErgoCV debug
    """.format(DEFAULT_PORT))

def main(argv):
    port = DEFAULT_PORT # Flask in Phone Keypad

    try:
        opts, args = getopt.getopt(argv, "hfep:", ["help", "flask-debug", "ecv-debug", "port="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-f", "--flask-debug"):
            print("Flask debug enabled")
            app.config['DEBUG'] = True
        elif opt in ("-e", "--ecv-debug"):
            print("ErgoCV debug enabled")
            ergoCv.debug()
            sys.exit(0)
        elif opt in ("-p", "--port"):
            port = arg
    
    app.run(port=port)

if __name__ == '__main__':
    main(sys.argv[1:])

