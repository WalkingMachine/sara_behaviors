#!/usr/bin/env python

from flexbe_core import EventState, Logger
import rospy
from geometry_msgs.msg import PoseStamped
from tf.transformations import euler_from_quaternion
from flexbe_core.proxy import ProxySubscriberCached
from flexbe_core.proxy import ProxyActionClient
from actionlib_msgs.msg import GoalStatus
from geometry_msgs.msg import Pose, Pose2D, Quaternion, Point
from move_base_msgs.msg import *
from std_msgs.msg import Float64
from tf import transformations

"""
Created on 10/25/2018
@author: Philippe La Madeleine
"""

class LookAtSound(EventState):
    """
    Make Sara's head keep looking at the strongest source of sounds.
    """

    def __init__(self, moveBase=False):
        """Constructor"""

        super(LookAtSound, self).__init__(outcomes=['done'])
        self.MoveBase = moveBase

        # Subscriber config
        self.soundsTopic = "/direction_of_arrival"
        self._sub = ProxySubscriberCached({self.soundsTopic: PoseStamped})

        # Publisher config
        self.pubPitch = rospy.Publisher("/sara_head_pitch_controller/command", Float64, queue_size=1)
        self.pubYaw = rospy.Publisher("/sara_head_yaw_controller/command", Float64, queue_size=1)
        self.msg = Float64()


        # action client
        self._action_topic = "/move_base"
        self._client = ProxyActionClient({self._action_topic: MoveBaseAction})


    def execute(self, userdata):

        # If a new sound direction is detected.
        if self._sub.has_msg(self.soundsTopic):
            message = self._sub.get_last_msg(self.soundsTopic)
            orientation = message.pose.orientation
            orient_quat = [orientation.x, orientation.y, orientation.z, orientation.w]
            roll, pitch, yaw = euler_from_quaternion(orient_quat)

            # Publish the head commands
            self.msg.data = min(max(-pitch, -0), 1)
            self.pubPitch.publish(self.msg)

            angle = min(max(yaw, -1.2), 1.2)
            self.msg.data = angle
            self.pubYaw.publish(self.msg)


            GoalPose = Pose()

            qt = transformations.quaternion_from_euler(0, 0, yaw-angle)
            GoalPose.orientation.w = qt[3]
            GoalPose.orientation.x = qt[0]
            GoalPose.orientation.y = qt[1]
            GoalPose.orientation.z = qt[2]

            self.setGoal(GoalPose)
            return "done"

    def on_exit(self, userdata):
        if not self._client.has_result(self._action_topic):
            self._client.cancel(self._action_topic)
            Logger.loginfo('Cancelled active action goal.')


    def setGoal(self, pose):

        goal = MoveBaseGoal()
        goal.target_pose.pose = pose
        goal.target_pose.header.frame_id = "base_link"

        # Send the action goal for execution
        try:
            Logger.loginfo("sending goal" + str(goal))
            self._client.send_goal(self._action_topic, goal)
        except Exception as e:
            Logger.logwarn("Unable to send navigation action goal:\n%s" % str(e))
            self._failed = True
