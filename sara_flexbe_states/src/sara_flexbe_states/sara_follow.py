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
    -- ReplanPeriod   float       Time in seconds between each replanning for movebase

    ># ID     int      entity ID.

    """

    def __init__(self, distance=1, ReplanPeriod=0.5):
        """Constructor"""

        super(SaraFollow, self).__init__(outcomes=['failed'],
                                         input_keys=['ID'])

        # Prepare the action client for move_base
        self._action_topic = "/move_base"
        self._client = ProxyActionClient({self._action_topic: MoveBaseAction})

        # Initialise the subscribers
        self.entities_topic = "/entities"
        self._pose_topic = "/robot_pose"
        self._sub = ProxySubscriberCached({self._pose_topic: Pose, self.entities_topic: Entities})

        # Get the parameters
        self.targetDistance = distance
        self.ReplanPeriod = ReplanPeriod

        # Initialise the status variables
        self.MyPose = None
        self.lastPlanTime = 0

    def execute(self, userdata):
        """Wait for action result and return outcome accordingly"""

        # Initialise the Entity
        Entity = None

        # Get my last position
        if self._sub.has_msg(self._pose_topic):
            self.MyPose = self._sub.get_last_msg(self._pose_topic)

        # Get the entity's position
        if self._sub.has_msg(self.entities_topic):
            message = self._sub.get_last_msg(self.entities_topic)
            for entity in message.entities:
                if entity.ID == userdata.ID:
                    Entity = entity

        # If both my pose and the entyties are known, we start following.
        if self.MyPose and Entity:
            # Calculate a new goal if the desired period has passed.
            if self.lastPlanTime+self.ReplanPeriod < rospy.get_time():
                self.lastPlanTime = rospy.get_time()
                self.setGoal(self.generateGoal(self.MyPose.position, Entity.position))

            # Check if movebase can reach the goal
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
        self.Counter = 0

    def on_exit(self, userdata):
        if not self._client.has_result(self._action_topic):
            self._client.cancel(self._action_topic)
            Logger.loginfo('Cancelled active action goal.')

    def on_pause(self):
        pose = self._client.get_feedback(self._action_topic)
        self.setGoal(pose)



    def generateGoal(self, MyPosition, EntityPosition):
        # Calculate the safe distance to reach
        GoalPose = Pose()

        # Calculate the diference in position
        dx = EntityPosition.x - MyPosition.x
        dy = EntityPosition.y - MyPosition.y

        # Calculate the desired distance to the person.
        # If the person is too close, the robot must not go backward.
        distanceToPerson = max(self.targetDistance, (dx ** 2 + dy ** 2) ** 0.5)

        # Calculate the desired position to reach.
        GoalPose.position.x = EntityPosition.x - dx / distanceToPerson * self.targetDistance
        GoalPose.position.y = EntityPosition.y - dy / distanceToPerson * self.targetDistance

        # Calculate the desired direction.
        angle = math.atan2(dy, dx)
        qt = quaternion_from_euler(0, 0, angle)
        GoalPose.orientation.w = qt[3]
        GoalPose.orientation.x = qt[0]
        GoalPose.orientation.y = qt[1]
        GoalPose.orientation.z = qt[2]

        return GoalPose


    def setGoal(self, pose):

        # Generate the goal
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