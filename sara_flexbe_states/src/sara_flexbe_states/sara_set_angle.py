#!/usr/bin/env python

from flexbe_core import EventState, Logger
import rospy
from std_msgs.msg import Float64


class SaraSetAngle(EventState):
    """
    Make sara change the angle her the head

    -- angle     Float64      angle of the head

    <= done                what's said is said
    """


    def __init__(self, angle):
        """Constructor"""

        super(SaraSetAngle, self).__init__(outcomes = ['done'])
        self.angle = angle

    def execute(self, userdata):

        Logger.loginfo('Setting head angle to '+str(self.angle))
        pub = rospy.Publisher("/sara_head_pitch_controller/command", Float64, queue_size=1)
        ms = Float64
        ms.data = self.angle
        pub.publish(ms)

        Logger.loginfo('Publishing done')

        return 'done'