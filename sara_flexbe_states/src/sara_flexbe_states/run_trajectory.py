#!/usr/bin/env python

from flexbe_core import EventState, Logger
import rospy
from wm_trajectory_manager import save_trajectory

class RunTrajectory(EventState):
    """
    recois le nom d'un fichier de trajectoire en parametre et appelle le service run_trajectory offert par le trajectory manager
    -- file

    <= done
    """

    def __init__(self, file):
        """Constructor"""

        super(RunTrajectory, self).__init__(outcomes = ['done'])
        self.msg = save_trajectory(file)

    def execute(self, userdata):
        """Wait for action result and return outcome accordingly"""
            rospy.wait_for_service('/save_trajectory')
            serv = rospy.ServiceProxy('/save_trajectory', say_service)
            serv(self.msg)

return 'done'
