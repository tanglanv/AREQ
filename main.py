import cv2 as cv
import numpy as np
import time

import constants as cst
import projector
import camera
import coreAR
import EQBoard
import sound

rep = ""

# Calibration loop
while rep != "y":
    rep = ""

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

    while rep != "y" and rep != "n":
        print("Is the calibration correct? (y/n)")
        rep = input()

    if rep == "n":
        cam.release()
        del proj, cam, core

# Intialize the game
eq = EQBoard.EQBoard()
soundCore = sound.Sound("musique1.wav")
soundCore.playsound()

# Display the board
board = eq.getEQ()
proj.draw(board)

# Wait 1s before taking the reference frame
key = cv.waitKey(1000)
core.storeRefFrame()

# Intialise variables
currentMove = [-1, -1]
t = time.time()

update = False

# Main loop
while key != 27:

    # Try to find a move (in real space coordinate)
    move = core.findMove()

    isInABoxe, i, value = eq.isInABoxe(move)

    if isInABoxe:

        # Compute the distance between the current move and the last one
        d = np.linalg.norm(np.array(move) - np.array(currentMove))

        if d < 100 and time.time() - t > 1:
            # change value
            eq.changeCursorValue(i, value)
            print("Values modified : ",value)

            # Display the board
            #proj.draw(eq.getEQ())

            soundCore.set_Gain(i,value)

            # Wait 1s before taking the reference frame
            key = cv.waitKey(1000)
            core.storeRefFrame()

            # Reset variables
            currentMove = [-1, -1]
            t = time.time()
        elif d > 100:
            # The move is not the same, store it and reset the timer
            currentMove = move
            t = time.time()


    eq.updateSoundValue(soundCore.loudness)
    proj.draw(eq.getEQ())

    key = cv.waitKey(100)

"""
allLoudness = soundCore.allLoudness.copy()
print(allLoudness)
n = len(allLoudness)
maxs = [-np.inf,-np.inf,-np.inf,-np.inf,-np.inf]
mins = [np.inf,np.inf,np.inf,np.inf,np.inf]
for i in range(len(allLoudness)):
    for j in range(5):
        if allLoudness[i][j] > maxs[j]:
            maxs[j] = allLoudness[i][j]
        if allLoudness[i][j] < mins[j]:
            mins[j] = allLoudness[i][j]

print("max : ",maxs)
print("mins : ",mins)
"""
cv.destroyAllWindows()
