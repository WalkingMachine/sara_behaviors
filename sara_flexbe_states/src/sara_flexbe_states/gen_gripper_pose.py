#!/usr/bin/env python
# encoding=utf8

from flexbe_core import EventState, Logger
from moveit_commander import MoveGroupCommander
from tf.transformations import quaternion_from_euler
from geometry_msgs.msg import Pose, Point, Quaternion, PointStamped
import math
import rospy
import tf

class GenGripperPose(EventState):
    '''
    Apply a transformation to a pose to get a gripper friendly pose
    -- l    float      radial offset in meters
    -- z    float       z offset in meters
    -- planar   bool    Whether to use a planar approach or not (l will also be along the plane if true)

    #> pose_in     Pose/point     input pose in the map frame
    <= pose_out    Pose     output pose in the base_link frame

    <= done                            success
    <= fail                            failure
    '''

    def __init__(self, l, z, planar):
        super(GenGripperPose, self).__init__(outcomes=['done', 'fail'], input_keys=['pose_in'], output_keys=['pose_out'])

        self.l = l
        self.zo = z
        self.planar = planar
        self.group = MoveGroupCommander("RightArm")
        self.listener = tf.TransformListener()

    def execute(self, userdata):
        # verifie si on recoit une pose ou un point
        out = Pose()
        if type(userdata.pose_in) is Pose:
            out.position.x = userdata.pose_in.position.x
            out.position.y = userdata.pose_in.position.y
            out.position.z = userdata.pose_in.position.z
        elif type(userdata.pose_in) is Point:
            out.position.x = userdata.pose_in.x
            out.position.y = userdata.pose_in.y
            out.position.z = userdata.pose_in.z
        else:
            Logger.loginfo('ERROR in ' + str(self.name) + ' : pose_in is not a Pose() nor a Point()')
            return 'fail'

        out.position.z += self.zo

        # Transform the point into the baselink frame
        point = PointStamped()
        point.header.frame_id = "map"
        point.point = out.position
        self.listener.waitForTransform("map", "base_link", rospy.Time(0), rospy.Duration(1))
        print("Frame : map")
        print(" point : " + str(point.point))
        point = self.listener.transformPoint("base_link", point)
        out.position = point.point

        gripperPose = self.group.get_current_pose().pose

        # calcul des angles
        yaw = math.atan2((out.position.y - gripperPose.position.y), (out.position.x - gripperPose.position.x))
        dist = ((out.position.y - gripperPose.position.y) ** 2 + (out.position.x - gripperPose.position.x) ** 2) ** 0.5
        if self.planar:
            pitch = 0
        else:
            pitch = -math.atan2((out.position.z - gripperPose.position.z), dist)

        # calcul du quaternion
        quat = quaternion_from_euler(0, pitch, yaw)
        self.quat = Quaternion()
        self.quat.x = quat[0]
        self.quat.y = quat[1]
        self.quat.z = quat[2]
        self.quat.w = quat[3]

        #calcul du vecteur dapproche avec les points
        vector = Point()
        vector.x = (gripperPose.position.x - out.position.x)
        vector.y = (gripperPose.position.y - out.position.y)
        if not self.planar:
            vector.z = (gripperPose.position.z - out.position.z)

        # calcul de la norme du vecteur
        norm = (vector.x ** 2 + vector.y ** 2 + vector.z ** 2) ** 0.5
        vector.x *= self.l / norm
        vector.y *= self.l / norm
        vector.z *= self.l / norm

        #applique le vecteur dapproche
        out.position.x += vector.x
        out.position.y += vector.y
        out.position.z += vector.z
        
        out.orientation = self.quat

        userdata.pose_out = out
        return 'done'
