#!/usr/bin/env python
# encoding=utf8

from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxySubscriberCached
import rostopic
from rospy.rostime import get_time
import inspect

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
        self.watchdog = watchdog
        self._topic = "/sara_command"
        self._connected = False

        (msg_path, msg_topic, fn) = rostopic.get_topic_type(self._topic)


        if msg_topic == self._topic:
            msg_type = self._get_msg_from_path(msg_path)
            self._sub = ProxySubscriberCached({self._topic: msg_type})
            self._connected = True

            Logger.loginfo('connecting to '+self._topic)
        else:
            Logger.logwarn('Topic %s for state %s not yet available.\nFound: %s\nWill try again when entering the state...' % (self._topic, self.name, str(msg_topic)))

    def execute(self, userdata):

        Logger.loginfo('looking for voice command ')
        if not self._connected:
            return 'fail'

        if self._sub.has_msg(self._topic):
            Logger.loginfo('getting message')
            message = self._sub.get_last_msg(self._topic)
            userdata.words = message.data
            self._sub.remove_last_msg(self._topic)
            return 'done'
        if (self.time-get_time() <= 0):
            return 'nothing'

    def on_enter(self, userdata):
        Logger.loginfo('entering marker state')

        self.time = get_time()+self.watchdog
        if not self._connected:
            (msg_path, msg_topic, fn) = rostopic.get_topic_type(self._topic)
            if msg_topic == self._topic:
                msg_type = self._get_msg_from_path(msg_path)
                self._sub = ProxySubscriberCached({self._topic: msg_type})
                self._connected = True
                Logger.loginfo('Successfully subscribed to previously unavailable topic %s' % self._topic)

            else:
                Logger.logwarn('Topic %s still not available, giving up.' % self._topic)
        if self._connected and self._sub.has_msg(self._topic):
            self._sub.remove_last_msg(self._topic)



    def _get_msg_from_path(self, msg_path):
        msg_import = msg_path.split('/')
        msg_module = '%s.msg' % (msg_import[0])
        package = __import__(msg_module, fromlist=[msg_module])
        clsmembers = inspect.getmembers(package, lambda member: inspect.isclass(member) and member.__module__.endswith(msg_import[1]))
        return clsmembers[0][1]
