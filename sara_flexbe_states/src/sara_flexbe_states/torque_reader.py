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
        self.watchdogTime = None

        self._sub = ProxySubscriberCached({self._topic: JointState})
        self.initialTorque = None

    def execute(self, userdata):
        if self.initialTorque is None:
            self.watchdogTime = get_time()+self.watchdog
            if self._sub.has_msg(self._topic):
                message = self._sub.get_last_msg(self._topic)
                for i in range(len(message.name)):
                    if message.name[i] == self.Joint:
                        self.Joint = i
                        break
                self.initialTorque = message.effort[self.Joint]
                print("Initial torque is:"+str(self.initialTorque))
        else:

            if self._sub.has_msg(self._topic):
                torque = self._sub.get_last_msg(self._topic).effort[self.Joint]
                if abs(self.initialTorque - torque) >= self.Threshold:
                    Logger.loginfo('Reading torque :'+str(abs(self.initialTorque - torque)))
                    if self.timer < get_time():
                        userdata.torque = torque
                        return 'threshold'
                else:
                    self.timer = get_time() + self.min_time

            if (self.watchdogTime-get_time() <= 0):
                return "watchdog"

    def on_enter(self, userdata):
        self.initialTorque = None
