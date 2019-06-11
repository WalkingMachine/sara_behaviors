#!/usr/bin/env python
from __future__ import print_function
from flexbe_core import EventState, Logger
from moveit_commander import MoveGroupCommander
from geometry_msgs.msg import Pose
import copy


class MoveitMoveCartesian(EventState):
    '''
    Move the arm between two specific poses or points or named_targets
    -- move                 Bool 	Whether or not the arm should move or simply check if the move is possible
    -- waitForExecution     Bool	Wait for execution to end before continuing
    -- group		    string	Name of the Moveit Planning group

    ># targetPose   Pose      Pose to reach

    <= done     No error occurred.
    <= failed   The plan could't be done.
    '''
    
    def __init__(self, move=True, waitForExecution=True, group="RightArm"):
        # See example_state.py for basic explanations.
        super(MoveitMoveCartesian, self).__init__(outcomes=['done', 'failed'], input_keys=['targetPose'])
        self.move = move
        self.waitForExecution = waitForExecution
        self.group = MoveGroupCommander(group)
        self.tol = 0.06
        self.result = None
        self.count = 0
        self.countlimit = 0
        self.movSteps = 0.01
        self.jumpThresh = 0.0

    def execute(self, userdata):
        if self.result:
            return self.result
        
        if self.waitForExecution:
            curState = self.group.get_current_joint_values()
            diff = compareStates(curState, self.endState)
            print("diff=" + str(diff))
            if diff < self.tol:
                self.count += 1
                if self.count > 3:
                    Logger.loginfo('Target reached :)')
                    return "done"
            else:
                self.count = 0
        else:
            return "done"
    
    
    def on_enter(self, userdata):
        Logger.loginfo('Enter Move Arm')
        
        if type(userdata.targetPose) is Pose:
            Logger.loginfo('target is a pose')
            waypoints = [self.group.get_current_pose().pose, copy.deepcopy(userdata.targetPose)]
            try:
                (plan, fraction) = self.group.compute_cartesian_path(
                    waypoints,
                    self.movSteps,
                    self.jumpThresh)
            except:
                Logger.loginfo('Planning failed; could not compute path')
                self.result = 'failed'
                return
        
        else:
            Logger.loginfo('ERROR in ' + str(self.name) + ' : target is not a Pose()')
            self.result = 'failed'
    
        Logger.loginfo('target defined')
        
        try:
            Logger.loginfo(str(plan))
            self.endState = plan.joint_trajectory.points[len(plan.joint_trajectory.points) - 1].positions
            Logger.loginfo(str(self.endState))
        except:
            Logger.loginfo('Planning failed; path is invalid')
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
        Logger.loginfo('Stopping movement')
        self.group.stop()
    
    
    def on_pause(self):
        Logger.loginfo('Pausing movement')
        self.group.stop()
    
    
    def on_resume(self, userdata):
        self.on_enter(userdata)
    

def compareStates(state1, state2):
    diff = 0.0
    for i in range(len(state1)):
        diff += (state1[i] - state2[i]) ** 2
    return diff ** 0.5
