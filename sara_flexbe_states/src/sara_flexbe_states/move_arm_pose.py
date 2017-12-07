#!/usr/bin/env python
from __future__ import print_function
from flexbe_core import EventState, Logger
from moveit_commander import MoveGroupCommander
from multiprocessing import Process


def MoveArmRun(group, pose, wait):
    Logger.loginfo('Enter Move Arm')
    group.set_pose_target(pose)
    try:
        plan = group.plan()
    except:
        return "failed"
    Logger.loginfo('Plan done, stating movement')

    if group.execute(plan, wait=wait):
        return "done"
    else:
        return "failed"


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

    def execute(self, userdata):
        Logger.loginfo('Moving Arm')
        if self.thread.is_alive():
            return self.thread.exitcode

    def on_enter(self, userdata):
        self.thread = Process(target=MoveArmRun, args=[self.group, userdata.pose, self.wait])
        self.thread.start()

    def on_exit(self, userdata):
        self.group.stop()


