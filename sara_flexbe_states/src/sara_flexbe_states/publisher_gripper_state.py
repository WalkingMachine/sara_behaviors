#!/usr/bin/env python


from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxyPublisher
from control_msgs.msg import _GripperCommandActionGoal, GripperCommandActionGoal

'''
Created on 31.01.2017

@author: Alberto Romay
'''


class PublisherGripperState(EventState):
    '''
    Publishes a command for the gripper.

    >= width      float        0-255 desired gripper width.
    >= effort     float        0-255 desired gripper effort.

    <= done       Done publishing.

    '''

    def __init__(self):
        '''
        Constructor
        '''
        super(PublisherGripperState, self).__init__(outcomes=['done'], input_keys=['width','effort'])

        self._topic = 'sara_gripper_action_controller/gripper_cmd/goal'
        self._pub = ProxyPublisher({self._topic: GripperCommandActionGoal})

    def execute(self, userdata):
        return 'done'

    def on_enter(self, userdata):
        msg = GripperCommandActionGoal()
        msg.goal.command.position = userdata.width
        msg.goal.command.max_effort = userdata.effort
        self._pub.publish(self._topic, msg)

