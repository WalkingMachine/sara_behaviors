#!/usr/bin/env python

from flexbe_core import EventState, Logger
import rospy
import re
import ros
import math

class getDistance(EventState):
    """
    Calcule la distance entre deux points donnes.

    ### InputKey
    ># point1
    ># point2

    ### OutputKey
    #> distance

    <= done
    """
    def __init__(self, point1, point2):
        """Constructor"""

        super(GetNumberFromText, self).__init__(outcomes = ['done'], input_keys = ['point1','point2'], output_keys = ['distance'])
        self.min=point1
        self.max=point2

    def execute(self, userdata):
        """Wait for action result and return outcome accordingly"""

        userdata.distance= calculate_distance(userdata.point1,userdata.point2)
        return 'done'

    def calculate_distance(p1,p2):
        return math.sqrt(math.pow(p2.x-p1.x,2)+math.pow(p2.y-p1.y,2)+math.pow(p2.z-p1.z,2))
