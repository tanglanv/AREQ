import numpy as np
import constants as cst
import cv2 as cv


class EQBoard:
    def __init__(self):
        self.EQValues = [0.0, 0.5, 1, 0.75, 0]
        self.soundValues = [0.0,0.0,0.0,0.0,0.0]

    def getEQ(self):
        self.imgEQ = np.zeros(cst.BOARD_MAX_SIZE + (3,), dtype=np.uint8)
        self.imgEQ[:] = cst.GRAY

        # # Draw the lines
        # for i in range(5):
        #     cv.line(self.imgEQ, (cst.MARGE_H + i * (cst.BOX_SIZE_X + cst.INTER_BOX), cst.MARGE_V),
        #             (cst.MARGE_H + i * (cst.BOX_SIZE_X + cst.INTER_BOX), cst.BOARD_MAX_SIZE[0] - cst.MARGE_V), cst.BLACK,
        #             cst.LINE_SIZE)

        # Draw the boxes
        for i in range(5):
            self.drawBoxes(i)

        return self.imgEQ

    def drawBoxes(self, i):
        # Corners of the Boxe
        x1 = cst.MARGE_H + (cst.BOX_SIZE_X + cst.INTER_BOX) * i
        y1 = cst.MARGE_V
        x2 = cst.MARGE_H + (cst.BOX_SIZE_X + cst.INTER_BOX) * i + cst.BOX_SIZE_X
        y2 = cst.BOARD_MAX_SIZE[0] - cst.MARGE_V

        # Draw Background
        cv.rectangle(self.imgEQ, (x1, y1), (x2, y2), cst.DARK_GRAY, -1)

        mrg = cst.INSIDE_BOX_MARGE
        # Draw Lines
        cv.line(self.imgEQ, (x1 + mrg, y1 + mrg), (x1 + mrg, y2 - mrg), cst.BLACK, cst.LINE_SIZE)

        # Draw Boxe
        # self.updateBar()

        # Draw Cursor
        y_center = y1 + int(mrg + (y2 - y1 - 2 * mrg) * (1 - self.EQValues[i]))
        xc1 = x1 + mrg - cst.CURSOR_X
        yc1 = y_center - cst.CURSOR_Y
        xc2 = x1 + mrg + cst.CURSOR_X
        yc2 = y_center + cst.CURSOR_Y
        # print(x1, y1, x2, y2)
        cv.rectangle(self.imgEQ, (xc1, yc1), (xc2, yc2), cst.BLUE, -1)

        y = y1 + int(mrg + (y2 - y1 - 2 * mrg) * (1 - self.soundValues[i]))

        if self.soundValues[i] <= 0.4:
            color = cst.GREEN
        elif 0.4 < self.soundValues[i] <= 0.6:
            color = cst.YELLOW
        elif 0.6 < self.soundValues[i]:
            color = cst.RED
        cv.rectangle(self.imgEQ, (x1 + 2 * mrg, y), (x2 - mrg, y2 - mrg), color, -1)

    def isInABoxe(self, pos):

        def getValue(y):
            y1 = cst.MARGE_V
            y2 = cst.BOARD_MAX_SIZE[0] - cst.MARGE_V
            mrg = cst.INSIDE_BOX_MARGE

            if y < y1 + mrg:
                return 1
            elif y > y2 - mrg:
                return 0
            return 1 - (y - y1 - mrg) / (y2 - y1 - 2 * mrg)

        if pos is None:
            return False, 0, 0

        for i in range(5):
            x1 = cst.MARGE_H + (cst.BOX_SIZE_X + cst.INTER_BOX) * i
            y1 = cst.MARGE_V
            x2 = cst.MARGE_H + (cst.BOX_SIZE_X + cst.INTER_BOX) * i + cst.BOX_SIZE_X
            y2 = cst.BOARD_MAX_SIZE[0] - cst.MARGE_V

            x = pos[0]
            y = pos[1]

            if x1 < x < x2 and y1 < y < y2:
                value = getValue(y)
                return True, i, value

        return False, 0, 0

    def changeCursorValue(self, i, value):
        self.EQValues[i] = value

    def updateSoundValue(self,values):
        self.soundValues = values



if __name__ == "__main__":
    # Create the projector
    game = EQBoard()
    EQ = game.getEQ()
    cv.imshow(cst.WINDOW_PROJECTOR, EQ)

    print(game.isInABoxe((50, 250)))
    print(game.isInABoxe((50, 459)))
    print(game.isInABoxe((50, 120)))

    cv.waitKey(0)
