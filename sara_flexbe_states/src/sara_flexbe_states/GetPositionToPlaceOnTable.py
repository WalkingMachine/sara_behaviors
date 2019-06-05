#!/usr/bin/env python
import string
import math
from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxySubscriberCached
from geometry_msgs.msg import Point, Pose
from sensor_msgs.msg import PointCloud2
from sensor_msgs import point_cloud2

'''
Created on 03.06.2019
@author: Quentin Gaillot
'''

class GetPositionToPlaceOnTable(EventState):
    """
    Renvoie la position d'un endroit sur la table pour poser un objet.

    ### InputKey
    ># angle        msg.ranges

    ### OutputKey
    <= done         Angle de l'obstacle
    """

    def __init__(self):
        '''
        Constructor
        '''
        super(GetPositionToPlaceOnTable, self).__init__(outcomes=['done', 'not_found'], input_keys=['distanceFromEdge'], output_keys=['position'])

        self.planeTopic = "/segment_table/plane"
        self.planeSub = ProxySubscriberCached({self.planeTopic: PointCloud2})

        self.robotposeTopic = "/robot_pose"
        self.robotposeSub = ProxySubscriberCached({self.robotposeTopic: Pose})

        self.plane = None

    def dist(self, point1, point2):
        x = point1.x - point2.x
        y = point1.y - point2.y
        return math.sqrt(x*x+y*y)

    def execute(self, userdata):
        '''
        Execute this state
        '''

        # Get the latest robot pose
        mypose = self.robotposeSub.get_last_msg(self.robotposeTopic)

        if self.planeSub.has_msg(self.planeTopic):
            Logger.loginfo('getting table point cloud')
            self.plane = self.planeSub.get_last_msg(self.planeTopic)
            self.planeSub.remove_last_msg(self.planeTopic)

        if self.plane is not None and mypose is not None:

            gen = point_cloud2.read_points(self.plane)

            closest_point = Point()
            closest_point.x = 0
            closest_point.y = 0
            closest_point.z = 0
            min_dist = 99999
            numberOfPoints = 0

            sum_x = 0
            sum_y = 0
            sum_z = 0

            # find the closest point and center
            point = Point()

            for p in gen:
                numberOfPoints = numberOfPoints + 1

                point.x = p[0]
                point.y = p[1]
                point.z = p[2]

                sum_x += point.x
                sum_y += point.y
                sum_z += point.z

                if self.dist(mypose.position, point) < min_dist:
                    min_dist = self.dist(mypose.position, point)
                    closest_point = point

            center = Point()
            center.x = sum_x / numberOfPoints
            center.y = sum_y / numberOfPoints
            center.z = sum_z / numberOfPoints

            #find point to return
            distanceClosestPointCenter = self.dist(closest_point, center)
            if distanceClosestPointCenter < userdata.distanceFromEdge:
                userdata.position = center
                return "done"
            else:
                rapportProportionnel = userdata.distanceFromEdge/distanceClosestPointCenter
                pointToReturn = Point()
                pointToReturn.x = closest_point.x + (center.x - closest_point.x) * rapportProportionnel
                pointToReturn.y = closest_point.y + (center.y - closest_point.y) * rapportProportionnel
                pointToReturn.z = closest_point.z + (center.z - closest_point.z) * rapportProportionnel
                userdata.position = pointToReturn

                return "done"

        else:
            if self.plane is None:
                Logger.loginfo('plane is none')
            if mypose is  None:
                Logger.loginfo('pose is none')