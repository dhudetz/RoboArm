import cv2.aruco as auo
from imutils.video import VideoStream
import camera
import time

arucoDict = auo.Dictionary_get(auo.DICT_6X6_250)
arucoParams = auo.DetectorParameters_create()

print("use Ctrl+C to exit.")
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)

while True:
    frame = vs.read()
    camera.draw_frame(frame)
