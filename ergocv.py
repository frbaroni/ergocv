#!/usr/bin/python3
import sys
import getopt
from ecv_core import ErgoCV


def usage():
    print("""Usage: python3 ergocv.py [options]
    Options:
        -h, --help
        this help

        -e camera_index, --ecv camera_index
        enable ErgoCV debug
    """)


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "he:", ["help", "ecv="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-e", "--ecv"):
            print("ErgoCV debug enabled")
            ergoCv = ErgoCV()
            ergoCv.setCameraIndex(int(arg))
            ergoCv.run_debug()
            sys.exit(0)


if __name__ == '__main__':
    main(sys.argv[1:])
