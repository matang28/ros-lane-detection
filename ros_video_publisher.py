#!/usr/bin/env python

import cv2
import numpy as np
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


def publish_video_file(path):
    publisher = rospy.Publisher('lanes_video', Image, queue_size=100)

    rospy.init_node('lanes_publisher', anonymous=True)
    rospy.Rate(0.5)
    bridge = CvBridge()

    capture = cv2.VideoCapture(path)

    if not capture.isOpened():
        print "Error opening resource: " + str(path)
        print "Maybe opencv VideoCapture can't open it"
        exit(1)

    print "Correctly opened resource, starting to show feed."
    ret, frame = capture.read()

    while ret:
        ret, frame = capture.read()

        if frame is None:
            break

        frame = np.uint8(frame)
        image_message = bridge.cv2_to_imgmsg(frame, encoding="passthrough")
        publisher.publish(image_message)

        key = cv2.waitKey(1000)
        if key == 27 or key == 1048603:
            break


if __name__ == '__main__':
    try:
        publish_video_file("lanes.mp4")
        exit(0)
    except rospy.ROSInterruptException as ex:
        print (ex)
        exit(1)
