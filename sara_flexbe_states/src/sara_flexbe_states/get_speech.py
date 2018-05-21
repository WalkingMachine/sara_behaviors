#!/usr/bin/env python
# encoding=utf8

from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxySubscriberCached
from rospy.rostime import get_time
from std_msgs.msg import String

class GetSpeech(EventState):
    '''
    Gets latest voice command given to sara.
    -- watchdog    float     max time in seconds before continuing

    #> words        String    command given
    

    <= received         The command is received.
    <= nothing          Nothing has been said.
    <= fail             Sara can't hear you.

    '''

    def __init__(self, watchdog):
        '''
        Constructor
        '''
        super(GetSpeech, self).__init__(outcomes=['done', 'nothing', 'fail'], output_keys=['words'])
        self._topic = "/sara_command"
        self._connected = False
        self.watchdog = watchdog

        self._sub = ProxySubscriberCached({self._topic: String})
        self.time = 0

    def execute(self, userdata):

        Logger.loginfo('looking for voice command ')
        if self._sub.has_msg(self._topic):
            Logger.loginfo('getting message')
            message = self._sub.get_last_msg(self._topic)
            userdata.words = message.data
            self._sub.remove_last_msg(self._topic)
            return 'done'
        if (self.time-get_time() <= 0):
            Logger.loginfo('no speech detected')
            return 'nothing'

    def on_enter(self, userdata):
        self.time = get_time()+self.watchdog
