class ErgoCVBase:

    """
        Base interface
    """

    def setExpectedPosition(self, position):
        """
            Set the expected ergonomic position, where the detected face will
            be matched against.
        """
        pass

    def getExpectedPosition(self):
        """
            Get the expected ergonomic position, where the detected face will
            be matched against.
        """
        pass

    def getFacePosition(self):
        """
            Return the last detected face position.
        """
        pass

    def getCameraImage(self, toExtension):
        """
            Return the last valid image, containing the face and ergo
            rectangle markers.
        """
        pass

    def setCameraIndex(self, index):
        """
            Set the camera index to fetch images.
        """
        pass

    def getCameraIndex(self):
        """
            Get the camera index which we use to fetch images.
        """
        pass

    def loadCameras(self):
        """
            Load available camera indexes.
        """
        pass

    def cameraPreview(self, index, toExtension):
        """
            Get the available camera image by index.
        """
        pass

    def isErgonomic(self):
        """
            Return if the last detected face is in ergonomic expected position.
        """
        pass

    def update(self):
        """
            Capture new image and try to find a face in it,
            validating if the ergo is in good position.
        """
        pass
