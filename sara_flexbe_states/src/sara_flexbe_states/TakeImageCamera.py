#!/usr/bin/env python


from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxyPublisher, ProxySubscriberCached
from control_msgs.msg import GripperCommandActionGoal
import rostopic
import inspect
from sensor_msgs.msg import Image

'''
Created on 31.01.2017

@author: Philippe La Madeleine
'''


class TakeImageCamera(EventState):
    '''
    Return the image from the topic.

    >= topic
    <= image

    <= received
    <= unavailable

    '''

    def __init__(self, topic):
        '''
        Constructor
        '''
        super(TakeImageCamera, self).__init__(outcomes=['received', 'unavailable'], output_keys=['image'])

        self._sub = ProxySubscriberCached({topic: Image})

        self.topic = topic
        self.message = None

    def execute(self, userdata):

        if self._sub.has_msg(self.topic):
            Logger.loginfo('Has an image')
            self.message = self._sub.get_last_msg(self.topic)
            self._sub.remove_last_msg(self.topic)

        if self.message is not None:
            userdata.image = self.message
            return 'received'

        return 'unavailable'

