#!/usr/bin/env python
# encoding=utf8

from flexbe_core import EventState, Logger
from moveit_commander import MoveGroupCommander
from tf.transformations import quaternion_from_euler
from geometry_msgs.msg import Pose, Point, Quaternion
import math

class GenGripperPose(EventState):
    '''
    Apply a transformation to a pose to get a gripper friendly pose
    -- l    float      offset 

    >= pose_in     Pose/point     input pose
    <= pose_out    Pose     output pose
    '''

    def __init__(self, l):
        super(GenGripperPose, self).__init__(outcomes=['done'], input_keys=['pose_in'], output_keys=['pose_out'])

        self.l = l
        self.group = MoveGroupCommander("RightArm")

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
            return 'done'
        gripperPose = self.group.get_current_pose().pose

        # calcul des angles
        yaw = math.atan2((out.position.y - gripperPose.position.y), (out.position.x - gripperPose.position.x))
        dist = ((out.position.y - gripperPose.position.y) ** 2 + (out.position.x - gripperPose.position.x) ** 2) ** 0.5
        pitch = math.atan2((out.position.z - gripperPose.position.z), dist)

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
