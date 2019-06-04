#!/usr/bin/env python

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
from geometry_msgs.msg import Point
from sara_msgs.msg import Entity, Entities
from gpd.msg import GraspConfigList

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
        self.grasp = msg.grasps[0]

    def __init__(self):
        super(GetGraspFromEntity, self).__init__(outcomes=['done', 'failed'], input_keys=['Entity'], output_keys=['GraspingPose'])
        #self.emotion=emotion
        self.grasp = None
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
        while self.grasp == None:
            i = i+1
            rospy.sleep(1)
            if i > 20:
                return 'failed'

        userdata.GraspingPose = self.grasp
        Logger.loginfo(self.grasp)


        topic = 'visualization_marker_array'
        marker_publisher = rospy.Publisher(topic, MarkerArray)

        markerArray = MarkerArray()
        marker = Marker()
        marker.header.frame_id = "/base_link"
        marker.type = marker.SPHERE
        marker.scale.x = 0.02
        marker.scale.y = 0.02
        marker.scale.z = 0.02
        marker.action = marker.ADD
        marker.color.a = 1.0
        marker.color.r = 1.0
        marker.color.g = 1.0
        marker.color.b = 0.0
        marker.pose.orientation.w = 1.0

        marker1 = copy.deepcopy(marker)
        marker1.id = 1
        marker1.pose.position.x = self.grasp.bottom.x
        marker1.pose.position.y = self.grasp.bottom.y
        marker1.pose.position.z = self.grasp.bottom.z
 
        marker2 = copy.deepcopy(marker)
        marker2.id = 2
        marker2.pose.position.x = self.grasp.top.x
        marker2.pose.position.y = self.grasp.top.y
        marker2.pose.position.z = self.grasp.top.z

        marker3 = copy.deepcopy(marker)
        marker3.id = 3
        marker3.pose.position.x = self.grasp.surface.x
        marker3.pose.position.y = self.grasp.surface.y
        marker3.pose.position.z = self.grasp.surface.z

        marker4 = copy.deepcopy(marker)
        marker4.id = 4
        marker4.pose.position.x = self.grasp.surface.x
        marker4.pose.position.y = self.grasp.surface.y
        marker4.pose.position.z = self.grasp.surface.z

        marker5 = copy.deepcopy(marker)
        marker5.id = 5
        marker5.pose.position.x = self.grasp.approach.x
        marker5.pose.position.y = self.grasp.approach.y
        marker5.pose.position.z = self.grasp.approach.z

        marker6 = copy.deepcopy(marker)
        marker6.id = 6
        marker6.pose.position.x = self.grasp.binormal.x
        marker6.pose.position.y = self.grasp.binormal.y
        marker6.pose.position.z = self.grasp.binormal.z

        marker7 = copy.deepcopy(marker)
        marker7.id = 7
        marker7.pose.position.x = self.grasp.axis.x
        marker7.pose.position.y = self.grasp.axis.y
        marker7.pose.position.z = self.grasp.axis.z

        marker8 = copy.deepcopy(marker)
        marker8.id = 8
        marker8.pose.position.x = self.grasp.sample.x
        marker8.pose.position.y = self.grasp.sample.y
        marker8.pose.position.z = self.grasp.sample.z

        markerArray.markers.append(marker1)
        markerArray.markers.append(marker2)
        markerArray.markers.append(marker3)
        markerArray.markers.append(marker4)
        markerArray.markers.append(marker5)
        markerArray.markers.append(marker6)
        markerArray.markers.append(marker7)
        markerArray.markers.append(marker8)



        marker_publisher.publish(markerArray)

        return 'done'
        #return 'failed'

    