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
        self.result = None

    def execute(self, userdata):

        if self.result:
            return self.result

        if self.waitForExecution:
            curPose = self.group.get_current_pose().pose
            if type(userdata.target) is Pose:
                diff = comparePose(curPose, userdata.target)
            else:
                diff = comparePos(curPose.position, userdata.target)
            if diff < self.tol:
                Logger.loginfo('Target reached :)')
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
            xyz = [userdata.target.x, userdata.target.y, userdata.target.z]
            self.group.set_position_target(xyz)
        elif type(userdata.target) is str:
            Logger.loginfo('the target is a named_target')
            self.group.set_named_target(userdata.target)
        else:
            Logger.loginfo('ERROR in ' + str(self.name) + ' : target is not a Pose() nor a Point() nor a string')
            self.result = 'failed'

        Logger.loginfo('target defined')
        try:
            plan = self.group.plan()
        except:
            Logger.loginfo('Planning failed')
            self.result = 'failed'
            return

        Logger.loginfo('Plan done successfully')
        if self.move:
            Logger.loginfo('Initiating movement')
            self.group.execute(plan, wait=False)
            if not self.waitForExecution:
                self.result = "done"
        else:
            Logger.loginfo('The target is reachable')
            self.result = "done"

    def on_exit(self, userdata):
        Logger.loginfo('Stoping movement')
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

def comparePos(pos1, pos2):
    diff =  (pos1.x - pos2.x) ** 2
    diff += (pos1.y - pos2.y) ** 2
    diff += (pos1.z - pos2.z) ** 2
    return diff
