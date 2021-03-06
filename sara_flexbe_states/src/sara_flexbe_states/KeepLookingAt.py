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
Modified on 06/17/2018
@author: Spyros Maniatopoulos

@mofificator: Veronica, Philippe, Huynh-Anh et Alexandre
"""

class KeepLookingAt(EventState):
    """
    Make Sara's head follow an entity using sara_set_head_angle.

    ># ID     int      entity ID.

    """

    def __init__(self):
        """Constructor"""

        super(KeepLookingAt, self).__init__(outcomes=['failed'],
                                         input_keys=['ID'])

        self.entities_topic = "/entities"
        self._sub = ProxySubscriberCached({self.entities_topic: Entities})

        self.pubp = rospy.Publisher("/sara_head_pitch_controller/command", Float64, queue_size=1)
        self.puby = rospy.Publisher("/sara_head_yaw_controller/command", Float64, queue_size=1)

        # Reference from and reference to
        self.service = get_directionRequest()
        self.service.reference = "head_xtion_link"
        self.service.origine = "base_link"

        self.Entity = None

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
            """Wait for action result and return outcome accordingly"""

            self.Entity = None

            # Get the entity's object in the latest detections
            if self._sub.has_msg(self.entities_topic):
                message = self._sub.get_last_msg(self.entities_topic)
                for entity in message.entities:
                    if entity.ID == userdata.ID:
                        self.Entity = entity
                        print("entity found: "+str(entity.ID))

            # If entity is defined, get the direction to it
            if self.Entity:

                if (self.Entity.name == "person"):
                    if (self.Entity.face.id != ""):
                        self.Entity.position.z += self.Entity.face.boundingBox.Center.z-0.1
                    else:
                        self.Entity.position.z += 1.6

                ms = Float64()
                serv = rospy.ServiceProxy('/get_direction', get_direction)
                self.service.point = self.Entity.position
                resp = serv(self.service)
                # Publish to both Yaw and Pitch controllers
                ms.data = min(max(-resp.pitch, -0), 1)
                self.pubp.publish(ms)
                ms.data = min(max(resp.yaw, -1.2), 1.2)
                self.puby.publish(ms)
                return
        else:
            Logger.logwarn("simulation mode: let's assume I'm looking at something")
            return

        ms = Float64()
        ms.data = 0.3
        self.pubp.publish(ms)
        ms.data = 0
        self.puby.publish(ms)

        return "failed"

    def on_enter(self, userdata):
        self.Entity = None

