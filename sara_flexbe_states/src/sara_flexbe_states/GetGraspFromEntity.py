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


        for grasp in self.graspList:
            pose = Pose()
            pose.Point = grasp.top
            yaw = atan2(grasp.approach.y , grasp.approach.x)
            pitch = atan2( grasp.approach.z , sqrt((grasp.approach.x*grasp.approach.x)+(grasp.approach.y*grasp.approach.y)) )
            roll = 0


        return 'done'
        #return 'failed'

    