#!/usr/bin/env python

from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxyActionClient

from actionlib_msgs.msg import GoalStatus
from move_base_msgs.msg import *
from geometry_msgs.msg import Pose, Point, Quaternion, Pose2D
from tf import transformations

"""
Created on 11/19/2015
Modified on 05/21/2017
@author: Spyros Maniatopoulos

@mofificator: Nicolas Nadeau & Philippe La Madeleine
"""

class SaraSetPoint(EventState):
    """
    Navigates a robot to a desired position and orientation using move_base.

    #> waypoint     Pose2D      Target waypoint for navigation.

    <= done                  Navigation to target pose succeeded.
    """

    def __init__(self):
        """Constructor"""

        super(SaraSetPoint, self).__init__(outcomes=['done'],
                                           output_keys=['waypoint'])

    def execute(self, userdata):
        """Wait for action result and return outcome accordingly"""
        return 'done'


    def on_enter(self, userdata):
        """Create and send action goal"""
        pt = Point(x=userdata.x, y=userdata.y)
        qt = transformations.quaternion_from_euler(0, 0, userdata.theta)
        userdata.waypoint = Pose(position=pt, orientation=Quaternion(*qt))

