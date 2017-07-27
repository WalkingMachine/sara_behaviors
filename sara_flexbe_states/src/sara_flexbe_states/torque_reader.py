#!/usr/bin/env python

from flexbe_core import EventState, Logger
import rospy


from flexbe_core.proxy import ProxyPublisher
from std_msgs.msg import Float32


class ReadTorque(EventState):
    '''
    Reads torque of a joint.

    <= done            torque increase has been detected.

    '''

    def __init__(self):

        super(ReadTorque, self).__init__(outcomes=['done'])


    def on_enter(self, userdata):
        Logger.loginfo('Entering torque reader')
        self.initial_torque = rospy.Subscriber("/elbow_torque", Float32)

    def execute(self, userdata):
        self.torque = rospy.Subscriber("/elbow_torque", Float32)
        Logger.loginfo('Reading  torque from /elbow_torque topic: %f', self.torque)
        if self.initial_torque < self.torque:
            return 'done'