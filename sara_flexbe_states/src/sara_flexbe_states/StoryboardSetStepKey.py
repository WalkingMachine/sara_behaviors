#!/usr/bin/env python

from flexbe_core import EventState
import rospy
from std_msgs.msg import UInt32


class StoryboardSetStepKey(EventState):
    """
    Set a step in the Vizbox storyboard.
    ># step   UInt32 The desired step of the story

    <= done  what's suppose to be set was set
    """

    def __init__(self):
        """set the step"""
        super(StoryboardSetStepKey, self).__init__(outcomes=['done'], input_keys=['step'])
        self.pub = rospy.Publisher("/challenge_step", UInt32)

    def execute(self, userdata):
        """execute what needs to be executed"""

        msg = UInt32()
        msg.data = userdata.step
        self.pub.publish(msg)
        return 'done'
