#!/usr/bin/env python

from flexbe_core import EventState, Logger
import rospy
import re
import ros

class processFollowDistance(EventState):
    """
    Calcule la distance  entre deux points donnes.

    ###Params
    -- minimum_distance      double      minimum_distance
    -- divisor_distance      double      divisor_distance
    -- threshold             double      threshold

    ### InputKey
    ># distance_of_target    double      distance_of_target

    ### OutputKey
    #> distance             double      distance

    ###Outcomes
    <= move                 the robot will move
    <= done                 the robot won't move
    """
    def __init__(self, minimum_distance, divisor_distance,threshold):
        """Constructor"""

        super(processFollowDistance, self).__init__(outcomes = ['move','done'], input_keys = ['distance_of_target'], output_keys = ['distance'])
        self.minimum_distance=minimum_distance
        self.divisor_distance=divisor_distance
        self.threshold=threshold

    def execute(self, userdata):
        """Determine action to perform and return outcome accordingly"""

        retour = self.minimum_distance
        dis =userdata.distance_of_target
        if(dis<self.threshold+self.minimum_distance and dis>self.minimum_distance):
            return 'done'
        mi_distance = dis/self.divisor_distance
        if(mi_distance>self.minimum_distance): retour = mi_distance
        userdata.distance = retour
        return 'move'
