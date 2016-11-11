#!/usr/bin/python3
import sys
import getopt
from ecv_core import ErgoCV
from ecv_gui import run_gui

DEFAULT_PORT = 35275 # Flask in Phone Keypad

def usage():
    print("""Usage: python3 ergocv.py [options]
    Options:
        -p port, --port port
        change the port number, default to {0}

        -f, --flask-debug
        enable flask debug

        -e camera_index, --ecv-debug camera_index
        enable ErgoCV debug
    """.format(DEFAULT_PORT))

def main(argv):
    debug = False
    port = DEFAULT_PORT

    try:
        opts, args = getopt.getopt(argv, "hfe:p:", ["help", "flask-debug",
            "ecv-debug=", "port="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-f", "--flask-debug"):
            print("Flask debug enabled")
            debug = True
        elif opt in ("-e", "--ecv-debug"):
            print("ErgoCV debug enabled")
            ergoCv = ErgoCV(int(arg))
            ergoCv.run_debug()
            sys.exit(0)
        elif opt in ("-p", "--port"):
            port = arg
    run_gui(port, debug)

if __name__ == '__main__':
    main(sys.argv[1:])

