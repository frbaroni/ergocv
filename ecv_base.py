class ErgoCVBase:
    """
        Base interface
    """
    def __init__(self, camera_index):
        """
            Initialize with given camera index.
        """
        pass
    def setErgoPosition(self, ergoPosition):
        """
            Set the ergonomic position, where the detected face will be
            matched against.
        """
        pass
    def getErgoPosition(self):
        """
            Get the ergonomic position, where the detected face will be
            matched against.
        """
        pass
    def getCurrentPosition(self):
        """
            Return the last detected face position.
        """
        pass
    def getImage(self, toExtension):
        """
            Return the last valid image, containing the face and ergo
            rectangle markers.
        """
        pass
    def setCameraIndex(self, camera_index):
        """
            Set the camera index to fetch images.
        """
        pass
    def getCameraIndex(self):
        """
            Get the camera index which we use to fetch images.
        """
        pass
    def isGoodErgonomic(self):
        """
            Return if the last ergonomic was inside the ergo position.
        """
        pass
    def update(self):
        """
            Capture new image and try to find a face in it,
            validating if the ergo is in good position.
        """
        pass
