#!/usr/bin/env python

from flexbe_core import EventState, Logger
import rostopic
import inspect
from rospy.rostime import get_time
from flexbe_core.proxy import ProxySubscriberCached
from sensor_msgs.msg import JointState


class ReadTorque(EventState):
    '''
    Reads torque of a joint.

    <= done            torque increase has been detected.

    '''

    def __init__(self, watchdog, Joint, Threshold, min_time):

        super(ReadTorque, self).__init__(outcomes=['threshold', 'watchdog', 'fail'])
        self.watchdog = watchdog
        self.Threshold = Threshold
        self.Joint = Joint
        self.min_time = min_time
        self.timer = 0
        self._topic = "/joint_states"
        self._connected = False


    def execute(self, userdata):
        if not self._connected:
            return 'fail'

        if self.initialTorque == None:
            self.watchdogTime = get_time()+self.watchdog
            if self._sub.has_msg(self._topic):
                message = self._sub.get_last_msg(self._topic)
                for i in range(len(message.name)):
                    if message.name[i] == self.Joint:
                        self.Joint = i
                        break
                self.initialTorque = message.effort[self.Joint]
        else:

            if self._sub.has_msg(self._topic):
                self.torque = self._sub.get_last_msg(self._topic).effort[self.Joint]
                if abs(self.initialTorque - self.torque) >= self.Threshold:
                    Logger.loginfo('Reading torque :'+str(abs(self.initialTorque - self.torque)))
                    if self.timer < get_time():
                        return 'threshold'
                else:
                    self.timer = get_time() + self.min_time

            if (self.watchdogTime-get_time() <= 0):
                return "watchdog"

    def on_enter(self, userdata):
        Logger.loginfo('Entering torque reader')

        if not self._connected:
            (msg_path, msg_topic, fn) = rostopic.get_topic_type(self._topic)
            if msg_topic == self._topic:
                msg_type = self._get_msg_from_path(msg_path)
                self._sub = ProxySubscriberCached({self._topic: msg_type})
                self._connected = True
                Logger.loginfo('Successfully subscribed to previously unavailable topic %s' % self._topic)
            else:
                Logger.logwarn('Topic %s still not available, giving up.' % self._topic)

        (msg_path, msg_topic, fn) = rostopic.get_topic_type(self._topic)
        if msg_topic == self._topic:
            msg_type = self._get_msg_from_path(msg_path)
            self._sub = ProxySubscriberCached({self._topic: msg_type})
            self._connected = True
            Logger.loginfo('connecting marker state to '+self._topic)
        else:
            Logger.logwarn('Topic %s for state %s not yet available.\nFound: %s\nWill try again when entering the state...' % (self._topic, self.name, str(msg_topic)))

        self.initialTorque = None



    def _get_msg_from_path(self, msg_path):
        msg_import = msg_path.split('/')
        msg_module = '%s.msg' % (msg_import[0])
        package = __import__(msg_module, fromlist=[msg_module])
        clsmembers = inspect.getmembers(package, lambda member: inspect.isclass(member) and member.__module__.endswith(msg_import[1]))
        return clsmembers[0][1]
