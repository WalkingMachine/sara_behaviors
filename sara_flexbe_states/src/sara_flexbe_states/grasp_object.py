#!/usr/bin/env python
import actionlib
import rospy
from sensor_msgs.msg import Image
import os
from object_recognition_msgs.msg import ObjectRecognitionAction, ObjectRecognitionGoal
from flexbe_core import EventState, Logger
from agile_grasp.msg import Grasps


class GraspObject(EventState):
    '''
    GraspObject finds requested object and returns its position in the space

    ># workspace     float64[]        3D boundings of the workspace where grasps are computed
    #> grasps        grasps[]         Grasps computed around the requested object
    <= done     Finish job.
    <= failed   Job as failed.
    '''


    def __init__(self):
        # See example_state.py for basic explanations.
        super(GraspObject, self).__init__(outcomes=['done', 'failed'],
                                          input_keys=['workspace'],
                                          output_keys=['grasps'])

    def execute(self, userdata):
        # This method is called periodically while the state is active.
        # Main purpose is to check state conditions and trigger a corresponding outcome.
        # If no outcome is returned, the state will stay active.
        Logger.loginfo('Waiting for AGILE grasper')


        # Run agile grasper and get message
        Logger.loginfo('Computing grasps on workspace '+userdata.workspace)
        os.system('roslaunch agile_grasp single_camera_grasps.launch workspace:='+'\''+userdata.workspace+'\'')

        grasps_msg = rospy.wait_for_message("/find_grasps/grasps", Grasps,
                                           5)  # for kinect2 : '/kinect2/qhd/image_color_rect' for xtion : '/camera/rgb/image_rect_color'
        try:
            print grasps_msg
            userdata.grasps = grasps_msg
            Logger.loginfo("Grasps received")
            return 'done'  # One of the outcomes declared above.
        except rospy.ROSException, e:
            Logger.loginfo("Time out")
            return 'failed'

