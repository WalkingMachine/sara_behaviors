#!/usr/bin/env python
from __future__ import print_function
from flexbe_core import EventState, Logger
from moveit_commander import MoveGroupCommander

class MoveArmPose(EventState):
    '''
    MoveArmPose move the arm to a specific pose
    -- wait     wait for execution

    ># pose     Pose      Targetpose.

    <= done     Finish job.
    <= failed   Job as failed.
    '''

    def __init__(self, wait=True):
        # See example_state.py for basic explanations.
        super(MoveArmPose, self).__init__(outcomes=['done', 'failed'], input_keys=['pose'])
        self.group = MoveGroupCommander("RightArm")
        self.plan = None
        self.wait = wait

    def execute(self, userdata):

        if self.group.execute(self.plan, wait=self.wait):
            return 'done'
        else:
            return 'failed'

    def on_enter(self, userdata):
        Logger.loginfo('Enter Move Arm')
        self.group.set_pose_target( userdata.pose )
        self.plan = self.group.plan()

    def on_exit(self, userdata):

        self.group.stop()