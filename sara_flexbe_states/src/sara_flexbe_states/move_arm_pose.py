#!/usr/bin/env python
from __future__ import print_function
from flexbe_core import EventState, Logger
from moveit_commander import MoveGroupCommander
import threading

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
        self.group = MoveGroupCommander("RightArm")

    def execute(self, userdata):
        Logger.loginfo('Moving Arm')
        nb = threading.activeCount()
        Logger.loginfo(str(nb))
        if self.thread.outcome:
            return self.thread.outcome

    def on_enter(self, userdata):
        self.thread = self.myThread(1, "moving_arm", 1, userdata, self.wait, self.group)
        self.thread.start()

    def on_exit(self, userdata):
        self.group.stop()


    class myThread(threading.Thread):
        def __init__(self, threadID, name, counter, userdata, wait, group):
            threading.Thread.__init__(self)
            self.threadID = threadID
            self.name = name
            self.counter = counter
            self.group = group
            self.plan = None
            self.pose = userdata.pose
            self.error = False
            self.wait = wait
            self.outcome = None

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