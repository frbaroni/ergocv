import cv2
import sys

COLOR_ERGO_POSITION = (255, 0, 0)
COLOR_ERGO_GOOD = (0, 255, 0)
COLOR_ERGO_BAD = (0, 0, 255)


class CameraTools:
    MAX_CAMERA_INDEX = 3

    def loadPreviews(self):
        previews = {}
        for i in range(self.MAX_CAMERA_INDEX):
            previews[i] = self.capture(i)
        return previews

    def capture(self, camera):
        try:
            webcam = cv2.VideoCapture(camera)
            ret, img = webcam.read()
            webcam.release()
            if ret:
                return img
        except:
            pass
        return None

    def convert(self, image, mime):
        if image is not None:
            try:
                res, img = cv2.imencode(mime, image)
                if res:
                    return img
            except:
                pass
        return None

    def drawRect(self, img, dimensions, color=(255, 255, 255), tickness=3):
        (left, top, width, height) = dimensions
        right = left + width
        bottom = top + height
        cv2.rectangle(img, (left, top), (right, bottom), color, tickness)


class FaceDetector:
    def __init__(self):
        self.haarFace = cv2.CascadeClassifier(
            './haar/haarcascade_frontalface_default.xml'
        )

    def detect(self, image):
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return self.haarFace.detectMultiScale(img_gray)


class ErgonomicHelper:
    def __init__(self):
        self.top = (0, 0)
        self.left = (0, 0)
        self.bottom = (0, 0)
        self.right = (0, 0)
        self.ergonomic = False

    def setErgonomicTop(self, top, height):
        self.top = (top, height)

    def getErgonomicTop(self):
        return self.top

    def setErgonomicLeft(self, left, width):
        self.left = (left, width)

    def getErgonomicLeft(self):
        return self.left

    def setErgonomicBottom(self, bottom, height):
        self.bottom = (bottom, height)

    def getErgonomicBottom(self):
        return self.bottom

    def setErgonomicRight(self, right, width):
        self.right = (right, width)

    def getErgonomicRight(self):
        return self.right

    def isErgonomic(self):
        return self.ergonomic

    def update(self, top, left, bottom, right):
        def inside(value, limits):
            return (
                       (self.limits[0] <= value)
                       and
                       (value <= self.limits[0] + self.limits[1])
                   )
        return (
                inside(top, self.top) and
                inside(left, self.left) and
                inside(right, self.right) and
                inside(bottom, self.bottom))

    def drawErgonomics(self, image):
        pass


class ErgoCV:
    def __init__(self):
        self.camera = 0
        self.faceDetector = FaceDetector()
        self.cameraTools = CameraTools()
        self.ergoHelper = ErgonomicHelper()

    def setPrimaryCamera(self, camera):
        self.camera = camera

    def getPrimaryCamera(self):
        return self.camera

    def run(self):
        image = self.cameraTools.capture(self.camera)
        if not image:
            print("Cannot capture from camera {}".format(self.camera),
                  file=sys.stderr)
            return
        faces = self.faceDetector.detect(image)
        if len(faces) == 0:
            print('Detected no faces at the captured image', file=sys.stderr)
            return
        if len(faces) > 1:
            print('Detected many faces at the captured image', file=sys.stderr)
            return
        if len(faces) == 1:
            top, left, bottom, right = faces[1]
            self.ergoHelper.update(top, left, bottom, right)
