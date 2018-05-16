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

        super(ReadTorque, self).__init__(outcomes=['threshold', 'watchdog', 'fail'], output_keys=['torque'])
        self.watchdog = watchdog
        self.Threshold = Threshold
        self.Joint = Joint
        self.min_time = min_time
        self.timer = 0
        self._topic = "/joint_states"
        self._connected = False

        self._sub = ProxySubscriberCached({self._topic: JointState})

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
                        userdata.torque = self.torque
                        return 'threshold'
                else:
                    self.timer = get_time() + self.min_time

            if (self.watchdogTime-get_time() <= 0):
                return "watchdog"

        self.initialTorque = None
