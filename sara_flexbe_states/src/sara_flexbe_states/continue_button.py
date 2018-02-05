#!/usr/bin/env python

from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxySubscriberCached
import rostopic
import inspect


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
        self._topic = "/ui/continue"
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
        if self._connected and self._sub.has_msg(self._topic):
            message = self._sub.get_last_msg(self._topic)
            if message.data:
                return 'true'
            else:
                return 'false'


    def on_enter(self, userdata):
        Logger.loginfo('entering marker state')

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
