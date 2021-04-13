import cv2
import cv2.aruco as auo
import numpy as np
import PIL
import imutils
from imutils.video import VideoStream
import time
import sys
from calibration import calibrate
import os

print("[INFO] Use Ctrl+C to exit.")
print("[INFO] calibrating camera...")
ret,camera_matrix,dist_coeffs = calibrate()
if ret:
	print("[INFO] attained camera calibration values.")
else:
	print("[ERROR] failed to get camera calibration values...")

arucoDict = auo.Dictionary_get(auo.DICT_6X6_1000)
arucoParams = auo.DetectorParameters_create()

print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)

while True:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 1000 pixels with , width=1000.
	frame = vs.read()
	frame = imutils.resize(frame)
	# detect ArUco markers in the input frame
	(corners, ids, rejected) = auo.detectMarkers(frame,
		arucoDict, parameters=arucoParams)
	if len(corners) > 0:
		# flatten the ArUco IDs list
		ids = ids.flatten()

		#print('corners: ', corners, ' ids: ', ids)
		# loop over the detected ArUCo corners
		#for (markerCorner, markerID) in zip(corners, ids):
		rvecs, tvecs, _objPoints = auo.estimatePoseSingleMarkers(corners,0.05,camera_matrix,
									dist_coeffs)
		#print(tvecs)
		for i in range(len(rvecs)):
			rvec = rvecs[i]
			tvec = tvecs[i]
			print(tvec, " ID: ", ids[i])
			auo.drawAxis(frame,camera_matrix,dist_coeffs,rvec,tvec,0.1)

			# extract the marker corners (which are always returned
			# in top-left, top-right, bottom-right, and bottom-left
			# order)
		for (markerCorner, markerID) in zip(corners, ids):
			mcorners = markerCorner.reshape((4, 2))
			(topLeft, topRight, bottomRight, bottomLeft) = mcorners
			topLeft = (int(topLeft[0]), int(topLeft[1]))
			cv2.putText(frame, str(markerID),
				(topLeft[0], topLeft[1] - 15),
				cv2.FONT_HERSHEY_COMPLEX,
				0.5, (0, 0, 255), 2)

	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break
	if key == ord("s"):
		time.sleep(15000)

cv2.destroyAllWindows()
vs.stop()
os._exit()
