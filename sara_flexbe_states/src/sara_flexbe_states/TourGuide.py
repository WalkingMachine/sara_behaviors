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
    state will return the sequence to travel to the object's room.


    ># startingRoom string	informationPoint's room. Must be "office", "living room", "kitchen" or "bedroom"

    ># endingRoom string	where the object should be found. Must be "office", "living room", "kitchen" or "bedroom"

    ># dictRoomToRoom  dict	dictionnary of the directions from room to room

    ># object  string		name of the object that needs to be located

    #> sequence list	     	the ending combined sequence

    <= done			The sequence as been generated.

    '''


    def __init__(self):
        '''
        Constructor
        '''

        super(TourGuide, self).__init__(outcomes=['done'],
                                        input_keys=['object', 'startingRoom', 'endingRoom', 'dictRoomToRoom'],
                                        output_keys=['sequence'])

        self._calculation_result = None

    def execute(self, userdata):

        '''Execute this state'''

        destinationKey = userdata.startingRoom+userdata.endingRoom
        seq = userdata.dictRoomToRoom[destinationKey]
        
        userdata.sequence = seq
        
        for index, order in enumerate(seq):
            seq[index][1] = seq[index][1].replace("_object", userdata.object)
        
        print(seq)

        # nothing to check
        return 'done'













































