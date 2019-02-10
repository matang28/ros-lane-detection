#!/usr/bin/env python

import cv2
import numpy as np
from detector import LaneDepartureDetector
import roslib
import sys
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


def _create_config(height, width):
    center_x = 670
    center_y = height / 2
    x_top_factor = 0.04
    x_lower_factor = 0.5
    lower_left = [center_x - x_lower_factor * width, height]
    lower_right = [center_x + x_lower_factor * width, height]
    top_left = [center_x - x_top_factor * width, center_y + height / 10]
    top_right = [center_x + x_top_factor * width, center_y + height / 10]

    roi_matrix = np.int32([
        lower_left, top_left, top_right, lower_right
    ])

    src = np.float32([(575, 464),
                      (707, 464),
                      (258, 682),
                      (1049, 682)])

    dst = np.float32([(550, 0),
                      (width - 500, 0),
                      (500, height),
                      (width - 550, height)])

    return src, dst, roi_matrix


class LaneDepartureConsumer:
    def __init__(self):
        rospy.init_node('test_vision_node')
        self.bridge = CvBridge()
        self.config = None
        self.detector = None
        self.image_subscription = rospy.Subscriber("lanes_video", Image, self.callback)
        self.departure_publisher = rospy.Publisher("image_lane_departure", String, queue_size=100)
        self.image_publisher = rospy.Publisher("image_lane_detector", Image, queue_size=100)

    def callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv(data, "bgr8")
        except CvBridgeError, e:
            print e

        if self.config:
            height = cv_image.shape[0]
            width = cv_image.shape[1]
            self.config = _create_config(height, width)
            self.detector = LaneDepartureDetector(self.config[0], self.config[1], self.config[2])

        (processed_image, departure) = self.detector.process_image(cv_image)

        self.departure_publisher.publish(self.bridge.cv2_to_imgmsg(str(departure)))

        try:
            self.image_publisher.publish(self.bridge.cv2_to_imgmsg(processed_image, "bgr8"))
        except CvBridgeError as e:
            print(e)

        cv2.waitKey(50)


def main(args):
    consumer = LaneDepartureConsumer()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down vison node."


if __name__ == '__main__':
    main(sys.argv)
