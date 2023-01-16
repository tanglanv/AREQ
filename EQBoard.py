import numpy as np
import constants as cst
import cv2 as cv

class EQBoard:
    def __init__(self):
        self.EQValues = [0.0,0.5,1,0.75,0]

    def getEQ(self):
        self.imgEQ = np.zeros(cst.BOARD_MAX_SIZE + (3,), dtype=np.uint8)
        self.imgEQ[:] = cst.GRAY

        # # Draw the lines
        # for i in range(5):
        #     cv.line(self.imgEQ, (cst.MARGE_H + i * (cst.BOX_SIZE_X + cst.INTER_BOX), cst.MARGE_V),
        #             (cst.MARGE_H + i * (cst.BOX_SIZE_X + cst.INTER_BOX), cst.BOARD_MAX_SIZE[0] - cst.MARGE_V), cst.BLACK,
        #             cst.LINE_SIZE)

        #Draw the boxes
        for i in range(5):
            self.drawBoxes(i)


        return self.imgEQ


    def drawBoxes(self, i):
        #Corners of the Boxe
        x1 = cst.MARGE_H + (cst.BOX_SIZE_X + cst.INTER_BOX) * i
        y1 = cst.MARGE_V
        x2 = cst.MARGE_H + (cst.BOX_SIZE_X + cst.INTER_BOX) * i + cst.BOX_SIZE_X
        y2 = cst.BOARD_MAX_SIZE[0] - cst.MARGE_V

        # Draw Background
        cv.rectangle(self.imgEQ,(x1,y1), (x2,y2), cst.DARK_GRAY, -1)

        mrg = cst.INSIDE_BOX_MARGE
        # Draw Lines
        cv.line(self.imgEQ, (x1 + mrg, y1 + mrg), (x1 +mrg, y2 - mrg), cst.BLACK, cst.LINE_SIZE)

        # Draw Boxe
        cv.rectangle(self.imgEQ,(x1+2*mrg,y1+mrg),(x2-mrg,y2-mrg), cst.RED, -1)

        # Draw Cursor
        y_center = y1 + int(mrg + (y2-y1 - 2 * mrg) * (1 - self.EQValues[i]))
        xc1 = x1+mrg - cst.CURSOR_X
        yc1 = y_center - cst.CURSOR_Y
        xc2 = x1 +mrg+ cst.CURSOR_X
        yc2 = y_center + cst.CURSOR_Y
        print(xc1, yc1, xc2, yc2)
        cv.rectangle(self.imgEQ, (xc1, yc1), (xc2, yc2), cst.BLUE, -1)

if __name__ == "__main__":
    # Create the projector
    game = EQBoard()
    EQ = game.getEQ()
    cv.imshow(cst.WINDOW_PROJECTOR, EQ)
    cv.waitKey(0)