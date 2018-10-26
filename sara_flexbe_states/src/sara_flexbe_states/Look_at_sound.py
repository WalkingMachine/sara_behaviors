#!/usr/bin/env python

from flexbe_core import EventState, Logger
import rospy
from geometry_msgs.msg import PoseStamped
from tf.transformations import euler_from_quaternion
from flexbe_core.proxy import ProxySubscriberCached
from std_msgs.msg import Float64

"""
Created on 10/25/2018
@author: Philippe La Madeleine
"""

class LookAtSound(EventState):
    """
    Make Sara's head follow the strongest source of sounds.

    """

    def __init__(self):
        """Constructor"""

        super(LookAtSound, self).__init__(outcomes=['failed'])

        self.soundsTopic = "/direction_of_arrival"
        self._sub = ProxySubscriberCached({self.soundsTopic: PoseStamped})

        self.pubPitch = rospy.Publisher("/sara_head_pitch_controller/command", Float64, queue_size=1)
        self.pubYaw = rospy.Publisher("/sara_head_yaw_controller/command", Float64, queue_size=1)

        self.msg = Float64()

    def execute(self, userdata):
        """Wait for action result and return outcome accordingly"""

        # Get the sound direction
        if self._sub.has_msg(self.soundsTopic):
            message = self._sub.get_last_msg(self.soundsTopic)
            yaw, pitch, roll = euler_from_quaternion(message.pose.orientation)

            # Publish the head commands
            self.msg.data = min(max(-pitch, -0), 1)
            self.pubPitch.publish(self.msg)
            self.msg.data = min(max(yaw, -1.2), 1.2)
            self.pubYaw.publish(self.msg)

            return

        return "failed"

