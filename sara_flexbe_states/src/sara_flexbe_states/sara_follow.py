#!/usr/bin/env python

from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxyActionClient

from actionlib_msgs.msg import GoalStatus
from move_base_msgs.msg import *
from std_srvs.srv import Empty
import rospy
from geometry_msgs.msg import Pose, Point, Quaternion, Pose2D
from tf import transformations
from tf.transformations import quaternion_from_euler
from sara_msgs.msg import Entities
from flexbe_core.proxy import ProxySubscriberCached
import math

"""
Created on 11/19/2015
Modified on 05/21/2017
@author: Spyros Maniatopoulos

@mofificator: Nicolas Nadeau & Philippe La Madeleine
"""

class SaraFollow(EventState):
    """
    Make Sara follow an entity using move_base.
    -- Distance     float       distance to keep between sara and the entity

    ># ID     int      entity ID.

    """

    def __init__(self, distance):
        """Constructor"""

        super(SaraFollow, self).__init__(outcomes=['failed'],
                                         input_keys=['ID'])

        self._action_topic = "/move_base"

        self._client = ProxyActionClient({self._action_topic: MoveBaseAction})

        self.entities_topic = "/entities"
        self._pose_topic = "/robot_pose"
        self._sub = ProxySubscriberCached({self._pose_topic: Pose, self.entities_topic: Entities})

        self.distance = distance
        self.MyPose = None
        self.Entity = None
        self.count = 0
        self.LastGoal = None

    def execute(self, userdata):
        """Wait for action result and return outcome accordingly"""

        # self.count += 1
        # if self.count > 10:
        #     self.count = 0
        #     return



        self.Entity = None

        # Get my last position
        if self._sub.has_msg(self._pose_topic):
            self.MyPose = self._sub.get_last_msg(self._pose_topic)

        # Get the entity's position
        if self._sub.has_msg(self.entities_topic):
            message = self._sub.get_last_msg(self.entities_topic)
            for entity in message.entities:
                if entity.ID == userdata.ID:
                    self.Entity = entity

        if self.MyPose and self.Entity:

            # Calculate the safe distance to reach
            GoalPose = Pose()

            length = ((self.Entity.position.x - self.MyPose.position.x) ** 2 + (
                        self.Entity.position.y - self.MyPose.position.y) ** 2) ** 0.5
            GoalPose.position.x = self.Entity.position.x - (
                        self.Entity.position.x - self.MyPose.position.x) / length * self.distance
            GoalPose.position.y = self.Entity.position.y - (
                        self.Entity.position.y - self.MyPose.position.y) / length * self.distance

            angle = math.atan2((self.Entity.position.y - self.MyPose.position.y), (self.Entity.position.x - self.MyPose.position.x))
            qt = quaternion_from_euler(0, 0, angle)
            GoalPose.orientation.w = qt[3]
            GoalPose.orientation.x = qt[0]
            GoalPose.orientation.y = qt[1]
            GoalPose.orientation.z = qt[2]

            self.setGoal(GoalPose)


            if self._client.has_result(self._action_topic):
                status = self._client.get_state(self._action_topic)
                if status in [GoalStatus.PREEMPTED, GoalStatus.REJECTED,
                                GoalStatus.RECALLED, GoalStatus.ABORTED]:
                    Logger.logwarn('Navigation failed: %s' % str(status))
                    return 'failed'


    def on_enter(self, userdata):
        """Clean the costmap"""
        rospy.wait_for_service('/move_base/clear_costmaps')
        serv = rospy.ServiceProxy('/move_base/clear_costmaps', Empty)
        serv()
        self.MyPose = None
        self.Entity = None

    def on_exit(self, userdata):
        if not self._client.has_result(self._action_topic):
            self._client.cancel(self._action_topic)
            Logger.loginfo('Cancelled active action goal.')

    def on_pause(self):
        pose = self._client.get_feedback(self._action_topic)
        self.setGoal(pose)

    def setGoal(self, pose):



        if self.LastGoal:
            dist = ((self.LastGoal.position.x - pose.position.x) ** 2
                    + (self.LastGoal.position.x - pose.position.x) ** 2
                    + (self.LastGoal.position.x - pose.position.x) ** 2) ** 0.5
            if dist < 0.5:
                return
        self.LastGoal = pose

        goal = MoveBaseGoal()

        goal.target_pose.pose = pose

        goal.target_pose.header.frame_id = "map"

        # Send the action goal for execution
        try:
            Logger.loginfo("sending goal" + str(goal))
            self._client.send_goal(self._action_topic, goal)
        except Exception as e:
            Logger.logwarn("Unable to send navigation action goal:\n%s" % str(e))
            self._failed = True