#!/usr/bin/env python

import rospy
import math
from flexbe_core import EventState, Logger
from sara_msgs.msg import Entities
from geometry_msgs.msg import Pose

'''
Created on 04.05.2019

@author: Quentin Gaillot
'''


class GetEmptyChair(EventState):
    '''
    Return the entity of the closest chair or couch that are empty in the input list

    #> output_entity emptyChair		Return the entity of the closest place to sit.

    <= nothing_found        No place found
    <= done					An empty place have been found.

    '''

    def __init__(self):
        '''
        Constructor
        '''
        super(GetEmptyChair, self).__init__(outcomes=['done', 'nothing_found'],
                                               output_keys=['output_entity'])

        self._sub = ProxySubscriberCached({'/entities': Entities})

        self._subpos = ProxySubscriberCached({'/robot_pose': Pose})
        self.mypose = None

        self.message = None

    def dist(self, entity1, entity2):
        x = entity1.position.x - entity2.position.x
        y = entity1.position.y - entity2.position.y
        return math.sqrt(x*x+y*y)


    def execute(self):
        '''Execute this state'''
        if self._subpos.has_msg('/robot_pose'):
            self.mypose = self._subpos.get_last_msg('/robot_pose')

        if self._sub.has_msg('/entities'):
            Logger.loginfo('getting list of entities')
            self.message = self._sub.get_last_msg('/entities')
            self._sub.remove_last_msg('/entities')

        people = []
        chairs = []

        if self.message is not None and self.mypose is not None:
            for self.entity in self.message.entities:
                if entity.name == "person":
                    people.append(entity)
                if entity.name == "chair":
                    chairs.append(entity)
                if entity.name == "couch":
                    chairs.append(entity)

            for person in people:
                for chair in chairs:
                    if dist(chair, person) < 0.5:
                        chairs.remove(chair)
                        continue

            if len(chairs) == 0:
                return 'nothing_found'

            closest_empty_chair = chairs[0]
            min_dist = 999
            for chair in chairs:
                if dist(self.mypose, chair) < min_dist:
                    min_dist = dist(self.mypose, chair)
                    closest_empty_chair = chair

            userdata.output_entity = closest_empty_chair
            return 'done'
