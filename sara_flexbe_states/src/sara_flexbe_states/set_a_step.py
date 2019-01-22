#!/usr/bin/env python

from flexbe_core import EventState, Logger
import rospy
from std_msgs.msg import UInt32


class Set_a_step(EventState):
    """
    Set a step in the Vizbox storyboard.
    -- step   UInt32 The desired step of the story

    <= done  what's suppose to be set was set
    """

    def __init__(self, step):
        """set the step"""
        super(Set_a_step, self).__init__(outcomes=['done'])
        self.pub = rospy.Publisher("/challenge_step", UInt32)
        self.msg = UInt32()
        self.msg.data = step

    def execute(self, userdata):
        """execute what needs to be executed"""
        self.pub.publish(self.msg)
        return 'done'
