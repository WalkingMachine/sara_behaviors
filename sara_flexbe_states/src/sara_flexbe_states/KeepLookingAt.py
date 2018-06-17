#!/usr/bin/env python

from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxyActionClient

from actionlib_msgs.msg import GoalStatus
from move_base_msgs.msg import *
from std_srvs.srv import Empty
import rospy
from geometry_msgs.msg import Pose, Point, Quaternion, Pose2D
from tf import transformations
from tf.transformations import quaternion_from_euler
from sara_msgs.msg import Entities
from flexbe_core.proxy import ProxySubscriberCached
import math
from std_msgs.msg import Float64
from wm_direction_to_point.srv import get_direction, get_directionRequest

"""
Created on 11/19/2015
Modified on 06/15/2018
@author: Spyros Maniatopoulos

@mofificator: Veronica, Philippe et Huynh-Anh
"""

class KeepLookingAt(EventState):
    """
    Make Sara's head follow an entity using sara_set_head_angle.

    ># ID     int      entity ID.

    """

    def __init__(self, angle):
        """Constructor"""

        super(SaraFollow, self).__init__(outcomes=['failed'],
                                         input_keys=['ID'])

        self.entities_topic = "/entities"
        self._sub = ProxySubscriberCached({self.entities_topic: Entities})

        self.pubp = rospy.Publisher("/sara_head_pitch_controller/command", Float64, queue_size=1)
        self.puby = rospy.Publisher("/sara_head_yaw_controller/command", Float64, queue_size=1)

        self.service = get_directionRequest()
        self.service.reference = "sara_head"
        self.service.origine = "base_link"

        self.Entity = None

        Logger.loginfo('waiting for service /get_direction')
        rospy.wait_for_service('/get_direction')

    def execute(self, userdata):
        """Wait for action result and return outcome accordingly"""

        # self.count += 1
        # if self.count > 10:
        #     self.count = 0
        #     return

        self.Entity = None

        # Get the entity's position
        if self._sub.has_msg(self.entities_topic):
            message = self._sub.get_last_msg(self.entities_topic)
            for entity in message.entities:
                if entity.ID == userdata.ID:
                    self.Entity = entity

        if self.Entity:
            ms = Float64()
            serv = rospy.ServiceProxy('/get_direction', get_direction)
            self.service.point = userdata.targetPoint
            resp = serv(self.service)

            ms.data = resp.pitch
            self.pubp.publish(ms)
            ms.data = resp.yaw
            self.puby.publish(ms)


    def on_enter(self, userdata):
        """Clean the costmap"""
        self.Entity = None

