import cv2
import cv2.aruco as auo
import numpy as np
import PIL
import imutils
from imutils.video import VideoStream
import time
import sys
from calibration import calibrate




print("use Ctrl+C to exit.")
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)

while True:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 1000 pixels with , width=1000.
	frame = vs.read()
	frame = imutils.resize(frame)
	frame = imutils.rotate(frame, 180, scale=1)
	#image = cv2.rotate(src, cv2.cv2.ROTATE_90_CLOCKWISE)
	# detect ArUco markers in the input frame
	(corners, ids, rejected) = auo.detectMarkers(frame,
		arucoDict, parameters=arucoParams)
	if len(corners) > 0:
		# flatten the ArUco IDs list
		ids = ids.flatten()
		#print('corners: ', corners, ' ids: ', ids)
		# loop over the detected ArUCo corners
		for (markerCorner, markerID) in zip(corners, ids):
			# extract the marker corners (which are always returned
			# in top-left, top-right, bottom-right, and bottom-left
			# order)
			corners = markerCorner.reshape((4, 2))
			#print('corners: ', corners)
			(topLeft, topRight, bottomRight, bottomLeft) = corners
			# convert each of the (x, y)-coordinate pairs to integers
			topRight = (int(topRight[0]), int(topRight[1]))
			bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
			bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
			topLeft = (int(topLeft[0]), int(topLeft[1]))

			# draw the bounding box of the ArUCo detection
			cv2.line(frame, topLeft, topRight, (0, 255, 0), 2)
			cv2.line(frame, topRight, bottomRight, (0, 0, 255), 2)
			cv2.line(frame, bottomRight, bottomLeft, (255, 0, 0), 2)
			cv2.line(frame, bottomLeft, topLeft, (200, 200, 0), 2)
			# compute and draw the center (x, y)-coordinates of the
			# ArUco marker
			cX = int((topLeft[0] + bottomRight[0]) / 2.0)
			cY = int((topLeft[1] + bottomRight[1]) / 2.0)
			cv2.circle(frame, (cX, cY), 4, (0, 0, 255), -1)
			# draw the ArUco marker ID on the frame
			fid_text = ""
			if markerID == 0:
				fid_text = "top_left"
			elif markerID == 1:
				fid_text = "bottom_right"
			elif markerID == 2:
				fid_text = "BLOCK"
			elif markerID == 3:
				fid_text = "top_right"
			cv2.putText(frame, fid_text,
				(topLeft[0], topLeft[1] - 15),
				cv2.FONT_HERSHEY_SIMPLEX,
				0.5, (0, 0, 0), 2)

	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break

cv2.destroyAllWindows()
vs.stop()
