#!/usr/bin/env python

from flexbe_core.proxy import ProxySubscriberCached
from flexbe_core import EventState, Logger
from sara_msgs.msg import Entities
from geometry_msgs.msg import Pose

'''
Created on 16.06.2019
@author: Alexandre Mongrain
'''


class list_entities_near_point(EventState):
    '''
        Will list entities near a point, within a radius sorted by distance

        -- radius        float        distance used to screen out farther entities.
        #< name                    string       name to compare entities with, can be used to screen found entities by name
        #< position                   Point       position used to compare distance, can be Point or Pose
        #> found_entities          object       list of found entities

        <= found            entities are found
        <= none_found        no one is found

    '''

    def __init__(self, radius):
        '''
        Constructor
        '''
        super(list_entities_near_point, self).__init__(outcomes=['found', 'none_found'],
                                                       output_keys=['entity_list', 'number'],
                                                       input_keys=['name', 'position'])
        self._sub = ProxySubscriberCached({'/entities': Entities})
        self.radius = radius
        self.message = None
        self.position = None

    def execute(self, userdata):
        if self._sub.has_msg('/entities'):
            Logger.loginfo('getting detected entities')
            self.message = self._sub.get_last_msg('/entities')
            self._sub.remove_last_msg('/entities')

        if type(userdata.position) == Pose:
            self.position = userdata.position.position
        else:
            self.position = userdata.position

        if self.message is not None:
            found_entities = self.list(userdata.name)
            userdata.entity_list = found_entities
            userdata.number = len(found_entities)

            if len(found_entities) != 0:
                return 'found'
            else:
                return 'none_found'

    def list(self, name):
        found_entities = []
        wraps = []
        for entity in self.message.entities:
            x = entity.position.x - self.position.x
            y = entity.position.y - self.position.y
            z = entity.position.z - self.position.z
            dist = (x**2 + y**2 + z**2)**0.5
            #Logger.loginfo('dist: '+str(dist)+" name: "+entity.name)
            if (name == "" or entity.name == name or entity.category == name) and dist < self.radius:
                wrap = wrapper()
                wrap.init(self.position, entity)
                wraps.append(wrap)

        wraps.sort(key=wrapper.key)

        for wrap in wraps:
            found_entities.append(wrap.entity)

        return found_entities


class wrapper():
    def init(self, position, entity):
        self.entity = entity
        
        x = entity.position.x - position.x
        y = entity.position.y - position.y
        z = entity.position.z - position.z
        
        self.dist = (x**2 + y**2 + z**2)**0.5
        self.dist /= entity.probability**2

    def key(self):
        return self.dist
