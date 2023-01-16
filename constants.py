
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

# Windows names
WINDOW_PROJECTOR = "Projector"
WINDOW_MAIN = "Main"

# Marker id for corners
N_MARKER_B1_TL = 25
N_MARKER_B1_TR = 26
N_MARKER_B1_BL = 27
N_MARKER_B1_BR = 28

# Marker position on the board (define the board space units)
BOARD_MAX_SIZE = (500,500)
MARKER_B1_TL = (0,0)
MARKER_B1_BL = (0,BOARD_MAX_SIZE[1])
MARKER_B1_TR = (BOARD_MAX_SIZE[0],0)
MARKER_B1_BR = BOARD_MAX_SIZE

SQUARE_SIZE = 100
LINE_SIZE = 5
EDGE_SIZE = (int((BOARD_MAX_SIZE[0]-3*SQUARE_SIZE)/2), int((BOARD_MAX_SIZE[1]-3*SQUARE_SIZE)/2))