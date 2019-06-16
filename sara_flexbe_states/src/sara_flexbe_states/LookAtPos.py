#!/usr/bin/env python

from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxyActionClient

from actionlib_msgs.msg import GoalStatus
from move_base_msgs.msg import *
import rospy
from geometry_msgs.msg import Pose, Point
from flexbe_core.proxy import ProxySubscriberCached
import math
from std_msgs.msg import Float64
from wm_direction_to_point.srv import get_direction, get_directionRequest

"""
Created on 16/06/2019
@author: Alexandre Mongrain

Based upon KeepLookingAt
"""


class LookAtPos(EventState):
    """
    Make Sara's head look at a point using sara_set_head_angle.

    ># pos     Point      Point or pose to look at

    """

    def __init__(self):
        """Constructor"""

        super(LookAtPos, self).__init__(outcomes=['failed', 'done'],
                                        input_keys=['pos'])

        self.pubp = rospy.Publisher("/sara_head_pitch_controller/command", Float64, queue_size=1)
        self.puby = rospy.Publisher("/sara_head_yaw_controller/command", Float64, queue_size=1)

        # Reference from and reference to
        self.service = get_directionRequest()
        self.service.reference = "head_xtion_link"
        self.service.origine = "base_link"

        self.serviceName = '/get_direction'
        Logger.loginfo('waiting for service '+str(self.serviceName))
        self.serv = rospy.ServiceProxy(self.serviceName, get_direction)

        self._active = True
        try:
            self.serv.wait_for_service(1)
        except:
            self._active = False

    def execute(self, userdata):
        if self._active:
            if self.pos == Pose:
                position = userdata.pos.position
            else:
                position = userdata.pos

            ms = Float64()
            serv = rospy.ServiceProxy('/get_direction', get_direction)
            self.service.point = position
            resp = serv(self.service)

            ms.data = min(max(-resp.pitch, -0), 1)
            self.pubp.publish(ms)
            ms.data = min(max(resp.yaw, -1.2), 1.2)
            self.puby.publish(ms)
            return "done"
        else:
            ms = Float64()
            ms.data = 0.3
            self.pubp.publish(ms)
            ms.data = 0
            self.puby.publish(ms)
            return "failed"
