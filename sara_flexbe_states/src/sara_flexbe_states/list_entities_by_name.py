#!/usr/bin/env python

from flexbe_core.proxy import ProxySubscriberCached
from flexbe_core import EventState, Logger
from sara_msgs.msg import Entities
from geometry_msgs.msg import Pose
from tf.transformations import euler_from_quaternion

import math


class list_entities_by_name(EventState):
    '''
        will list people seen by the camera

        -- Name                 string              name of the entities
        -- frontality_level     float               The level of frontality. 0.0 is circular, 1 is linear 0 is circular
        #> persons              object              the persons found

        <= found                people are found
        <= not_found            no one is found

    '''

    def __init__(self, Name, frontality_level):
        '''
        Constructor
        '''
        super(list_entities_by_name, self).__init__(outcomes=['found', 'not_found'],
                                                    output_keys=['Entities_list', 'number'])
        self._sub = ProxySubscriberCached({'/entities': Entities})

        self._topic = "/robot_pose"
        self._subpos = ProxySubscriberCached({self._topic: Pose})
        self.frontality_level = frontality_level
        self.mypose = None
        self.message = None
        self.Name = Name

    def execute(self, userdata):

        if self._subpos.has_msg(self._topic):
            self.mypose = userdata.pose = self._subpos.get_last_msg(self._topic)

        if self._sub.has_msg('/entities'):
            Logger.loginfo('getting list of entities')
            self.message = self._sub.get_last_msg('/entities')
            self._sub.remove_last_msg('/entities')

        if self.message is not None and self.mypose is not None:
            persons = self.list()
            userdata.Entities_list = persons
            userdata.number = len(persons)

            if len(persons) != 0:
                return 'found'
            else:
                return 'not_found'

    def list(self):
        Entities = []
        wraps = []
        for entity in self.message.entities:
            if entity.name == self.Name:
                wrap = wrapper()
                wrap.init(self.mypose, entity, self.frontality_level)

                wraps.append(wrap)

        wraps.sort(key=wrapper.key)

        for wrap in wraps:
            Entities.append(wrap.entity)

        return Entities


class wrapper():
    def init(self, mypose, entity, frontality_level):
        self.entity = entity

        x = entity.position.x - mypose.position.x
        y = entity.position.y - mypose.position.y

        quat = [mypose.orientation.x, mypose.orientation.y, mypose.orientation.z, mypose.orientation.w]
        euler = euler_from_quaternion(quat)
        A = euler[2]

        a = math.tan(A)
        b = y - x * a

        self.dist = (abs(y - a * x - b) / (1 + b ** 2) ** 0.5) * frontality_level
        self.dist += (((entity.position.x - mypose.position.x) ** 2 + (
                entity.position.y - mypose.position.y) ** 2) ** 0.5) * (1 - frontality_level)
        self.dist /= entity.probability ** 2

    def key(self):
        return self.dist