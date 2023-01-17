import numpy
import cv2

PROJ_WIDTH = 1920
PROJ_HEIGHT = 1080
PROJ_SIZE = (PROJ_WIDTH, PROJ_HEIGHT)

# First screen resolution
FIRST_SCREEN_WIDTH = 1920
FIRST_SCREEN_HEIGHT = 1080

# Colors
GRAY = (203, 214, 218)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (255, 0, 0)
RED = (0, 0, 255)
GREEN = (0, 255, 0)
DARK_GRAY = (175, 177, 179)

# Windows names
WINDOW_PROJECTOR = "Projector"
WINDOW_MAIN = "Main"

# Marker id for corners
N_MARKER_B1_TL = 25
N_MARKER_B1_TR = 26
N_MARKER_B1_BL = 27
N_MARKER_B1_BR = 28

# Marker position on the board (define the board space units) (vertical, horizontal)
BOARD_MAX_SIZE = (500,500)
MARKER_B1_TL = (0,0)
MARKER_B1_BL = (0,BOARD_MAX_SIZE[1])
MARKER_B1_TR = (BOARD_MAX_SIZE[0],0)
MARKER_B1_BR = BOARD_MAX_SIZE

SQUARE_SIZE = 100
LINE_SIZE = 5
# EDGE_SIZE = (int((BOARD_MAX_SIZE[0]-3*SQUARE_SIZE)/2), int((BOARD_MAX_SIZE[1]-3*SQUARE_SIZE)/2))
EDGE_SIZE = (int((BOARD_MAX_SIZE[0]-3*SQUARE_SIZE)/2), int((BOARD_MAX_SIZE[1]-3*SQUARE_SIZE)/2))

MARGE_H = int(BOARD_MAX_SIZE[1]*0.05)
MARGE_V = int(BOARD_MAX_SIZE[0]*0.08)
MARGE = (MARGE_H,MARGE_V)

BOX_SIZE_X = int(BOARD_MAX_SIZE[1]*0.14)
BOX_SIZE_Y = int(BOARD_MAX_SIZE[0]*0.9)
BOX_SIZE = (BOX_SIZE_X, BOX_SIZE_Y)

INTER_BOX = int(BOARD_MAX_SIZE[1]*0.05)

INSIDE_BOX_MARGE = int(BOX_SIZE_X * 0.2)
CURSOR_X =  int(BOX_SIZE_X * 0.15)
CURSOR_Y = int(BOX_SIZE_X * 0.1)