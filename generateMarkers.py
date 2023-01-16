
import cv2 as cv
import numpy as np
import cv2.aruco as aruco
import constants as cst

dict = aruco.Dictionary_get(aruco.DICT_6X6_250)

markerImage = aruco.drawMarker(dict, cst.N_MARKER_B1_TL, 200, borderBits=1)
cv.imwrite("markerTopLeft.png", markerImage)
markerImage = aruco.drawMarker(dict, cst.N_MARKER_B1_TR, 200, borderBits=1)
cv.imwrite("markerTopRight.png", markerImage)
markerImage = aruco.drawMarker(dict, cst.N_MARKER_B1_BL, 200, borderBits=1)
cv.imwrite("markerBottomLeft.png", markerImage)
markerImage = aruco.drawMarker(dict, cst.N_MARKER_B1_BR, 200, borderBits=1)
cv.imwrite("markerBottomRight.png", markerImage)