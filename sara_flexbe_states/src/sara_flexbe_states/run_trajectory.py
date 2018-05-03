#!/usr/bin/env python

from flexbe_core import EventState, Logger
import rospy
from wm_trajectory_manager.srv import run_trajectory, run_trajectoryRequest

class RunTrajectory(EventState):
    """
    recois le nom d'un fichier de trajectoire en parametre et appelle le service run_trajectory offert par le trajectory manager
    -- file     string      The .yaml file containing the trajectory

    <= done     The trajectory has been initiated
    """

    def __init__(self, file):
        """Constructor"""

        super(RunTrajectory, self).__init__(outcomes = ['done'])
        self.msg = run_trajectoryRequest()
        self.msg.file = file

    def execute(self, userdata):
        """Wait for action result and return outcome accordingly"""
        rospy.wait_for_service('/run_trajectory')
        serv = rospy.ServiceProxy('/run_trajectory', run_trajectory)
        serv(self.msg)

        return 'done'