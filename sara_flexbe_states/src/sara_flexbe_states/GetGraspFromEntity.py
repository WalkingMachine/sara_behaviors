#!/usr/bin/env python

import math
from flexbe_core import EventState, Logger
import rospy
import copy
from std_msgs.msg import UInt8

from sensor_msgs.msg import PointCloud2
from sensor_msgs import point_cloud2
import numpy as np
from scipy.linalg import lstsq
from gpd.msg import CloudIndexed
from std_msgs.msg import Header, Int64
from geometry_msgs.msg import Point, Pose
from sara_msgs.msg import Entity, Entities
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

        self.idealRoll = 0.0
        self.idealPitch = 0.0
        self.idealYaw = 0.07  # 4 degrees to the right relatively to the robot POV
        self.maxgraspScore = 0.0

        self.pub = rospy.Publisher('cloud_indexed', CloudIndexed, queue_size=1)


    def on_enter(self, userdata):
        self.entity = userdata.Entity

    def execute(self, userdata):
        Logger.loginfo("Selected entity : " + str(self.entity.ID))
        Logger.loginfo(
            "Current position : (" + str(self.entity.position.x) + ", " + str(self.entity.position.y) + ", " + str(
                self.entity.position.x) + ")")

        cloud = []
        for p in point_cloud2.read_points(self.entity.pointcloud):
            cloud.append([p[0], p[1], p[2]])

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
        msg.cloud_sources.view_points.append(Point(0, 0, 0))
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

        topic = 'visualization_marker_array'
        marker_publisher = rospy.Publisher(topic, MarkerArray)

        markerArray = MarkerArray()
        marker = Marker()
        marker.header.frame_id = "/base_link"
        marker.type = marker.ARROW
        marker.scale.x = 0.02
        marker.scale.y = 0.02
        marker.scale.z = 0.02
        marker.action = marker.ADD
        marker.color.a = 1.0
        marker.color.r = 1.0
        marker.color.g = 1.0
        marker.color.b = 0.0

        score = 99999.0


        stocked_pose = None
        stocked_grasp = 0
        approach_pose = Pose()
        # Normalisation des scores de grasp
        for grasp in self.graspList:
            if grasp.score.data > self.maxgraspScore:
                self.maxgraspScore = grasp.score.data

        for grasp in self.graspList:
            Logger.loginfo("TEST GRASP")
            pose = Pose()
            pose.position = grasp.top
            yaw = math.atan2(grasp.approach.y, grasp.approach.x)
            pitch = -math.atan2(grasp.approach.z, math.sqrt(
                (grasp.approach.x * grasp.approach.x) + (grasp.approach.y * grasp.approach.y)))

            approach = [grasp.approach.x, grasp.approach.y, grasp.approach.z]
            approach /= (approach**2).sum()**0.5  # Get the unit vector
            binormal = [grasp.binormal.x, grasp.binormal.y, grasp.binormal.z]
            binormal /= (binormal**2).sum()**0.5  # Get the unit vector

            binormal_ref_x = np.cross([0, 0, 1], approach)
            binormal_ref_y = np.cross(binormal_ref_x, approach)
            roll = math.atan2(np.vdot(approach, binormal_ref_y), np.vdot(approach, binormal_ref_x))

            #if roll > math.pi / 2:
            #    roll = roll - math.pi
            #roll += math.pi

            # Transformation to quaternion for a Pose
            quat = quaternion_from_euler(roll, pitch, yaw, axes='sxyz')
            pose.orientation.x = quat[0]
            pose.orientation.y = quat[1]
            pose.orientation.z = quat[2]
            pose.orientation.w = quat[3]

            #	    addMarkersToArray(marker,pose,markerArray)

            poseScore = self.calculateGraspScore(pose, grasp)
            # Poses with a negative approach gets a negative multiplier
            if grasp.approach.z > 0:  # Approche par le haut
                rospy.loginfo("Total pose score (Positive approach): %s", str(poseScore))
                if score > poseScore:
                    score = poseScore
                    stocked_pose = pose
                    stocked_grasp = grasp

            else:  # Approche par le bas
                rospy.loginfo("Total pose score (Negative approach): %s", str(poseScore * 10))
                if score > poseScore * 10:
                    score = poseScore * 10
                    stocked_pose = pose
                    stocked_grasp = grasp

        if stocked_pose is not None:
            userdata.GraspingPose = stocked_pose
            approach_pose = self.createApproachPose(stocked_pose, stocked_grasp, self.approachDistance)
            userdata.ApproachPose = approach_pose
            # Creates markers for the chosen pose
            self.addMarkersToArray(marker, stocked_pose, stocked_grasp, markerArray)
            marker3 = copy.deepcopy(marker)
            marker3.id = 3
            marker3.pose = approach_pose
            markerArray.markers.append(marker3)

            marker_publisher.publish(markerArray)
            return 'done'

        # marker_publisher.publish(markerArray)
        return 'failed'  # If all scores are higher than the default value

    def createApproachPose(self, pose, grasp, dist):
        # Creates a pose at distance specified from grasping pose per gpd approach position
        approach_pose = Pose()
        approach_pose.orientation = pose.orientation
        approach_pose.position.x = pose.position.x - dist * grasp.approach.x / np.linalg.norm(
            [grasp.approach.x, grasp.approach.y, grasp.approach.z])
        approach_pose.position.y = pose.position.y - dist * grasp.approach.y / np.linalg.norm(
            [grasp.approach.x, grasp.approach.y, grasp.approach.z])
        approach_pose.position.z = pose.position.z - dist * grasp.approach.z / np.linalg.norm(
            [grasp.approach.x, grasp.approach.y, grasp.approach.z])
        return approach_pose

    def addMarkersToArray(self, marker, pose, grasp, markerArray):
        # Adds markers for identified pose
        marker1 = copy.deepcopy(marker)
        marker1.id = 1
        marker1.pose = pose
        markerArray.markers.append(marker1)
        marker2 = copy.deepcopy(marker)
        marker2.type = marker.SPHERE
        marker2.id = 2
        marker2.pose.position.x = grasp.top.x + grasp.binormal.x / 20
        marker2.pose.position.y = grasp.top.y + grasp.binormal.y / 20
        marker2.pose.position.z = grasp.top.z + grasp.binormal.z / 20
        markerArray.markers.append(marker2)
        return True

    def calculateGraspScore(self, pose, grasp):
        # Calculates a score for a given grasp, a minimum score is prefered
        # Pythagorean distance (except z) multiplied by a scoring multiplier
        score1 = ((pose.position.x) ** 2. + (pose.position.y) ** 2.) ** (0.5) * self.distanceScoringMultiplier
        # Pythagorean angle multiplied by a scoring multiplier
        (roll, pitch, yaw) = euler_from_quaternion(
            [pose.orientation.x, pose.orientation.y, pose.orientation.z, pose.orientation.w])
        score2 = ((self.idealRoll - roll) ** 2. + (self.idealPitch - pitch) ** 2. + (self.idealYaw - yaw) ** 2.) ** (
                0.5) * self.orientationScoringMultiplier
        # Inverse of normalized score minus 1 (so normalized best = 0) multiplied by a scoring multiplier
        score3 = ((self.maxgraspScore / grasp.score.data) - 1) * self.graspScoringMultiplier
        rospy.loginfo("Position score : %.4f, Orientation score : %.4f, Grasping score : %.4f", score1, score2, score3)
        score = score1 + score2 + score3
        return score
