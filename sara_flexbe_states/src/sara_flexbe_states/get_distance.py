#!/usr/bin/env python

from flexbe_core import EventState, Logger
import rospy
import re
import ros

class getDistance(EventState):
    """
    Calcul la distance entre deux points donnes.

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

    def calculate_distance(point1,point2):
        retour =0
        return retour
