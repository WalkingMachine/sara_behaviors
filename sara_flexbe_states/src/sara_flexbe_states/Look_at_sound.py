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
    Make Sara's head keep looking at the strongest source of sounds.
    """

    def __init__(self):
        """Constructor"""

        super(LookAtSound, self).__init__(outcomes=['done'])

        # Subscriber config
        self.soundsTopic = "/direction_of_arrival"
        self._sub = ProxySubscriberCached({self.soundsTopic: PoseStamped})

        # Publisher config
        self.pubPitch = rospy.Publisher("/sara_head_pitch_controller/command", Float64, queue_size=1)
        self.pubYaw = rospy.Publisher("/sara_head_yaw_controller/command", Float64, queue_size=1)
        self.msg = Float64()

    def execute(self, userdata):

        # If a new sound direction is detected.
        if self._sub.has_msg(self.soundsTopic):
            message = self._sub.get_last_msg(self.soundsTopic)
            orientation = message.pose.orientation
            orient_quat = [orientation.x, orientation.y, orientation.z, orientation.w]
            roll, pitch, yaw = euler_from_quaternion(orient_quat)

            # Publish the head commands
            self.msg.data = min(max(-pitch, -0), 1)
            self.pubPitch.publish(self.msg)
            self.msg.data = min(max(yaw, -1.2), 1.2)
            self.pubYaw.publish(self.msg)

            return "done"
