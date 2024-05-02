# !/usr/bin/env python3
import rclpy
import cv2
from rclpy.node import Node

from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Header

class DetermineColor(Node):
    def __init__(self):
        super().__init__('color_detector')
        self.image_sub = self.create_subscription(Image, '/color', self.callback, 10)
        self.color_pub = self.create_publisher(Header, '/rotate_cmd', 10)
        self.bridge = CvBridge()

    def callback(self, data):
        try:
            # listen image topic
            image = self.bridge.imgmsg_to_cv2(data, 'bgr8')

            avg_color_init = cv2.mean(image)
            avg_color = avg_color_init[:3]

            # prepare rotate_cmd msg
            # DO NOT DELETE THE BELOW THREE LINES!
            msg = Header()
            msg = data.header
            msg.frame_id = '0'  # default: STOP
    
            # determine background color
            # TODO 
            # determine the color and assing +1, 0, or, -1 for frame_id
            # msg.frame_id = '+1' # CCW 
            # msg.frame_id = '0'  # STOP
            # msg.frame_id = '-1' # CW

            if avg_color[2] > avg_color[0] and avg_color[2] > avg_color[1]:
                msg.frame_id = '-1'
            elif avg_color[0] > avg_color[1] and avg_color[0] > avg_color[2]:
                msg.frame_id = '+1'

            cv2.imshow('Image', image)
            cv2.waitKey(1)
            
            # publish color_state
            self.color_pub.publish(msg)
        except CvBridgeError as e:
            self.get_logger().error('Failed to convert image: %s' % e)
           



if __name__ == '__main__':
    rclpy.init()
    detector = DetermineColor()
    rclpy.spin(detector)
    detector.destroy_node()
    rclpy.shutdown()
