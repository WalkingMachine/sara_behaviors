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
from tf.transformations import quaternion_from_euler

from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray

class GetGraspFromEntity(EventState):
    '''
    State taking an entity and returning the best grasp based on the pointcloud entity
    @author Jeffrey Cousineau
    @license Apache2.0

    ># Entity         object    entity to grasp
    #> GraspingPose   object    pose to grasp the given entity
    
    <= done                     grasp was found and returned
    <= failed                   grasp was not found
    '''

    def graspCallback(self, msg):
        self.graspList = msg.grasps

    def __init__(self):
        super(GetGraspFromEntity, self).__init__(outcomes=['done', 'failed'], input_keys=['Entity'], output_keys=['GraspingPose'])
        #self.emotion=emotion
        self.graspList = None
        self.grasps_sub = rospy.Subscriber('/detect_grasps/clustered_grasps', GraspConfigList, self.graspCallback)

    def on_enter(self, userdata):
        self.entity = userdata.Entity

    def execute(self, userdata):
        Logger.loginfo("Selected entity : " + str(self.entity.ID))
        Logger.loginfo("Current position : (" + str(self.entity.position.x) + ", " + str(self.entity.position.y)+ ", " + str(self.entity.position.x) + ")")
        
        
        cloud = []
        for p in point_cloud2.read_points(self.entity.pointcloud):
            cloud.append([p[0], p[1], p[2]])
        
        Logger.loginfo("Cloud size : " + str(len(cloud)))

        #if len(cloud) > 0:
        cloud = np.asarray(cloud)
        X = cloud
        A = np.c_[X[:,0], X[:,1], np.ones(X.shape[0])]
        C, _, _, _ = lstsq(A, X[:,2])
        a, b, c, d = C[0], C[1], -1., C[2] # coefficients of the form: a*x + b*y + c*z + d = 0.
        dist = ((a*X[:,0] + b*X[:,1] + d) - X[:,2])**2
        err = dist.sum()
        idx = np.where(dist > 0.01)

        pub = rospy.Publisher('cloud_indexed', CloudIndexed, queue_size=1)

        msg = CloudIndexed()
        header = Header()
        header.frame_id = "/base_link"
        header.stamp = rospy.Time.now()
        msg.cloud_sources.cloud = point_cloud2.create_cloud_xyz32(header, cloud.tolist())
        msg.cloud_sources.view_points.append(Point(0,0,0))
        for i in xrange(cloud.shape[0]):
            msg.cloud_sources.camera_source.append(Int64(0))
        for i in idx[0]:
            msg.indices.append(Int64(i))    
        #s = raw_input('Hit [ENTER] to publish')
        pub.publish(msg)
        
        i = 0

        ################################
        # Temporary setting a timeout
        while self.graspList == None:
            i = i+1
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


        stocked_pose = None
        stocked_z = 0
        for grasp in self.graspList:
            Logger.loginfo("TEST GRASP")
            pose = Pose()
            pose.position = grasp.top
            yaw = math.atan2(grasp.approach.y , grasp.approach.x)
            pitch = math.atan2( grasp.approach.z , math.sqrt((grasp.approach.x*grasp.approach.x)+(grasp.approach.y*grasp.approach.y)) )
            binormal = [grasp.binormal.x, grasp.binormal.y, grasp.binormal.z]
            binormal_ref = np.cross( [0,0,1] , [grasp.approach.x, grasp.approach.y, grasp.approach.z] )
            roll = math.acos( np.dot(binormal, binormal_ref) / (np.linalg.norm(binormal)*np.linalg.norm(binormal_ref)) )

            if roll > math.pi/2:
                roll = roll - math.pi

            quat = quaternion_from_euler(roll, pitch, yaw, axes='sxyz')

            pose.orientation.x = quat[0]
            pose.orientation.y = quat[1]
            pose.orientation.z = quat[2]
            pose.orientation.w = quat[3]

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

            ## keep the pose with a negative z approach or the one with the closest z of zero if all positive
            if grasp.approach.z > 0:
                Logger.loginfo("APPROCHE VERS LE HAUT")
                if stocked_pose is not None:
                    if grasp.approach.z > stocked_z:
                        stocked_pose = pose
                        stocked_z = grasp.approach.z
                else:
                    stocked_pose = pose
                    stocked_z = grasp.approach.z
            else:
                Logger.loginfo("APPROCHE VERS LE BAS")
                marker_publisher.publish(markerArray)

                userdata.GraspingPose = pose
                return 'done'

        if stocked_pose is not None:

            marker_publisher.publish(markerArray)

            userdata.GraspingPose = stocked_pose
            return 'done'

        marker_publisher.publish(markerArray)

        return 'failed'

    