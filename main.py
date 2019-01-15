import cv2
import numpy as np

path = "lanes.mp4"

video = cv2.VideoCaptrue(path)
while video.isOpened():
	ret, frame = video.read()
	
	if frame is None:
		break

	cv2.imshow('gray', frame)

	if cv2.waitKey(1) & 0xFF == ord('q')
		break

cv2.destroyAllWindows()
video.release()
