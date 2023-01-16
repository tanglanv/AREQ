import numpy as np
import constants as cst
import cv2 as cv


class TicTacToe:
    def __init__(self):
        self.board = np.zeros((3, 3), dtype=int)
        self.turn = 1
        self.winner = 0
        self.game_over = False

    def getEQ(self):
        self.imgEQ = np.zeros(cst.BOARD_MAX_SIZE + (3,), dtype=np.uint8)
        self.imgEQ[:] = cst.GRAY

        # Draw the lines
        for i in range(5):
            cv.line(self.imgEQ, (cst.MARGE_V + i * (cst.BOX_SIZE_X + cst.INTER_BOX), cst.MARGE_V),
                    (cst.MARGE_H + i * (cst.BOX_SIZE_X + cst.INTER_BOX), cst.BOARD_MAX_SIZE[1] - cst.MARGE_V), cst.BLACK,
                    cst.LINE_SIZE)
        return self.imgEQ

    def getBoard(self):
        self.imgBoard = np.zeros(cst.BOARD_MAX_SIZE + (3,), dtype=np.uint8)
        self.imgBoard[:] = cst.GRAY
        self.imgBoard[cst.EDGE_SIZE[0]:cst.BOARD_MAX_SIZE[0] - cst.EDGE_SIZE[0],
        cst.EDGE_SIZE[1]:cst.BOARD_MAX_SIZE[1] - cst.EDGE_SIZE[1]] = cst.WHITE

        # Draw the squares
        for i in range(3):
            for j in range(3):
                if self.board[i, j] == 1:
                    cv.rectangle(self.imgBoard,
                                 (cst.EDGE_SIZE[0] + cst.SQUARE_SIZE * j, cst.EDGE_SIZE[1] + cst.SQUARE_SIZE * i), (
                                 cst.EDGE_SIZE[0] + cst.SQUARE_SIZE * (j + 1),
                                 cst.EDGE_SIZE[1] + cst.SQUARE_SIZE * (i + 1)), cst.RED, -1)
                elif self.board[i, j] == 2:
                    cv.rectangle(self.imgBoard,
                                 (cst.EDGE_SIZE[0] + cst.SQUARE_SIZE * j, cst.EDGE_SIZE[1] + cst.SQUARE_SIZE * i), (
                                 cst.EDGE_SIZE[0] + cst.SQUARE_SIZE * (j + 1),
                                 cst.EDGE_SIZE[1] + cst.SQUARE_SIZE * (i + 1)), cst.BLUE, -1)

        # Draw the lines
        for i in range(1, 3):
            cv.line(self.imgBoard, (cst.EDGE_SIZE[0] + i * cst.SQUARE_SIZE, cst.EDGE_SIZE[1]),
                    (cst.EDGE_SIZE[0] + i * cst.SQUARE_SIZE, cst.BOARD_MAX_SIZE[1] - cst.EDGE_SIZE[1]), cst.BLACK,
                    cst.LINE_SIZE)
            cv.line(self.imgBoard, (cst.EDGE_SIZE[0], cst.EDGE_SIZE[1] + i * cst.SQUARE_SIZE),
                    (cst.BOARD_MAX_SIZE[0] - cst.EDGE_SIZE[0], cst.EDGE_SIZE[1] + i * cst.SQUARE_SIZE), cst.BLACK,
                    cst.LINE_SIZE)

        return self.imgBoard

    def getPosition(self, pos):
        return (int((pos[0] - cst.EDGE_SIZE[0]) / cst.SQUARE_SIZE), int((pos[1] - cst.EDGE_SIZE[1]) / cst.SQUARE_SIZE))

    def play(self, pos):
        if self.game_over:
            return
        j, i = self.getPosition(pos)
        if self.board[i, j] == 0:
            print("Move played:", i, j)
            self.board[i, j] = self.turn
            self.turn = 3 - self.turn
            self.checkWinner()
        else:
            return

    def checkWinner(self):
        # Check rows
        for i in range(3):
            if self.board[i, 0] != 0 and self.board[i, 0] == self.board[i, 1] and self.board[i, 1] == self.board[i, 2]:
                self.winner = self.board[i, 0]
                self.game_over = True
                return

        # Check columns
        for j in range(3):
            if self.board[0, j] != 0 and self.board[0, j] == self.board[1, j] and self.board[1, j] == self.board[2, j]:
                self.winner = self.board[0, j]
                self.game_over = True
                return

        # Check diagonals
        if self.board[0, 0] != 0 and self.board[0, 0] == self.board[1, 1] and self.board[1, 1] == self.board[2, 2]:
            self.winner = self.board[0, 0]
            self.game_over = True
            return
        if self.board[0, 2] != 0 and self.board[0, 2] == self.board[1, 1] and self.board[1, 1] == self.board[2, 0]:
            self.winner = self.board[0, 2]
            self.game_over = True
            return

        # Check if the board is full
        if np.count_nonzero(self.board) == 9:
            self.winner = 0
            self.game_over = True
            return

        self.game_over = False

    def reset(self):
        self.board = np.zeros((3, 3), dtype=int)
        self.turn = 1
        self.winner = 0
        self.game_over = False

    def getResult(self):
        if self.winner == 0:
            return "Draw"
        elif self.winner == 1:
            return "Red wins"
        elif self.winner == 2:
            return "Blue wins"
        else:
            return "Error"

    def isInTheBoard(self, pos):
        if pos is None:
            return False

        i, j = self.getPosition(pos)
        if i >= 0 and i < 3 and j >= 0 and j < 3:
            return True
        else:
            return False

if __name__ == "__main__":
    # Create the projector
    game = TicTacToe()
    EQ = game.getEQ()
    cv.imshow(cst.WINDOW_PROJECTOR, EQ)
    cv.waitKey(0)