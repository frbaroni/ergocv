import cv2

class ErgoCV:
    def __init__(self):
        self.webcam = cv2.VideoCapture(0)
        self.hasWindows = False
        self.debug_mode = False
        self.position = None
        self.faces = []
        self.img = None
        self.tick = 400
        self.haarFace = cv2.CascadeClassifier('./haar/haarcascade_frontalface_default.xml')

    def __del__(self): 
        self.webcam.release()
        if self.hasWindows:
            cv2.destroyAllWindows()

    def setPosition(self, position):
        self.position = position

    def getPosition(self, position):
        return self.position

    def getFaces(self):
        return self.faces

    def getImage(self, toExtension):
        return self.convert(self.img, toExtension)

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

    def convert(self, img, toExtension):
        return cv2.imencode(toExtension, img)

    def keyPressed(self, delay=10):
        return chr(cv2.waitKey(delay) & 0xFF)

    def detectFaces(self, img):
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.haarFace.detectMultiScale(img_gray)
        return faces

    def haarRect(self, img, dimensions, color = (255, 255, 255), tickness = 3):
        (left, top, width, height) = dimensions
        right = left + width
        bottom = top + height
        cv2.rectangle(img, (left, top), (right, bottom), color, tickness)

    def check(self, face):
        diff = face - self.position
        if abs(diff[0]) > 30 or abs(diff[3]) > 20:
            print('Bad Ergo {0}'.format(diff))
        else:
            print('Ergo Ok {0}'.format(diff))

    def run(self):
        key = ''
        while key != 'q':
            img = self.capture()
            faces = self.detectFaces(img)
            if self.position is not None:
                self.haarRect(img, self.position, (255, 0, 0), 8)
            for face in faces:
                self.haarRect(img, face, (0, 0, 255), 2)
                if (self.position is None) or (key == 'a'):
                    self.position = face
                self.check(face)
                self.img = img
                self.faces = faces
            if self.debug_mode:
                self.show('Faces & Eyes, [a] to adjust, [q] to exit', img)
            key = self.keyPressed(self.tick)

    def debug(self):
        self.debug_mode = True
        self.run()

