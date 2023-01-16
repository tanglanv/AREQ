import constants as cst
import numpy as np

import cv2 as cv
import cv2.aruco as aruco


class Projector:
    def __init__(self):

        self.matDraw = np.zeros((cst.PROJ_HEIGHT, cst.PROJ_WIDTH, 3), np.uint8)
        self.matDraw[:] = cst.GRAY

        cv.namedWindow(cst.WINDOW_PROJECTOR, cv.WINDOW_NORMAL)
        cv.moveWindow(cst.WINDOW_PROJECTOR, cst.FIRST_SCREEN_WIDTH, 0)
        cv.setWindowProperty(cst.WINDOW_PROJECTOR, cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)

    def draw(self, mat):
        # Warp the image in the projector space
        self.matDraw = cv.warpPerspective(mat, self.R2P, cst.PROJ_SIZE)

        cv.imshow(cst.WINDOW_PROJECTOR, self.matDraw)
        cv.waitKey(1)

    def drawWhite(self):
        self.matDraw[:] = cst.WHITE
        cv.imshow(cst.WINDOW_PROJECTOR, self.matDraw)
        cv.waitKey(1)

    def drawBlack(self):
        self.matDraw[:] = cst.BLACK
        cv.imshow(cst.WINDOW_PROJECTOR, self.matDraw)
        cv.waitKey(1)

    def release(self):
        # Close all windows
        cv.destroyAllWindows()

    def drawMarkers(self):
        newPts = []
        newIds = []

        self.matDraw = np.zeros((cst.PROJ_HEIGHT, cst.PROJ_WIDTH, 3), np.uint8)
        self.matDraw[:] = cst.WHITE

        nMarker = int(np.random.randint(1, 250))

        sizeMarker = int(self.matDraw.shape[0] / 15.0)
        nMarkersX = int(self.matDraw.shape[1] / 1.5 / sizeMarker)
        nMarkersY = int(self.matDraw.shape[0] / 1.5 / sizeMarker)

        for i in range(nMarkersX):
            for j in range(nMarkersY):
                newIds.append(nMarker)

                arucoDict = aruco.Dictionary_get(aruco.DICT_5X5_250)

                corner = ((0.5 + i * 1.5) * sizeMarker, (0.5 + j * 1.5) * sizeMarker)

                # Draw specific markers
                img = aruco.drawMarker(arucoDict, nMarker, int(sizeMarker))

                # Add third channel
                img = cv.cvtColor(img, cv.COLOR_GRAY2BGR)

                # Draw the marker in the projector (! x and y are inverted)
                self.matDraw[int(corner[1]):int(corner[1] + sizeMarker),
                int(corner[0]):int(corner[0] + sizeMarker)] = img

                newPts.append(corner)
                nMarker = (nMarker + 1) % 250

        cv.imshow(cst.WINDOW_PROJECTOR, self.matDraw)
        cv.waitKey(1)

        return newPts, newIds

    def checkCalibration(self):

        # Create an image in real space
        mat = np.zeros(cst.BOARD_MAX_SIZE + (3,), np.uint8)
        mat[:] = cst.WHITE

        # Draw a rectangle around the board
        cv.rectangle(mat, (0, 0), (cst.BOARD_MAX_SIZE[0], cst.BOARD_MAX_SIZE[1]), cst.BLUE, cst.LINE_SIZE)

        # Draw a square for the playing area
        cv.rectangle(mat, (cst.EDGE_SIZE[0], cst.EDGE_SIZE[1]),
                     (cst.BOARD_MAX_SIZE[0] - cst.EDGE_SIZE[0], cst.BOARD_MAX_SIZE[1] - cst.EDGE_SIZE[1]), cst.RED,
                     cst.LINE_SIZE)

        # Warp the image in the projector space and display it
        self.matDraw = cv.warpPerspective(mat, self.R2P, cst.PROJ_SIZE)
        cv.imshow(cst.WINDOW_PROJECTOR, self.matDraw)
        cv.waitKey(1)


# Test function in case this file is called directly
if __name__ == "__main__":
    # Create the projector
    proj = Projector()

    # Try to draw the black screen
    try:
        proj.drawBlack()
    except:
        print("Failed to draw black screen.")

    cv.waitKey(1000)

    # Try to draw the markers
    try:
        proj.drawMarkers()
    except:
        print("Failed to draw the markers.")

    cv.waitKey(1000)

    # Try to draw the calibration image
    try:
        proj.checkCalibration()
    except:
        print("Failed to draw the calibration image.")

    cv.waitKey(1000)