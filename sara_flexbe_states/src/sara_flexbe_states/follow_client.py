#!/usr/bin/env python

from flexbe_core import EventState, Logger
import rospy
from wm_people_follower.srv import peopleFollower

class FollowClient(EventState):
    """
    Make sara say something

    -- command     int      1=lock, 2=follow, 3=unfollow, 4=unlock

    <= done                what's said is said
    """

    def __init__(self, command):
        """Constructor"""

        super(FollowClient, self).__init__(outcomes = ['done', 'fail'])
        self.msg = command
    def execute(self, userdata):
        """Wait for action result and return outcome accordingly"""

        rospy.wait_for_service('/wm_people_follow')
        serv = rospy.ServiceProxy('/wm_people_follow', peopleFollower)
        resp = serv(self.msg).response
        print(resp)
        if resp==1:
            return 'done'
        return 'fail'
