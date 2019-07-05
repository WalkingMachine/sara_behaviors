#!/usr/bin/env python

import rospy
from flexbe_core import EventState, Logger

'''
Created on 6.07.2019

@author: Huynh-Anh Le
'''


class TourGuide(EventState):
    '''
    Implements a state will give the sequence to get to the object needed.
    state will return the sequence to get to the object


    ># originePose object		waypoint of the informationPoint

    ># dictDirect  object		dictionnary of the directions

    ># dictObject  object		dictionnary of the objects

    ># object  object		    object that needs to be located

    #> sequence object	     	the ending combined sequence

    <= done						Indicates completion of the calculation.

    '''


    def __init__(self):
        '''
        Constructor
        '''

        super(TourGuide, self).__init__(outcomes=['done'],
                                        input_keys=['object','originPose','dictDirect','dictObject'],
                                        output_keys=['sequence'])

        self._calculation_result = None

    def execute(self, userdata):

        '''Execute this state'''

        destinationPos = userdata.dictObject[userdata.object][0]
        destinationKey = userdata.originPose+destinationPos
        seq1 = userdata.dictObject[userdata.object][1][userdata.originPose][0]
        seq2=userdata.dictDirect[destinationKey]
        seq3=userdata.dictObject[userdata.object][1][userdata.originPose][1]

        userdata.sequence = seq1 + seq2 + seq3

        # nothing to check
        return 'done'













































