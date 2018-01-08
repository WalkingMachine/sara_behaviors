#!/usr/bin/env python
from __future__ import print_function
from flexbe_core import EventState, Logger
from moveit_commander import MoveGroupCommander
from geometry_msgs.msg import Point, Pose


class MoveitMove(EventState):
    '''
    Move the arm to a specific pose or point or named_target
    -- move                    wetter or not the arm should move or simply check if the move is possible
    -- waitForExecution     wait for execution to end before continuing

    ># pose     Pose      Targetpose.

    <= done     No error occurred.
    <= failed   The plan could't be done.
    '''

    def __init__(self, move=True, waitForExecution=True, group="RightArm"):
        # See example_state.py for basic explanations.
        super(MoveitMove, self).__init__(outcomes=['done', 'failed'], input_keys=['target'])
        self.move = move
        self.waitForExecution = waitForExecution
        self.group = MoveGroupCommander(group)
        self.tol = 0.0001
        self.result = None

    def execute(self, userdata):

        if self.result:
            return self.result

        if self.waitForExecution:
            curState = self.group.get_current_joint_values()
            diff = compareStates(curState, self.endState)
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
            Logger.loginfo(str(plan))
            # Logger.loginfo(str(plan.joint_trajectory.points))
            self.endState = plan.joint_trajectory.points[len(plan.joint_trajectory.points)-1].positions
            Logger.loginfo(str(self.endState))
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

    def on_pause(self):
        Logger.loginfo('Pausing movement')
        self.group.stop()

    def on_resume(self, userdata):
        self.on_enter(userdata)


def compareStates(state1, state2):
    diff = 0.0
    for i in range(len(state1)):
        diff = (state1[i] - state2[i]) ** 2
    return diff
