import cv2
from ecv_base import ErgoCVBase

MAX_CAMERA_INDEX = 3
MAX_ERRORS = 5
COLOR_ERGO_POSITION = (255, 0, 0)
COLOR_ERGO_GOOD = (0, 255, 0)
COLOR_ERGO_BAD = (0, 0, 255)

class ErgoCV(ErgoCVBase):
    def __init__(self):
        self.hasWindows = False
        self.camera_previews = {}
        self.camera_index = None
        self.camera_image = None
        self.expectedPosition = None
        self.goodErgonomic = False
        self.facePosition = None
        self.errors = 0
        self.haarFace = cv2.CascadeClassifier('./haar/haarcascade_frontalface_default.xml')

    def __del__(self): 
        if self.hasWindows:
            cv2.destroyAllWindows()

    def setExpectedPosition(self, position):
        self.expectedPosition = position

    def getExpectedPosition(self):
        return self.expectedPosition

    def getFacePosition(self):
        return self.facePosition

    def convertImage(self, image, toExtension):
        if image is not None:
            try:
                res, img = cv2.imencode(toExtension, image)
                if res:
                    return img
            except:
                pass
        return None

    def getCameraImage(self, toExtension):
        return self.convertImage(self.camera_image, toExtension)

    def setCameraIndex(self, index):
        self.camera_index = index

    def getCameraIndex(self):
        return self.camera_index

    def loadCameras(self):
        self.camera_previews = {}
        for index in range(MAX_CAMERA_INDEX):
            image = self.capture(index)
            if image is not None:
                self.camera_previews[index] = image
        indexes = list(self.camera_previews.keys())
        return indexes

    def cameraPreview(self, index, toExtension):
        return self.convertImage(self.camera_previews[index], toExtension)

    def isErgonomic(self):
        return self.goodErgonomic

    def capture(self, camera_index):
        try:
            webcam = cv2.VideoCapture(camera_index)
            ret, img = webcam.read()
            webcam.release()
            if ret:
                return img
        except:
            return None

    def show(self, name, img):
        cv2.imshow(name, img)
        self.hasWindows = True

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

    def processImage(self, img):
        faces = self.detectFaces(img)
        if len(faces) == 1:
            self.facePosition = faces[0]
            if self.expectedPosition is None:
                self.expectedPosition = faces[0]
            self.drawRect(img, self.expectedPosition, COLOR_ERGO_POSITION, 8)

            diff = self.facePosition - self.expectedPosition
            self.goodErgonomic = not (abs(diff[0]) > 30 or abs(diff[3]) > 20)

            self.drawRect(img, self.facePosition,
                    COLOR_ERGO_GOOD if self.goodErgonomic else COLOR_ERGO_BAD,
                    2)

            self.img = img
            self.errors = 0

    def registerError(self):
        self.errors += 1
        print('Warning! Error reading the video camera! ({0}/{1})'.format(
            self.errors,
            MAX_ERRORS))
        if self.errors > MAX_ERRORS:
            self.goodErgonomic = False
            self.img = None
            print('Warning! Too many errors reading the video camera!')

    def update(self):
        if self.camera_index is not None:
            img = self.capture(self.camera_index)
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
                self.expectedPosition = self.facePosition
            if self.facePosition is not None:
                print('{0} ergo: {1} current: {2}'.format(
                    'GOOD' if self.isErgonomic() else 'BAD',
                    self.expectedPosition,
                    self.facePosition
                    ))
            if self.img is not None:
                self.show('ErgoCV - Debug, [a] to adjust, [q] to exit', self.img)
