#!/usr/bin/env python

from flexbe_core import EventState, Logger
import rospy
from wm_sound_library.srv import *
from std_msgs.msg import String as msg

class SaraSound(EventState):
    """
    Make sara play something

    -- sound     string      what sound to play

    <= done                what's played is played
    """

    def __init__(self, sound):
        """Constructor"""

        super(SaraSound, self).__init__(outcomes = ['done'])
        self.sound = sound

    def execute(self, userdata):
        """Wait for action result and return outcome accordingly"""

        rospy.wait_for_service('/wm_play_sound')
        req = msg()
        req.data = str(self.sound)
        serv = rospy.ServiceProxy('/wm_play_sound', play_service )
        serv( req )

        return 'done'

