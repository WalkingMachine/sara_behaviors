#!/usr/bin/env python
# encoding=utf8

from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxySubscriberCached, ProxyPublisher
from rospy.rostime import get_time
from std_msgs.msg import String, Empty

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
        self._topic_sub = "/sara_command"
        self._topic_pub = "/wm_snips_asr/TODO"  # TODO get topic
        self._connected = False
        self.watchdog = watchdog

        self._sub = ProxySubscriberCached({self._topic_sub: String})
        self._pub = ProxyPublisher({self._topic_pub: Empty})
        self.time = 0

    def execute(self, userdata):
        if self._sub.has_msg(self._topic_sub):
            Logger.loginfo('getting message')
            message = self._sub.get_last_msg(self._topic_sub)
            userdata.words = message.data
            self._sub.remove_last_msg(self._topic_sub)
            return 'done'
        if (self.time-get_time() <= 0):
            Logger.loginfo('no speech detected')
            return 'nothing'

    def on_enter(self, userdata):
        self.emotionPub.publish(self._topic_pub, Empty())
        self.time = get_time()+self.watchdog
        self._sub.remove_last_msg(self._topic_sub)
