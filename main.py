import cv2 as cv
import numpy as np
import time

import constants as cst
import projector
import camera
import coreAR
import ticTacToe

rep=""

# Calibration loop
while rep!="y":
    rep=""
        
    cv.namedWindow(cst.WINDOW_MAIN, cv.WINDOW_NORMAL)

    proj = projector.Projector()
    cam = camera.Camera(1)
    core = coreAR.CoreAR(cam, proj)

    print("Calibrating camera...")
    core.calibrateCamera()
    print("Camera calibrated.")

    print("Calibrating projector...")
    core.calibrateProjector()
    print("Projector calibrated.")

    # Store the transformation matrix for the projector
    proj.R2P = core.R2P

    # Check the calibration
    proj.checkCalibration()
    cv.waitKey(30)

    while rep!="y" and rep!="n":
        print("Is the calibration correct? (y/n)")
        rep = input()

    if rep=="n":
        cam.release()
        del proj, cam, core

# Intialize the game
game = ticTacToe.TicTacToe() 

# Display the board
board = game.getEQ()
proj.draw(board)

# Wait 1s before taking the reference frame
key = cv.waitKey(1000)
core.storeRefFrame()

# Intialise variables
currentMove = [-1, -1]
t = time.time()

# Main loop
while key!=27 and game.game_over==False:

    # Try to find a move (in real space coordinate)
    move = core.findMove()

    # If it's in the board
    if game.isInTheBoard(move):
        # Compute the distance between the current move and the last one
        d = np.linalg.norm(np.array(move)-np.array(currentMove))

        # If the distance is greater than the threshold and is the same for at least 3 seconds
        if d<100 and time.time()-t>3:
            # The move is valid, play it
            game.play(move)

            # Display the board
            proj.draw(game.getEQ())

            # Wait 1s before taking the reference frame
            key = cv.waitKey(1000)
            core.storeRefFrame()

            # Reset variables
            currentMove = [-1, -1]
            t = time.time()

        elif d>100:
            # The move is not the same, store it and reset the timer
            currentMove = move
            t = time.time()

    # If the game is over, display it
    if game.game_over:
        print("Game over.")
        print(game.getResult())
        break

    key = cv.waitKey(100)

cv.destroyAllWindows()
