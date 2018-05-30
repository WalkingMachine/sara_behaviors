#!/usr/bin/env python

from flexbe_core import EventState, Logger
import cv2
from cv_bridge import CvBridge, CvBridgeError
import rospy


class TestGenderAge(EventState):
    '''
    Finding the gender and an age range of a person


    #> image      image     the image
    <= done       done
    '''

    def __init__(self):
        """Constructor"""
        super(TestGenderAge, self).__init__(outcomes=['done'], output_keys=['image'])
        rospy.loginfo("Fin init")

    def execute(self, userdata):
        """Wait for action result and return outcome accordingly"""

        bridge = CvBridge()
        cv_image = cv2.imread("/home/quentin/sara_ws/src/gender-age-classification/src/image/olivier.jpg")
        image_message = bridge.cv2_to_imgmsg(cv_image, encoding="passthrough")
        userdata.image = image_message
        rospy.loginfo("Done")
        return 'done'
