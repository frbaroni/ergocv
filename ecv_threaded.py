import time
import threading
import cv2
from ecv_core import ErgoCVBase, ErgoCV

class ErgoCVThreaded(ErgoCVBase):
    class Container(threading.Thread):
        def __init__(self, ergoCV, tick_delay):
            self.lock = threading.RLock()
            threading.Thread.__init__(self)
            self.tick_delay = tick_delay
            self.terminated = False
            self.ergoCV = ergoCV

        def run(self):
            while not self.terminated:
                self.lock.acquire()
                self.ergoCV.update()
                print('{0} ergo: {1} current: {2}'.format(
                    "GOOD" if self.ergoCV.good_position() else "BAD",
                    self.ergoCV.getErgoPosition(),
                    self.ergoCV.getCurrentPosition()
                    ))
                self.lock.release()
                time.sleep(self.tick_delay)

        def setTickDelay(self, tick_delay):
            self.tick_delay = tick_delay

    def __init__(self):
        self.ergoCV = None
        self.thread = None
    
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

    def start(self, camera_index, tick_delay):
        self.ergoCV = ErgoCV(camera_index)
        self.thread = ErgoCVThreaded.Container(self.ergoCV, tick_delay)
        self.thread.start()

    def setErgoPosition(self, ergoPosition):
        self.lockedDo(lambda: self.ergoCV.setErgoPosition(ergoPosition))

    def getErgoPosition(self):
        return self.lockedCall(lambda: self.ergoCV.getErgoPosition())

    def getCurrentPosition(self):
        return self.lockedCall(lambda: self.ergoCV.getCurrentPosition())

    def setTickDelay(self, tick_delay):
        self.lockedDo(lambda: self.thread.setTickDelay(tick_delay))

    def getImage(self, toExtension):
        return self.lockedCall(lambda: self.ergoCV.getImage(toExtension))

    def good_position(self):
        return self.lockedCall(lambda: self.ergoCV.good_position())

    def update(self):
        self.lockedDo(lambda: self.ergoCV.update())
