#!/usr/bin/env python
from __future__ import print_function
from flexbe_core import EventState, Logger
from moveit_commander import MoveGroupCommander


class GetArmPose(EventState):
    '''
    GetArmPose return the pose of the arm

    <# pose     Pose      Target waypoint for navigation.

    <= done     Finish job.
    '''

    def __init__(self):
        # See example_state.py for basic explanations.
        super(GetArmPose, self).__init__(outcomes=['done'], output_keys=['pose'])
        self.group = MoveGroupCommander("RightArm")

    def execute(self, userdata):

        return 'done'

    def on_enter(self, userdata):
        Logger.loginfo('Getting arm pose')
        self.group.get_current_pose()
