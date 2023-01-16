from ctypes import c_void_p

import cv2 as cv
import cv2.aruco as aruco
import numpy as np

import constants as cst
import projector
import camera


class CoreAR:
    def __init__(self, cam, proj):
        self.cam = cam
        self.proj = proj

    def calibrateCamera(self):
        self.proj.drawBlack()

        cornersCamera = []
        cornersBoard = []

        # Detect markers
        while len(cornersCamera) < 4:
            parmeters = aruco.DetectorParameters_create()
            dictionnary = aruco.Dictionary_get(aruco.DICT_6X6_250)
            markers, ids, rejectedImgPoints = aruco.detectMarkers(self.cam.getFrame(), dictionnary,
                                                                  parameters=parmeters)

            nbCornersDetected = 0

            # Get markers corresponding to corners
            for i in range(0, len(markers)):
                if ids[i] == cst.N_MARKER_B1_TR or ids[i] == cst.N_MARKER_B1_TL or ids[i] == cst.N_MARKER_B1_BR or ids[
                    i] == cst.N_MARKER_B1_BL:
                    nbCornersDetected += 1

                if ids[i] == cst.N_MARKER_B1_TR:
                    cornersCamera.append(markers[i][0][0])
                    cornersBoard.append(cst.MARKER_B1_TR)

                if ids[i] == cst.N_MARKER_B1_TL:
                    cornersCamera.append(markers[i][0][0])
                    cornersBoard.append(cst.MARKER_B1_TL)

                if ids[i] == cst.N_MARKER_B1_BR:
                    cornersCamera.append(markers[i][0][0])
                    cornersBoard.append(cst.MARKER_B1_BR)

                if ids[i] == cst.N_MARKER_B1_BL:
                    cornersCamera.append(markers[i][0][0])
                    cornersBoard.append(cst.MARKER_B1_BL)

            # If everything goes right, create the transformation matrix
            if nbCornersDetected == 4:
                self.R2C, _ = cv.findHomography(np.array(cornersBoard), np.array(cornersCamera))
                self.C2R, _ = cv.findHomography(np.array(cornersCamera), np.array(cornersBoard))

                self.cameraIsCalibrated = True

                # Display the corners
                resultFrame = self.cam.getFrame()
                aruco.drawDetectedMarkers(resultFrame, markers, borderColor=(0, 0, 255))
                cv.imshow(cst.WINDOW_MAIN, resultFrame)

                # Get the marker in real space
                cornersReal = cv.perspectiveTransform(np.array([cornersCamera]), self.C2R)

            else:
                # Clean the lists
                cornersCamera.clear()
                cornersBoard.clear()

    def calibrateProjector(self):
        pointsCamera = []
        pointsProjector = []

        while len(pointsCamera) < 8:
            pointsCamera.clear()
            pointsProjector.clear()

            # Draw markers on projector
            markersPts, markersId = self.proj.drawMarkers()

            # Wait a second
            cv.waitKey(1000)

            # Detect markers on camera
            parameters = aruco.DetectorParameters_create()
            dictionnary = aruco.Dictionary_get(aruco.DICT_5X5_250)
            markers, ids, rejectedImgPoints = aruco.detectMarkers(self.cam.getFrame(), dictionnary,
                                                                  parameters=parameters)

            # Get markers corresponding to the projected ones
            for i in range(len(markers)):
                for j in range(len(markersId)):
                    if ids[i][0] == markersId[j]:
                        pointsCamera.append(markers[i][0][0])
                        pointsProjector.append(markersPts[j])

        # Display the markers
        resultFrame = self.cam.getFrame()
        aruco.drawDetectedMarkers(resultFrame, markers, borderColor=(0, 0, 255))
        cv.imshow(cst.WINDOW_MAIN, resultFrame)

        # Create the transformation matrix
        pointsReal = cv.perspectiveTransform(np.array([pointsCamera]), self.C2R)[0]
        pointsProjector = np.array(pointsProjector)

        self.R2P, _ = cv.findHomography(pointsReal, pointsProjector)

    def findMove(self):
        # Get the current frame
        frame = self.cam.getFrame()

        # Convert to gray
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        green = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        # Find the difference between the reference frame and the current one
        diff = cv.absdiff(self.refFrame, gray)

        # cv.imshow("Difference", diff)


        # Threshold
        _, thresh = cv.threshold(diff, 130, 255, cv.THRESH_BINARY)
        cv.imshow("Threshold", thresh)

        # Opening
        kernel = np.ones((5, 5), np.uint8)
        opening = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel)

        # Find new elements
        contours, hierarchy = cv.findContours(opening, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        # Find the biggest contour
        biggest = None
        maxArea = 0
        for cnt in contours:
            area = cv.contourArea(cnt)
            if area > maxArea:
                maxArea = area
                biggest = cnt

        # Draw the biggest contour
        if biggest is not None:
            cv.drawContours(frame, [biggest], -1, (0, 255, 0), 3)
            cv.imshow(cst.WINDOW_MAIN, frame)
            cv.waitKey(1)

            # Store the center
            M = cv.moments(biggest)
            cx = M['m10'] / M['m00']
            cy = M['m01'] / M['m00']

            # Get its position in real space
            center = []
            center.append([cx, cy])

            # Get the position in real space
            pos = cv.perspectiveTransform(np.array([center]), self.C2R)
            return pos[0][0]

    def storeRefFrame(self):
        self.refFrame = self.cam.getFrame()
        # Turn it gray
        self.refFrame = cv.cvtColor(self.refFrame, cv.COLOR_BGR2GRAY)
        cv.imshow("Reference", self.refFrame)