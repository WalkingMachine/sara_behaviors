#!/usr/bin/env python

import rospy
from flexbe_core import EventState, Logger
from sara_msgs.msg import Entity

'''
Created on 05.05.2019

@author: Quentin Gaillot
'''


class GetEntityFromListByID(EventState):
    '''
    return the entity with a specified ID if its exist in the list in input

    ># entityList   object[]   	List of entities.

    ># ID   int    	ID number of the entity to find.

    #> entityFound object      The found entity.

    <= done                     Indicates completion of the extraction.
    <= not_found                Indicates completion of the extraction.

    '''

    def __init__(self, attributes=[]):
        '''Constructor'''
        super(GetAttribute, self).__init__(outcomes=['done', 'not_found'],
                                           input_keys=['entityList','ID'],
                                           output_keys=['entity'])


    def execute(self, userdata):
        '''Execute this state'''
        for entity in userdata.entityList:
            if entity.ID == ID:
                userdata.entity = entity
                return 'done'

        userdata.entity = ""
        return 'not_found'