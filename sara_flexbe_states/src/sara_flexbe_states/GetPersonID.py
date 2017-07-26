#!/usr/bin/env python
import actionlib
import rospy
import math
from sensor_msgs.msg import Image
from geometry_msgs.msg import PoseWithCovariance, Pose
import os
from object_recognition_msgs.msg import ObjectRecognitionAction, ObjectRecognitionGoal
from flexbe_core import EventState, Logger
from agile_grasp.msg import Grasps
from spencer_tracking_msgs.msg import *


class GetPersonID(EventState):
    '''
    GraspObject finds requested object and returns its position in the space

    ># workspace     float64[]        3D boundings of the workspace where grasps are computed
    #> grasps        grasps[]         Grasps computed around the requested object
    <= done     Finish job.
    <= failed   Job as failed.
    '''


    def __init__(self):
        # See example_state.py for basic explanations.
        super(GetPersonID, self).__init__(outcomes=['done', 'failed'],
                                          output_keys=['person_id'])

    def execute(self, userdata):
        # This method is called periodically while the state is active.
        # Main purpose is to check state conditions and trigger a corresponding outcome.
        # If no outcome is returned, the state will stay active.
        closest_pose = PoseWithCovariance()
        Logger.loginfo('Starting SPENCER people tracker')
        os.system('roslaunch spencer_people_tracking_launch tracking_single_rgbd_sensor.launch height_above_ground:=1.6')
        tracked_persons = rospy.wait_for_message('/spencer/perception/tracked_persons', TrackedPersons, 30)

        try:
            Logger.loginfo('Got list of tracked persons')
            for person in tracked_persons:
                x_pos = person.pose.pose.position.x
                y_pos = person.pose.pose.position.y
                distance = math.sqrt(x_pos^2 + y_pos^2)
                if distance <= 2.0:
                    person2track = person.track_id
                    Logger.loginfo("Closest person to track retrieved")
                    userdata.person_id = person2track
                    return 'done'
                else:
                    Logger.loginfo("Did not find any person close to robot")
                    return 'failed'
            # person2track = tracked_persons[0].track_id

        except rospy.ROSException, e:
            Logger.loginfo("Did not find any person close to robot")
            return 'failed'

