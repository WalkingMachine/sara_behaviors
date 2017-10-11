#!/usr/bin/env python


from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxyPublisher, ProxySubscriberCached
from control_msgs.msg import GripperCommandActionGoal, GripperCommandActionFeedback
import rostopic
from rospy.rostime import get_time
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

    def __init__(self):
        '''
        Constructor
        '''
        super(SetGripperState, self).__init__(outcomes=['object', 'no_object'], input_keys=['width','effort'], output_keys=['object_size'])

        self._topic = 'sara_gripper_action_controller/gripper_cmd/goal'
        self._topic = 'sara_gripper_action_controller/gripper_cmd/feedback'
        self._pub = ProxyPublisher({self._topic: GripperCommandActionGoal})
        self.sub = ProxySubscriberCached
        (msg_path, msg_topic, fn) = rostopic.get_topic_type(self._topic)

        if msg_topic == self._topic:
            msg_type = self._get_msg_from_path(msg_path)
            self._sub = ProxySubscriberCached({self._topic: msg_type})
            self._connected = True
            Logger.loginfo('connecting marker state to '+self._topic)
        else:
            Logger.logwarn('Topic %s for state %s not yet available.\nFound: %s\nWill try again when entering the state...' % (self._topic, self.name, str(msg_topic)))

    def execute(self, userdata):
        if self.time-get_time() <= 0:
            if self._sub.has_msg(self._topic):
                message = self._sub.get_last_msg(self._topic)
                userdata.object_size = message.feedback.position()
                if abs( userdata.object_size-self.width) > 0.001:
                    return 'object'
                else:
                    return 'no_object'
            return 'object'

    def on_enter(self, userdata):
        msg = GripperCommandActionGoal()
        msg.goal.command.position = userdata.width
        msg.goal.command.max_effort = userdata.effort
        self._pub.publish(self._topic, msg)

        self.time = get_time()
        if not self._connected:
            (msg_path, msg_topic, fn) = rostopic.get_topic_type(self._topic)
            if msg_topic == self._topic:
                msg_type = self._get_msg_from_path(msg_path)
                self._sub = ProxySubscriberCached({self._topic: msg_type})
                self._connected = True
                Logger.loginfo('Successfully subscribed to previously unavailable topic %s' % self._topic)
            else:
                Logger.logwarn('Topic %s still not available, giving up.' % self._topic)

    def _get_msg_from_path(self, msg_path):
        msg_import = msg_path.split('/')
        msg_module = '%s.msg' % (msg_import[0])
        package = __import__(msg_module, fromlist=[msg_module])
        clsmembers = inspect.getmembers(package, lambda member: inspect.isclass(member) and member.__module__.endswith(msg_import[1]))
        return clsmembers[0][1]
