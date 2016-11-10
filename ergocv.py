from flask import Flask, send_file
import cv2


app = Flask(__name__)
@app.route('/')
def index():
    return 'Hello World'

WEBCAM_INDEX = 0

class ErgoCV:
    def __init__(self):
        self.webcam = cv2.VideoCapture(WEBCAM_INDEX)
        self.hasWindows = False

    def __del__(self): 
        self.webcam.release()
        if self.hasWindows:
            cv2.destroyAllWindows()

    def capture(self):
        ret, img = self.webcam.read()
        return img

    def window(self, name):
        return 'ErgoCV - {0}'.format(name)

    def show(self, name, img):
        cv2.imshow(self.window(name), img)
        self.hasWindows = True

    def close(self, name):
        cv2.destroyWindow(self.window(name))

    def keyPressed(self, key, delay=10):
        return cv2.waitKey(delay) & 0xFF == ord(key)

    def run(self):
        initial = None
        haarFace = cv2.CascadeClassifier('./haar/haarcascade_frontalface_default.xml')
        while not self.keyPressed('q', 100):
            img = self.capture()
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = haarFace.detectMultiScale(img_gray)
            for face in faces:
                self.haarRect(img, face, (0, 0, 255))
                if initial is None or self.keyPressed('a'):
                    initial = face
                diff = face - initial
                if abs(diff[0]) > 30 or abs(diff[3]) > 20:
                    print('Oops! {0}'.format(diff))
                else:
                    print('Ok! =] {0}'.format(diff))
            self.show('Faces & Eyes, [a] to adjust, [q] to exit', img)

    def haarRect(self, img, dimensions, color = (255, 255, 255), tick = 3):
        (left, top, width, height) = dimensions
        right = left + width
        bottom = top + height
        cv2.rectangle(img, (left, top), (right, bottom), color, 3)


def main():
    ecv = ErgoCV()
    ecv.run()

main()
