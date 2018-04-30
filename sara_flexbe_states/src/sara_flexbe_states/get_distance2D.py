#!/usr/bin/env python

from flexbe_core import EventState, Logger
import rospy
import re
import ros
import math

class getDistance2D(EventState):
    """
    Calcule la distance entre deux points donnes.

    ### InputKey
    ># point1
    ># point2

    ### OutputKey
    #> distance

    <= done
    """
    def __init__(self):
        """Constructor"""

        super(getDistance2D, self).__init__(outcomes = ['done'], input_keys = ['point1','point2'], output_keys = ['distance'])

    def execute(self, userdata):
        """Wait for action result and return outcome accordingly"""

        userdata.distance= self.calculate_distance(userdata.point1,userdata.point2)
        return 'done'

    def calculate_distance(self, p1, p2):
        return ((p2.x-p1.x)**2+(p2.y-p1.y)**2)**.5
