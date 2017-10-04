#!/usr/bin/env python
from __future__ import print_function
from flexbe_core import EventState, Logger
from geometry_msgs.msg import Pose
from wm_moveit_server.srv import move
import rospy
import moveit_commander as mc

class MoveArm(EventState):
    '''
    MoveArm move the arm to a specific pose

    ># pose     Pose      Targetpose.

    <= done     Finish job.
    <= failed   Job as failed.
    '''

    def __init__(self):
        # See example_state.py for basic explanations.
        super(MoveArm, self).__init__(outcomes=['done', 'failed'], input_keys=['pose'])
        self.robot = mc.RobotCommander()
        self.PS = mc.PlanningSceneInterface()
        self.group = mc.MoveGroupCommander("RightArm")
        self.plan = None

    def execute(self, userdata):

        if (self.group.execute(self.plan)):
            return 'done'  # One of the outcomes declared above.
        else:
            return 'failed'

    def on_enter(self, userdata):
        # This method is called when the state becomes active, a transition from another state to this one is taken.
        # It is primarily used to start actions which are associated with this state.
        Logger.loginfo('Enter Move Arm')
        self.group.set_pose_target( userdata.pose )
        self.plan = self.group.plan()

    def on_exit(self, userdata):

        self.group.stop()