#!/usr/bin/env python
from __future__ import print_function
from flexbe_core import EventState, Logger
from moveit_commander import MoveGroupCommander

class MoveArmNamedPose(EventState):
    '''
    MoveArmPose receive a ROS pose as input and launch a ROS service with the same joint configuration
    -- pose_name     The name of the pose
    -- wait        Wait for execution

    ># joint_state     state      State Configuration.

    <= done     Finish job.
    <= failed   Job as failed.
    '''

    def __init__(self, pose_name, wait=True):

        # See example_state.py for basic explanations.
        super(MoveArmNamedPose, self).__init__(outcomes=['done', 'failed'])
        self.group = MoveGroupCommander("RightArm")
        self.plan = None
        self.pose_name = pose_name
        self.wait = wait
        self.error = False

    def execute(self, userdata):
        if self.error:
            try:
                self.plan = self.group.plan()
            except:
                return 'failed'

        if (self.group.execute(self.plan, wait=self.wait)):
            return 'done'  # One of the outcomes declared above.
        else:
            return 'failed'


    def on_enter(self, userdata):

        self.group.set_named_target(self.pose_name)
        try:
            self.plan = self.group.plan()
        except:
            self.error = True

    def on_exit(self, userdata):

        self.group.stop()