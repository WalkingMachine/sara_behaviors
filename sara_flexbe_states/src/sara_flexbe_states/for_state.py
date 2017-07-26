#!/usr/bin/env python

from flexbe_core import EventState, Logger
import rospy
from wm_tts import srv
from wm_tts import msg

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
        self.sentence = sentence
        self.emotion = emotion

    def execute(self, userdata):
        """Wait for action result and return outcome accordingly"""

        rospy.wait_for_service('/wm_say')
        req = msg.say
        req.sentence = str(self.sentence)
        req.emotion = self.emotion
        serv = rospy.ServiceProxy('/wm_say', srv.say_service )
        serv( req )

        return 'done'

