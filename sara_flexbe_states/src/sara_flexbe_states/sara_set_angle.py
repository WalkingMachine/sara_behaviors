#!/usr/bin/env python

from flexbe_core import EventState, Logger
import rospy
from std_msgs.msg import Float64


class SaraSetHeadAngle(EventState):
    """
    Make sara change the angle her the head

    -- angle     Float64      angle of the head

    <= done                what's said is said
    """


    def __init__(self, pitch, yaw):
        """Constructor"""

        super(SaraSetHeadAngle, self).__init__(outcomes = ['done'])
        self.pitch = pitch
        self.yaw = yaw

    def execute(self, userdata):

        ms = Float64()
        Logger.loginfo('Setting head pitch to '+str(self.pitch))
        Logger.loginfo('Setting head yaw to '+str(self.yaw))
        pub = rospy.Publisher("/sara_head_pitch_controller/command", Float64, queue_size=1)
        ms.data = self.pitch
        pub.publish(ms)
        pub = rospy.Publisher("/sara_head_yaw_controller/command", Float64, queue_size=1)
        ms.data = self.yaw
        pub.publish(ms)

        Logger.loginfo('Publishing done')

        return 'done'
