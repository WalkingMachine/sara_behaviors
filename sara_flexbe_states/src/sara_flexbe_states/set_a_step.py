#!/usr/bin/env python

from flexbe_core import EventState, Logger
import rospy
from std_msgs.msg import UInt32



class Set_a_step(EventState):
    """
       set a step. need a story
    -- step   UInt32  the desired step of the story

    <= done  what's suppose to be set was set
    """

    def __init__(self, step):
        """set the step"""
        super(Set_a_step, self).__init__(outcomes=['done'])
        self.pub = rospy.Publisher("/challenge_step", UInt32)
        self.msg = UInt32()
        self.msg.data =step

    def execute(self, userdata):
        """execute what needs to be executed"""
        self.pub.publish(self.msg)
        Logger.loginfo('Success')
        return 'done'
