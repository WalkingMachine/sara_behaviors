#!/usr/bin/env python

from flexbe_core import EventState, Logger
import rospy
from std_msgs.msg import Float64


class SaraSetHeadAngleKey(EventState):
    """
    Make sara change the angle her the head

    -- angle     Float64      angle of the head

    <= done                what's said is said
    """


    def __init__(self):
        """Constructor"""

        super(SaraSetHeadAngleKey, self).__init__(outcomes = ['done'], input_keys=['yaw', 'pitch'])
        self.pubp = rospy.Publisher("/sara_head_pitch_controller/command", Float64, queue_size=1)
        self.puby = rospy.Publisher("/sara_head_yaw_controller/command", Float64, queue_size=1)

    def execute(self, userdata):

        ms = Float64()
        Logger.loginfo('Setting head pitch to '+str(userdata.pitch))
        Logger.loginfo('Setting head yaw to '+str(userdata.yaw))
        ms.data = userdata.pitch
        self.pubp.publish(ms)
        ms.data = userdata.yaw
        self.puby.publish(ms)
        Logger.loginfo('Publishing done')
        return 'done'
