#!/usr/bin/env python

from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxySubscriberCached
import rostopic
import inspect
from std_msgs.msg import Bool


class ContinueButton(EventState):
    '''
    Reads on a topic to see for the continue button.

    <= done            Continue if button pressed.

    '''

    def __init__(self):
        '''
        Constructor
        '''
        super(ContinueButton, self).__init__(outcomes=['true', 'false'])
        self._topic = "/continue_button"
        self._connected = False

        self._sub = ProxySubscriberCached({self._topic: Bool})

    def execute(self, userdata):

        Logger.loginfo('Waiting for the continue button')
        if self._sub.has_msg(self._topic):
            message = self._sub.get_last_msg(self._topic)
            self._sub.remove_last_msg(self._topic)
            if message.data:
                return 'true'
            else:
                return 'false'
