import cv2

class ErgoCVCore:
    def __init__(self):
        self.webcam = cv2.VideoCapture(0)
        self.hasWindows = False
        self.ergoPosition = None
        self.currentPosition = None
        self.img = None
        self.haarFace = cv2.CascadeClassifier('./haar/haarcascade_frontalface_default.xml')

    def __del__(self): 
        self.webcam.release()
        if self.hasWindows:
            cv2.destroyAllWindows()

    def setErgoPosition(self, ergoPosition):
        self.ergoPosition = ergoPosition

    def getErgoPosition(self, ergoPosition):
        return self.ergoPosition

    def getCurrentPosition(self):
        return self.currentPosition

    def getImage(self, toExtension):
        return self.convert(self.img, toExtension)

    def capture(self):
        ret, img = self.webcam.read()
        if ret:
            return img
        else:
            return None

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

    def drawRect(self, img, dimensions, color = (255, 255, 255), tickness = 3):
        (left, top, width, height) = dimensions
        right = left + width
        bottom = top + height
        cv2.rectangle(img, (left, top), (right, bottom), color, tickness)

    def good_position(self):
        diff = self.currentPosition - self.ergoPosition
        return not (abs(diff[0]) > 30 or abs(diff[3]) > 20)

    def update(self):
        img = self.capture()
        if img is not None:
            faces = self.detectFaces(img)
            if len(faces) == 1:
                self.currentPosition = faces[0]
                if self.ergoPosition is None:
                    self.ergoPosition = faces[0]
                self.drawRect(img, self.ergoPosition, (255, 0, 0), 8)
                self.drawRect(img, self.currentPosition, (0, 0, 255), 2)
                self.img = img


    def run_debug(self):
        key = ''
        while key != 'q':
            key = self.keyPressed(60)
            self.update()
            if key == 'a':
                self.ergoPosition = self.currentPosition
            print('{0} ergo: {1} current: {2}'.format(
                "GOOD" if self.good_position() else "BAD",
                self.ergoPosition,
                self.currentPosition
                ))
            self.show('Debug, [a] to adjust, [q] to exit', self.img)

