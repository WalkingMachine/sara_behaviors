#!/usr/bin/env python

from flexbe_core.proxy import ProxySubscriberCached
from flexbe_core import EventState, Logger
from sara_msgs.msg import Entities


class list_person(EventState):
    '''
        will list people seen by the camera

        #> persons          object

        <= found            people are found
        <= not_found        no one is found

    '''

    def __init__(self):
        '''
        Constructor
        '''
        super(list_person, self).__init__(outcomes=['found', 'not_found'], output_keys=['list_person', 'number'])
        self._sub = ProxySubscriberCached({'/entities': Entities})

    def execute(self, userdata):

        if self._sub.has_msg('/entities'):
            Logger.loginfo('getting message')
            message = self._sub.get_last_msg('/entities')
            self._sub.remove_last_msg('/entities')

            persons = self.list(message)
            userdata.list_person = persons
            userdata.number = len(persons)
            return 'found'
        else:
            return 'not_found'

    def list(self, message):
        persons = []
        for entity in message.entities:
            if entity.name == 'person':
                persons.append(entity)
        return persons
