#!/usr/bin/env python

from flexbe_core import EventState, Logger
import rospy
from wm_tts.msg import say

class SaraSay(EventState):
    """
    Make sara say something

    -- sentence     string      what to say
    -- emotion     int       how to feel

    <= done                what's said is said
    """

    def __init__(self, sentence, emotion):
        """Constructor"""

        super(SaraSay, self).__init__(outcomes = ['done'])
        self.pub = rospy.Publisher("/say", say, queue_size=1)
        self.msg = say(sentence, emotion)

    def execute(self, userdata):
        """Wait for action result and return outcome accordingly"""
        self.pub.publish(self.msg)
        Logger.loginfo('Publishing done')

        return 'done'

