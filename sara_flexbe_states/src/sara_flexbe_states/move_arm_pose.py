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



    def __init__(self, move=True, wait=True):
        # See example_state.py for basic explanations.
        super(MoveArmPose, self).__init__(outcomes=['done', 'failed'], input_keys=['pose'])
        self.move = move
        self.wait = wait
        self.thread = None
        self.outcome = None
        self.group = MoveGroupCommander("RightArm")
        self.tol = self.group.get_goal_position_tolerance()**2

    def execute(self, userdata):
        curPose = self.group.get_current_pose().pose
        diff = (curPose.position.x - userdata.pose.position.x)**2 \
            +(curPose.position.y - userdata.pose.position.y)**2 \
            +(curPose.position.z - userdata.pose.position.z)**2
        Logger.loginfo("diff = "+str(diff))
        if not self.wait or diff < self.tol:
            return "done"

    def on_enter(self, userdata):
        Logger.loginfo('Enter Move Arm')
        self.group.set_pose_target(userdata.pose)
        Logger.loginfo('target defined')
        try:
            plan = self.group.plan()
        except:
            return 'failed'

        Logger.loginfo('Plan done, stating movement')

        if self.group.execute(plan, wait=False):
            return "done"
        else:
            return "failed"

    def on_exit(self, userdata):
        self.group.stop()


