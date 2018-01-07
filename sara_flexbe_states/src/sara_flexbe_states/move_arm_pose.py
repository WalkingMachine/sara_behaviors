#!/usr/bin/env python
from __future__ import print_function
from flexbe_core import EventState, Logger
from moveit_commander import MoveGroupCommander
from geometry_msgs.msg import Point, Pose


class MoveArmPose(EventState):
    '''
    MoveArmPose move the arm to a specific pose
    -- wait     wait for execution

    ># pose     Pose      Targetpose.

    <= done     Finish job.
    <= failed   Job as failed.
    '''



    def __init__(self, move=True, waitForExecution=True, group="RightArm"):
        # See example_state.py for basic explanations.
        super(MoveArmPose, self).__init__(outcomes=['done', 'failed'], input_keys=['target'])
        self.move = move
        self.waitForExecution = waitForExecution
        self.group = MoveGroupCommander(group)
        self.tol = 0.0001

    def execute(self, userdata):
        if self.waitForExecution:
            curPose = self.group.get_current_pose().pose
            diff = comparePose(curPose, userdata.pose)
            # Logger.loginfo("diff = " + str(diff))
            if diff < self.tol:
                return "done"
        else:
            return "done"

    def on_enter(self, userdata):
        Logger.loginfo('Enter Move Arm')

        if type(userdata.target) is Pose:
            Logger.loginfo('the target is a pose')
            self.group.set_pose_target(userdata.target)
        elif type(userdata.target) is Point:
            Logger.loginfo('the target is a point')
            self.group.set_position_target(userdata.target)
        elif type(userdata.target) is str:
            Logger.loginfo('the target is a named_target')
            self.group.set_named_target(self.pose_name)
        else:
            Logger.loginfo('ERROR in ' + str(self.name) + ' : target is not a Pose() nor a Point() nor a string')
            return 'failed'

        Logger.loginfo('target defined')
        try:
            plan = self.group.plan()
        except:
            Logger.loginfo('Planning failed')
            return 'failed'

        Logger.loginfo('Plan done, stating movement')

        if not self.move or self.group.execute(plan, wait=False):
            return "done"
        else:
            return "failed"

    def on_exit(self, userdata):
        self.group.stop()

def comparePose(pose1, pose2):
    diff =  (pose1.position.x - pose2.position.x) ** 2
    diff += (pose1.position.y - pose2.position.y) ** 2
    diff += (pose1.position.z - pose2.position.z) ** 2
    diff += (pose1.orientation.x - pose2.orientation.x) ** 2
    diff += (pose1.orientation.y - pose2.orientation.y) ** 2
    diff += (pose1.orientation.z - pose2.orientation.z) ** 2
    diff += (pose1.orientation.w - pose2.orientation.w) ** 2
    return diff