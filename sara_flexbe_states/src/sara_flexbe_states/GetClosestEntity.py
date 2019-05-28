#!/usr/bin/env python

import rospy
import math
from flexbe_core import EventState, Logger
from sara_msgs.msg import Entities
from geometry_msgs.msg import Pose
from flexbe_core.proxy import ProxySubscriberCached

'''
Created on 27.05.2019

@author: Quentin Gaillot
'''


class GetClosestEntity(EventState):
    '''
    return the closest entity from the list in parameter. If no list in parameter, return the closest entity from the topic /entities

    ># entityList   object[]   	List of entities.

    #> entityFound object      The found entity.

    <= done                     Indicates completion of the extraction.
    <= not_found                Indicates completion of the extraction.

    '''

    def __init__(self):
        '''Constructor'''
        super(GetClosestEntity, self).__init__(outcomes=['done', 'not_found'],
                                           input_keys=['entityList'],
                                           output_keys=['output_entity'])

        self._sub = ProxySubscriberCached({'/entities': Entities})
        self._subpos = ProxySubscriberCached({'/robot_pose': Pose})
        self.mypose = None

    def dist(self, entity1, entity2):
        x = entity1.position.x - entity2.position.x
        y = entity1.position.y - entity2.position.y
        return math.sqrt(x*x+y*y)

    def execute(self, userdata):
        '''Execute this state'''
        if self._subpos.has_msg('/robot_pose'):
            self.mypose = self._subpos.get_last_msg('/robot_pose')

        if len(userdata.entityList) == 0:
            Logger.loginfo('va chercher la liste entities')
            if self._sub.has_msg('/entities'):
                myList = self._sub.get_last_msg('/entities')
                self._sub.remove_last_msg('/entities')
                myList = myList.entities
                Logger.loginfo('a la liste entities')
        else:
            myList = userdata.entityList
            Logger.loginfo('a la liste en parametre')

        if len(myList) == 0:
            Logger.loginfo('liste vide')
            return "not_found"

        min_dist = 99999
        closestEntity = myList[0]
        for entity in myList:
            if self.dist(self.mypose, entity) < min_dist:
                min_dist = self.dist(self.mypose, entity)
                closestEntity = entity

        userdata.output_entity = closestEntity
        return 'done'
