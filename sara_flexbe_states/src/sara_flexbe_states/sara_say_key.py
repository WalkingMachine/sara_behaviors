#!/usr/bin/env python

from flexbe_core import EventState, Logger
import rospy
from wm_tts import srv
from wm_tts import msg

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
        self.emotion = emotion
        self.Format = Format

    def execute(self, userdata):
        """Wait for action result and return outcome accordingly"""

        rospy.wait_for_service('/wm_say')
        req = msg.say
        req.sentence = str(self.Format( userdata.sentence ))
        req.emotion = self.emotion
        serv = rospy.ServiceProxy('/wm_say', srv.say_service )
        serv( req )

        return 'done'

