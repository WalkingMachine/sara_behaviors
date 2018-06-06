#!/usr/bin/env python

from flexbe_core import EventState, Logger
import rospy
import tf
from geometry_msgs.msg import PointStamped, Point, Pose

class TF_transformation(EventState):
    """
    Transformation from a referential  to another

    ###Params
    -- in_ref   String      first referential
    -- out_ref  String      second referential

    ### InputKey
    ># in_pos   geometry_msgs/Point       point in first referential

    ### OutputKey
    #> out_pos  geometry_msgs/Point       point in second referential

    ###Outcomes
    <= done                 Did all the transformation
    <= fail                 Failed to transform

    """

    def __init__(self, in_ref, out_ref):
        '''Constructor'''
        super(TF_transformation,self).__init__(outcomes=['done','fail'], input_keys=['in_pos'], output_keys=['out_pos'])
        self.listener = tf.TransformListener()
        self.in_ref=in_ref
        self.out_ref=out_ref

    def execute(self, userdata):

        point = PointStamped()
        if type(userdata.in_pos) is Point:
            print("this is a point")
            point.point = userdata.in_pos
        elif type(userdata.in_pos) is Pose:
            print("this is a pose")
            point.point = userdata.in_pos.position
        else:
            Logger.loginfo('ERROR in ' + str(self.name) + ' : in_pos is not a Pose() nor a Point()')
            return 'fail'

        point.header.frame_id = self.in_ref
        self.listener.waitForTransform("map", self.out_ref, rospy.Time(0), rospy.Duration(1))
        print("Frame : map")
        print(" point : "+str(point.point))

        point = self.listener.transformPoint(self.out_ref, point)
        userdata.out_pos = point.point
        return 'done'
