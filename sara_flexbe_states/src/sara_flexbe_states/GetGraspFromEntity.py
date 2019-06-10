#!/usr/bin/env python

import math
from flexbe_core import EventState, Logger
import rospy
import copy
from std_msgs.msg import UInt8

from sensor_msgs.msg import PointCloud2, PointCloud
from sensor_msgs import point_cloud2
import numpy as np
from scipy.linalg import lstsq
from gpd.msg import CloudIndexed
from std_msgs.msg import Header, Int64
from geometry_msgs.msg import Point, Pose, PoseStamped, Point32
from sara_msgs.msg import Entity, Entities
from tf import TransformListener
from gpd.msg import GraspConfigList
from tf.transformations import quaternion_from_euler, euler_from_quaternion


from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray


class GetGraspFromEntity(EventState):
    '''
    State taking an entity and returning the best grasp based on the pointcloud entity
    @author Jeffrey Cousineau
    @license Apache2.0

    ># Entity         object    entity to grasp
    #> GraspingPose   object    pose to grasp the given entity
    -- ApproachDistance	float	distance from object at which the gripper shall approach
    -- DistanceScoringMultiplier	float	how much a meter distance affects the score (Higher = closer poses)
    -- OrientationScoringMultiplier	float	how much radians difference from ideal pose affects the score (Higher = more correctly orientated poses)
    -- GraspScoringMultiplier	float	how much scores from gpd affects the final score (Higher = more weight in final score from gpd)
    
    <= done                     grasp was found and returned
    <= failed                   grasp was not found
    '''

    def graspCallback(self, msg):
        self.graspList = msg.grasps

    def __init__(self, approachDistance, distanceScoringMultiplier, orientationScoringMultiplier,
                 graspScoringMultiplier):
        super(GetGraspFromEntity, self).__init__(outcomes=['done', 'failed'], input_keys=['Entity'],
                                                 output_keys=['ApproachPose', 'GraspingPose'])
        self.approachDistance = approachDistance
        self.distanceScoringMultiplier = distanceScoringMultiplier
        self.orientationScoringMultiplier = orientationScoringMultiplier
        self.graspScoringMultiplier = graspScoringMultiplier
        self.graspList = None
        self.grasps_sub = rospy.Subscriber('/detect_grasps/clustered_grasps', GraspConfigList, self.graspCallback)

        self.listener = TransformListener(20)
        self.idealRoll = 0.0
        self.idealPitch = 0.0
        self.idealYaw = 0.07  # 4 degrees to the right relatively to the robot POV
        self.maxgraspScore = 0.0

        self.pub = rospy.Publisher('cloud_indexed', CloudIndexed, queue_size=1)
        self.marker_pub = rospy.Publisher('grasp_pose', PoseStamped, queue_size=1)
        self.marker_pub_app = rospy.Publisher('approach_pose', PoseStamped, queue_size=1)

    def execute(self, userdata):

        if userdata.Entity.pointcloud.header.frame_id == "":
            return "failed"


        Logger.loginfo("Selected entity : " + str(userdata.Entity.ID))
        Logger.loginfo(
            "Current position : (" + str(userdata.Entity.position.x) + ", " + str(userdata.Entity.position.y) + ", " + str(
                userdata.Entity.position.x) + ")")

        # Convert to Pointcloud and change frame of reference to base)link
        pointCloud = PointCloud()
        pointCloud.header = userdata.Entity.pointcloud.header
        for p in point_cloud2.read_points(userdata.Entity.pointcloud):
            point = Point32()
            point.x, point.y, point.z = [p[0], p[1], p[2]]
            pointCloud.points.append(point)
        pointCloud.header.stamp = rospy.Time.now()-rospy.Duration(1)
        self.listener.waitForTransform(pointCloud.header.frame_id, "/base_link", rospy.Time(0), rospy.Duration(10))
        pointCloud = self.listener.transformPointCloud("/base_link", pointCloud)

        cloud = []
        for p in pointCloud.points:
            cloud.append([p.x, p.y, p.z])

        Logger.loginfo("Cloud size : " + str(len(cloud)))

        # if len(cloud) > 0:
        cloud = np.asarray(cloud)
        X = cloud
        A = np.c_[X[:, 0], X[:, 1], np.ones(X.shape[0])]
        C, _, _, _ = lstsq(A, X[:, 2])
        a, b, c, d = C[0], C[1], -1., C[2]  # coefficients of the form: a*x + b*y + c*z + d = 0.
        dist = ((a * X[:, 0] + b * X[:, 1] + d) - X[:, 2]) ** 2
        err = dist.sum()
        idx = np.where(dist > 0.01)


        msg = CloudIndexed()
        header = Header()
        header.frame_id = "/base_link"
        header.stamp = rospy.Time.now()
        msg.cloud_sources.cloud = point_cloud2.create_cloud_xyz32(header, cloud.tolist())
        msg.cloud_sources.view_points.append(Point(0, 0, 1.5))
        for i in xrange(cloud.shape[0]):
            msg.cloud_sources.camera_source.append(Int64(0))
        for i in idx[0]:
            msg.indices.append(Int64(i))
            # s = raw_input('Hit [ENTER] to publish')
        self.pub.publish(msg)

        i = 0

        ################################
        # Temporary setting a timeout
        while self.graspList == None:
            i = i + 1
            rospy.sleep(1)
            if i > 20:
                return 'failed'

        bestScore = 0
        bestGrasp = None
        # Normalisation des scores de grasp
        for grasp in self.graspList:
            if grasp.score.data > self.maxgraspScore:
                self.maxgraspScore = grasp.score.data

        for grasp in self.graspList:

            # Poses with a negative approach gets a negative multiplier
            if grasp.approach.z < 0:  # Approche par le haut
                # poseScore = self.calculateGraspScore(pose)
                poseScore = grasp.score.data
                rospy.loginfo("Total pose score (Positive approach): %s", str(poseScore))

                if bestScore < poseScore:
                    bestScore = poseScore
                    bestGrasp = grasp

        if bestGrasp is not None:
            Logger.loginfo("TEST GRASP")

            # Get pose
            pose = self.graspToPose(bestGrasp)
            userdata.GraspingPose = pose

            # Generate approach pose
            approach_pose = Pose()
            applength = np.linalg.norm([bestGrasp.approach.x, bestGrasp.approach.y, bestGrasp.approach.z])
            approach_pose.position.x = pose.position.x - bestGrasp.approach.x / applength * self.approachDistance
            approach_pose.position.y = pose.position.y - bestGrasp.approach.y / applength * self.approachDistance
            approach_pose.position.z = pose.position.z - bestGrasp.approach.z / applength * self.approachDistance
            approach_pose.orientation = pose.orientation
            userdata.ApproachPose = approach_pose

            # Creates markers for the chosen pose
            stamped = PoseStamped()
            stamped.header.frame_id = "base_link"
            stamped.header.stamp = rospy.Time.now()
            stamped.pose = pose
            self.marker_pub.publish(stamped)
            stamped.pose = approach_pose
            self.marker_pub_app.publish(stamped)
            return 'done'

        # marker_publisher.publish(markerArray)
        return 'failed'  # If all scores are higher than the default value

    def graspToPose(self, grasp):
        pose = Pose()
        pose.position = grasp.top

        yaw = math.atan2(grasp.approach.y, grasp.approach.x)
        distXY = (grasp.approach.x**2 + grasp.approach.y**2)**0.5
        pitch = -math.atan2(grasp.approach.z, distXY)

        approach = np.array([grasp.approach.x, grasp.approach.y, grasp.approach.z])
        approach /= (approach ** 2).sum() ** 0.5  # Get the unit vector
        binormal = np.array([grasp.binormal.x, grasp.binormal.y, grasp.binormal.z])
        binormal /= (binormal ** 2).sum() ** 0.5  # Get the unit vector

        binormal_ref_x = np.cross(np.array([0, 0, 1]), approach)
        binormal_ref_y = np.cross(binormal_ref_x, approach)
        roll = math.atan2(np.vdot(approach, binormal_ref_y), np.vdot(approach, binormal_ref_x)) * math.pi / 2

        # Transformation to quaternion for a Pose
        quat = quaternion_from_euler(roll, pitch, yaw, axes='sxyz')
        pose.orientation.x = quat[0]
        pose.orientation.y = quat[1]
        pose.orientation.z = quat[2]
        pose.orientation.w = quat[3]

        return pose