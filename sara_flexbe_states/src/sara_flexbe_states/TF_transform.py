#!/usr/bin/env python

import rospy
import tf


class TF_transformation:
    """
    Transformation from a reference  to another

    --in_ref    frame_id     first reference
    --out_ref   frame_id     second reference

    ># in_pos   Point        point in in_pos

    <= done                  Did all the transformation
    <= fail                  Failed to transform

    """

    def __init__(self,in_ref,out_ref):
        '''
        Constructor
        '''
        super(TF_transformation,self).__init__(outcomes=['done','fail'], input_keys=['in_pos'], output_keys=['out_pos'])
        self.listener = tf.TransformListener()
        self.in_ref=in_ref
        self.out_ref=out_ref

    def execute(self, userdata):
        point = geometry_msgs.msg.PointStamped()
        point.header.frame_id = self.in_ref
        point.point = userdata.in_pos
        self.listener.waitForTransform("map", self.out_ref, rospy.Time(0), rospy.Duration(1))
        print("Frame : map")
        print(" point : "+str(point.point))
        try:
            point = self.listener.transformPoint(self.out_ref, point)
            userdata.out_pos = point.point
            return 'done'
        except:
            return 'fail'
