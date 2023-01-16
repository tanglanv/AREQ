import cv2 as cv
import numpy as np
import constants as cst


class Camera:
    def __init__(self, id):
        if not hasattr(self, "trials"):
            self.trials = 0

        self.id = id

        print("Opening camera:", self.id)
        try:
            self.cap = cv.VideoCapture(self.id, cv.CAP_MSMF)
        except:
            print("Failed to open camera:", self.id)
            self.nextCamera()

        # If the camera is not opened, try to open the next one
        if not self.cap.isOpened():
            print("Failed to open camera:", self.id)
            self.nextCamera()

        # Set the camera exposure
        self.cap.set(15, -4)

    def getFrame(self):
        # Empty the image buffer
        for i in range(10):
            self.cap.grab()

        ret, frame = self.cap.read()
        if ret:
            cv.imshow(cst.WINDOW_MAIN, frame)
            cv.waitKey(1)
            return frame
        else:
            return None

    def release(self):
        self.cap.release()

    def nextCamera(self):
        self.id = self.id + 1
        if self.id >= 10:
            self.id = 0
            self.trials += 1
            if self.trials >= 5:
                print("Failed to open cameras. Exiting.")
                exit()

        self.cap.release()
        self.__init__(self.id)

    def release(self):
        self.cap.release()


# Test function in case this file is called directly
if __name__ == "__main__":
    # Open the camera and display it until the user presses escape
    cam = Camera(0)
    while True:
        frame = cam.getFrame()
        if frame is not None:
            cv.imshow("Camera", frame)
        if cv.waitKey(1) == 27:
            break
    cam.release()
    cv.destroyAllWindows()
    print("Camera released.")
    exit()
