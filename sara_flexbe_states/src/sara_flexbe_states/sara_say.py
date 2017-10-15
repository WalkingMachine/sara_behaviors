#!/usr/bin/env python

from flexbe_core import EventState, Logger
import rospy
from wm_tts.msg import say
from wm_tts.srv import say_service

class SaraSay(EventState):
    """
    Make sara say something

    -- sentence     string      what to say
    -- emotion     int       how to feel
    -- block      bool       wait the end before continue

    <= done                what's said is said
    """

    def __init__(self, sentence, emotion, block=True):
        """Constructor"""

        super(SaraSay, self).__init__(outcomes = ['done'])
        self.msg = say(sentence, emotion)
        self.block = block
        if not self.block:
            self.pub = rospy.Publisher("/say", say, queue_size=1)


    def execute(self, userdata):
        """Wait for action result and return outcome accordingly"""
        if self.block:
            rospy.wait_for_service('/wm_say')
            serv = rospy.ServiceProxy('/wm_say', say_service)
            serv(self.msg)

        else:
            self.pub.publish(self.msg)
            Logger.loginfo('Publishing done')

        return 'done'

