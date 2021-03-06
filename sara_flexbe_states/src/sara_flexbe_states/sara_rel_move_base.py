#!/usr/bin/env python

from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxyActionClient

from actionlib_msgs.msg import GoalStatus
from move_base_msgs.msg import *
from std_srvs.srv import Empty
from geometry_msgs.msg import Pose, Pose2D, Quaternion, Point
from tf import transformations
import rospy

"""
Created on 11/19/2015
Modified on 05/21/2017
@author: Spyros Maniatopoulos

@mofificator: Nicolas Nadeau & Philippe La Madeleine
"""

class SaraRelMoveBase(EventState):
    """
    Navigates Sara to a relative position and orientation using move_base.

    ># pose     Pose2D      Target waypoint for navigation.

    <= arrived                  Navigation to target pose succeeded.
    <= failed                   Navigation to target pose failed.
    """

    def __init__(self):
        """Constructor"""

        super(SaraRelMoveBase, self).__init__( outcomes=['arrived', 'failed'],
                                            input_keys=['pose'])

        self._action_topic = "/move_base"

        self._client = ProxyActionClient({self._action_topic: MoveBaseAction})

        self._arrived = False
        self._failed = False
        self._pose = None


    def execute(self, userdata):
        """Wait for action result and return outcome accordingly"""

        if self._arrived:
            return 'arrived'
        if self._failed:
            return 'failed'

        if self._client.has_result(self._action_topic):
            status = self._client.get_state(self._action_topic)
            if status == GoalStatus.SUCCEEDED:
                self._arrived = True
                return 'arrived'
            elif status in [GoalStatus.PREEMPTED, GoalStatus.REJECTED,
                            GoalStatus.RECALLED, GoalStatus.ABORTED]:
                Logger.logwarn('Navigation failed: %s' % str(status))
                self._failed = True
                return 'failed'


    def on_enter(self, userdata):
        """Create and send action goal"""

        self._arrived = False
        self._failed = False

        # Create and populate action goal
        if type(userdata.pose)==Pose:
            self._pose = userdata.pose
        elif type(userdata.pose)==Pose2D:
            pt = Point(x=userdata.pose.x, y=userdata.pose.y)
            qt = transformations.quaternion_from_euler(0, 0, userdata.pose.theta)
            self._pose = Pose(position=pt, orientation=Quaternion(*qt))

        self.setGoal(self._pose)

    def on_exit(self, userdata):
        if not self._client.has_result(self._action_topic):
            self._client.cancel(self._action_topic)
            Logger.loginfo('Cancelled active action goal.')

    def on_pause(self):
        pose = self._client.get_feedback(self._action_topic)
        self.setGoal(pose)

    def on_resume(self, userdata):
        self.setGoal(self._pose)

    def setGoal(self, pose):

        rospy.wait_for_service('/move_base/clear_costmaps')
        serv = rospy.ServiceProxy('/move_base/clear_costmaps', Empty)
        serv()
        goal = MoveBaseGoal()

        goal.target_pose.pose = pose

        goal.target_pose.header.frame_id = "base_link"
        # goal.target_pose.header.stamp.secs = 5.0

        # Send the action goal for execution
        try:
            self._client.send_goal(self._action_topic, goal)
        except Exception as e:
            Logger.logwarn("Unable to send navigation action goal:\n%s" % str(e))
            self._failed = True