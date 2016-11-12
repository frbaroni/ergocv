import cv2
from ecv_base import ErgoCVBase

MAX_ERRORS = 5
COLOR_ERGO_POSITION = (255, 0, 0)
COLOR_ERGO_GOOD = (0, 255, 0)
COLOR_ERGO_BAD = (0, 0, 255)

class ErgoCV(ErgoCVBase):
    def __init__(self, camera_index):
        self.camera_index = camera_index
        self.hasWindows = False
        self.ergoPosition = None
        self.goodErgonomic = False
        self.currentPosition = None
        self.img = None
        self.errors = 0
        self.haarFace = cv2.CascadeClassifier('./haar/haarcascade_frontalface_default.xml')

    def __del__(self): 
        if self.hasWindows:
            cv2.destroyAllWindows()

    def setErgoPosition(self, ergoPosition):
        self.ergoPosition = ergoPosition

    def getErgoPosition(self):
        return self.ergoPosition

    def getCurrentPosition(self):
        return self.currentPosition

    def getImage(self, toExtension):
        try:
            res, img = self.convert(self.img, toExtension)
            if res:
                return img
        except:
            pass
        return None

    def setCameraIndex(self, camera_index):
        self.camera_index = camera_index

    def getCameraIndex(self):
        return self.camera_index

    def capture(self):
        try:
            webcam = cv2.VideoCapture(self.camera_index)
            ret, img = webcam.read()
            webcam.release()
            if ret:
                return img
        except:
            return None

    def show(self, name, img):
        cv2.imshow(name, img)
        self.hasWindows = True

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

    def isGoodErgonomic(self):
        return self.goodErgonomic

    def processImage(self, img):
        faces = self.detectFaces(img)
        if len(faces) == 1:
            self.currentPosition = faces[0]
            if self.ergoPosition is None:
                self.ergoPosition = faces[0]
            self.drawRect(img, self.ergoPosition, COLOR_ERGO_POSITION, 8)

            diff = self.currentPosition - self.ergoPosition
            self.goodErgonomic = not (abs(diff[0]) > 30 or abs(diff[3]) > 20)

            self.drawRect(img, self.currentPosition,
                    COLOR_ERGO_GOOD if self.goodErgonomic else COLOR_ERGO_BAD,
                    2)

            self.img = img
            self.errors = 0

    def registerError(self):
        self.errors += 1
        if self.errors > MAX_ERRORS:
            self.goodErgonomic = False
            self.img = None
            print('Warning! Too many errors reading the video camera!')

    def update(self):
        img = self.capture()
        if img is not None:
            self.processImage(img)
        else:
            self.registerError()

    def run_debug(self):
        key = ''
        while key != 'q':
            key = self.keyPressed(500)
            self.update()
            if key == 'a':
                self.ergoPosition = self.currentPosition
            if self.currentPosition is not None:
                print('{0} ergo: {1} current: {2}'.format(
                    'GOOD' if self.isGoodErgonomic() else 'BAD',
                    self.ergoPosition,
                    self.currentPosition
                    ))
            if self.img is not None:
                self.show('ErgoCV - Debug, [a] to adjust, [q] to exit', self.img)
