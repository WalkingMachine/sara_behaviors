#!/usr/bin/env python

from flexbe_core.proxy import ProxySubscriberCached
from flexbe_core import EventState, Logger
from sara_msgs.msg import Entities
from geometry_msgs.msg import Pose
from tf.transformations import euler_from_quaternion

import math


class GetEntityByID(EventState):
    '''
        Search for an entity by it's ID number

        ># ID              int
        #> Entity          object

        <= found            people are found
        <= not_found        no one is found

    '''

    def __init__(self):
        '''
        Constructor
        '''
        super(GetEntityByID, self).__init__(outcomes=['found', 'not_found'], input_keys=['ID'], output_keys=['Entity'])
        self._sub = ProxySubscriberCached({'/entities': Entities})

        self.message = None

    def execute(self, userdata):

        if self._sub.has_msg('/entities'):
            Logger.loginfo('getting list of entities')
            self.message = self._sub.get_last_msg('/entities')
            self._sub.remove_last_msg('/entities')

        if self.message is not None:

            for entity in self.message.entities:
                if entity.ID == userdata.ID:
                    userdata.Entity = entity
                    return 'found'

            return 'not_found'
