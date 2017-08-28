#!/usr/bin/env python

from flexbe_core import EventState, Logger
import rospy
from wm_tts import msg

class SaraSayAsync(EventState):
    """
    Make sara say something

    -- sentence     string      what to say
    -- emotion     int       how to feel

    <= done                what's said is said
    """

    def __init__(self, sentence, emotion):
        """Constructor"""

        super(SaraSayAsync, self).__init__(outcomes = ['done'])
        self.sentence = sentence
        self.emotion = emotion

    def execute(self, userdata):
        """Wait for action result and return outcome accordingly"""

        pub = rospy.Publisher("/say", msg.say, queue_size=5)
        ms = msg.say()
        ms.sentence = self.sentence
        ms.emotion = self.emotion
        pub.publish(ms)

        Logger.loginfo('Publishing done')


        return 'done'

