#!/usr/bin/env python


from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxyPublisher, ProxySubscriberCached
from control_msgs.msg import GripperCommandActionGoal
import rostopic
import inspect

'''
Created on 31.01.2017

@author: Philippe La Madeleine
'''


class SetGripperState(EventState):
    '''
    Publishes a command for the gripper.

    >= width        float        desired gripper width in meter.
    >= effort       float        desired gripper effort.
    <= object_size   float       result width.

    <# object       an object has been gripped
    ># no_object    no object gripped

    '''

    def __init__(self, width, effort):
        '''
        Constructor
        '''
        super(SetGripperState, self).__init__(outcomes=['object', 'no_object'], output_keys=['object_size'])

        self.width = width
        self.effort = effort
        self._connected  = False

        self._topic = '/sara_gripper_action_controller/gripper_cmd/goal'
        self._topic_result = '/sara_gripper_action_controller/gripper_cmd/result'

        self._pub = ProxyPublisher({self._topic: GripperCommandActionGoal})

        (msg_path, msg_topic, fn) = rostopic.get_topic_type(self._topic_result)
        if msg_topic == self._topic_result:
            msg_type = self._get_msg_from_path(msg_path)
            self._sub = ProxySubscriberCached({self._topic_result: msg_type})
            self._connected = True

            Logger.loginfo('connecting marker state to ' + self._topic_result)
        else:
            Logger.logwarn('Topic %s for state %s not yet available.\nFound: %s\nWill try again when entering the state...' % (self._topic_result, self.name, str(msg_topic)))

    def execute(self, userdata):

        if not self._connected:
            userdata.object_size = 0
            return 'no_object'

        if self._sub.has_msg(self._topic_result):
            message = self._sub.get_last_msg(self._topic_result)
            size = message.result.position
            self._sub.remove_last_msg(self._topic_result)
            userdata.object_size = size
            if abs( size-self.width) > 0.006:
                return 'object'
            else:
                return 'no_object'

    def on_enter(self, userdata):
        msg = GripperCommandActionGoal()
        msg.goal.command.position = self.width
        msg.goal.command.max_effort = self.effort
        self._pub.publish(self._topic, msg)

        if not self._connected:
            (msg_path, msg_topic, fn) = rostopic.get_topic_type(self._topic_result)
            if msg_topic == self._topic_result:
                msg_type = self._get_msg_from_path(msg_path)
                self._sub = ProxySubscriberCached({self._topic_result: msg_type})
                self._connected = True
                Logger.loginfo('Successfully subscribed to previously unavailable topic %s' % self._topic_result)
                self._sub.remove_last_msg(self._topic_result)
            else:
                Logger.logwarn('Topic %s still not available, giving up.' % self._topic_result)


    def _get_msg_from_path(self, msg_path):
        msg_import = msg_path.split('/')
        msg_module = '%s.msg' % (msg_import[0])
        package = __import__(msg_module, fromlist=[msg_module])
        clsmembers = inspect.getmembers(package, lambda member: inspect.isclass(member) and member.__module__.endswith(msg_import[1]))
        return clsmembers[0][1]
