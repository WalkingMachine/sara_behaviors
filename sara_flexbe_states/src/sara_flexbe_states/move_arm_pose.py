#!/usr/bin/env python
from __future__ import print_function
from flexbe_core import EventState, Logger
from moveit_commander import MoveGroupCommander
from multiprocessing import Process

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
        self.error = None
        self.group = MoveGroupCommander("RightArm")

    def execute(self, userdata):
        Logger.loginfo('Moving Arm')
        if self.outcome:
            return self.outcome

    def on_enter(self, userdata):
        self.thread = Process(target=self.run)
        self.thread.start()


    def on_exit(self, userdata):
        self.group.stop()

    def run(self):
        Logger.loginfo('Enter Move Arm')
        self.group.set_pose_target(self.pose)
        try:
            self.plan = self.group.plan()
        except:
            self.error = True

        if self.error:
            try:
                self.plan = self.group.plan()
            except:
                self.outcome = "failed"
                return

        if self.group.execute(self.plan, wait=self.wait):
            self.outcome = "done"
            return
        else:
            self.outcome = "failed"
            return