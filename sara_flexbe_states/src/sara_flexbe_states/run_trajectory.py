#!/usr/bin/env python

from flexbe_core import EventState, Logger
import rospy
from wm_trajectory_manager.srv import run_trajectory, run_trajectoryRequest
from controller_manager_msgs.srv import SwitchController

class RunTrajectory(EventState):
    """
    recois le nom d'un fichier de trajectoire en parametre et appelle le service run_trajectory offert par le trajectory manager
    -- file     string      The .yaml file containing the trajectory
    -- duration     double      How long should we wait before stopping. In set to 0, will not wait and not stop.

    <= done     The trajectory has been initiated
    """

    def __init__(self, file="", duration=0):
        """Constructor"""

        super(RunTrajectory, self).__init__(outcomes = ['done'])
        self.msg = run_trajectoryRequest()
        self.msg.file = file
        self.duration = rospy.Duration.from_sec(duration)
        self.timer = None

    def execute(self, userdata):

        """Wait for action result and return outcome accordingly"""
        if self.timer+self.duration < rospy.Time.now():
            return 'done'


    def on_enter(self, userdata):
        # Set on the timer
        self.timer = rospy.Time.now()

        # Wtitch on the controller
        rospy.wait_for_service('/controller_manager/switch_controller')
        rospy.wait_for_service('/run_trajectory')
        try:
            switch_controller = rospy.ServiceProxy(
                '/controller_manager/switch_controller', SwitchController)
            ret = switch_controller(['sara_arm_trajectory_controller'],
                                    ['sara_arm_velocity_controller'], 2)

            serv = rospy.ServiceProxy('/run_trajectory', run_trajectory)
            serv = rospy.ServiceProxy('/run_trajectory', run_trajectory)
            serv(self.msg)

        except rospy.ServiceException, e:
            print "Service call failed: %s" % e

    def on_exit(self, userdata):
        if not self.duration.is_zero():
            # Wtitch on and off the controller to stop it
            rospy.wait_for_service('/controller_manager/switch_controller')
            try:
                switch_controller = rospy.ServiceProxy(
                    '/controller_manager/switch_controller', SwitchController)
                ret = switch_controller(['sara_arm_velocity_controller'],
                                        ['sara_arm_trajectory_controller'], 2)

                switch_controller = rospy.ServiceProxy(
                    '/controller_manager/switch_controller', SwitchController)
                ret = switch_controller(['sara_arm_trajectory_controller'],
                                        ['sara_arm_velocity_controller'], 2)

            except rospy.ServiceException, e:
                print "Service call failed: %s" % e
