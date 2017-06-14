import time
import threading
import cv2
from ecv_base import ErgoCVBase
from ecv_core import ErgoCV

class ErgoCVThreaded(ErgoCVBase):
    class Container(threading.Thread):
        def __init__(self, ergoCV):
            self.lock = threading.RLock()
            threading.Thread.__init__(self)
            self.tick_delay = 1
            self.terminated = False
            self.ergoCV = ergoCV

        def run(self):
            while not self.terminated:
                self.lock.acquire()
                self.ergoCV.update()
                print('{0} ergo: {1} current: {2}'.format(
                    "GOOD" if self.ergoCV.isErgonomic() else "BAD",
                    self.ergoCV.getExpectedPosition(),
                    self.ergoCV.getFacePosition()
                    ))
                self.lock.release()
                time.sleep(self.tick_delay)

        def setTickDelay(self, tick_delay):
            self.tick_delay = tick_delay

    def __init__(self):
        self.ergoCV = ErgoCV()
        self.thread = ErgoCVThreaded.Container(self.ergoCV)

    def start(self):
        self.thread.start()
    
    def lockedDo(self, fn):
        if self.thread:
            self.thread.lock.acquire()
            fn()
            self.thread.lock.release()

    def lockedCall(self, fn):
        if self.thread:
            self.thread.lock.acquire()
            res = fn()
            self.thread.lock.release()
            return res
        else:
            return None

    def setExpectedPosition(self, position):
        self.lockedDo(lambda: self.ergoCV.setExpectedPosition(position))

    def getExpectedPosition(self):
        return self.lockedCall(lambda: self.ergoCV.getExpectedPosition())

    def getFacePosition(self):
        return self.lockedCall(lambda: self.ergoCV.getFacePosition())

    def setTickDelay(self, tick_delay):
        self.lockedDo(lambda: self.thread.setTickDelay(tick_delay))

    def getCameraImage(self, toExtension):
        return self.lockedCall(lambda: self.ergoCV.getCameraImage(toExtension))

    def setCameraIndex(self, index):
        self.lockedDo(lambda: self.ergoCV.setCameraIndex(index))

    def getCameraIndex(self):
        return self.lockedCall(lambda: self.ergoCV.getCameraIndex())

    def loadCameras(self):
        return self.lockedCall(lambda: self.ergoCV.loadCameras())

    def cameraPreview(self, index, toExtension):
        return self.lockedCall(lambda: self.ergoCV.cameraPreview(index, toExtension))

    def isErgonomic(self):
        return self.lockedCall(lambda: self.ergoCV.isErgonomic())

    def update(self):
        self.lockedDo(lambda: self.ergoCV.update())
