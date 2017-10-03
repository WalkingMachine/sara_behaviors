#!/usr/bin/env python

from flexbe_core import EventState, Logger
import rospy
from wm_tts.msg import say

class SaraSayKey(EventState):
    """
    Make sara say something

    -- Format      string   how to say it
    -- emotion     int       how to feel
    >= sentence              what key to say

    <= done                what's said is said
    """

    def __init__(self, Format , emotion):
        """Constructor"""

        super(SaraSayKey, self).__init__(outcomes = ['done'],
                                      input_keys=['sentence'])
        self.Format = Format
        self.msg = say()
        self.msg.emotion = emotion
        self.pub = rospy.Publisher("/say", say, queue_size=1)

    def execute(self, userdata):
        """Wait for action result and return outcome accordingly"""
        self.msg.sentence = str(self.Format( userdata.sentence ))
        self.pub.publish(self.msg)
        Logger.loginfo('Publishing done')

        return 'done'

