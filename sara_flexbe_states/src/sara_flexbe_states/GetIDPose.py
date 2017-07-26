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


class GetIDPose(EventState):
    '''
    GraspObject finds requested object and returns its position in the space

    ># workspace     float64[]        3D boundings of the workspace where grasps are computed
    #> grasps        grasps[]         Grasps computed around the requested object
    <= done     Finish job.
    <= failed   Job as failed.
    '''


    def __init__(self):
        # See example_state.py for basic explanations.
        super(GetIDPose, self).__init__(outcomes=['done', 'lost', 'failed'],
                                          input_keys=['person_id', 'last_pose'],
                                        output_keys=['person_pose'])

    def execute(self, userdata):
        # This method is called periodically while the state is active.
        # Main purpose is to check state conditions and trigger a corresponding outcome.
        # If no outcome is returned, the state will stay active.
        closest_pose = PoseWithCovariance()
        Logger.loginfo('Getting person\'s pose from its ID')
        tracked_persons = rospy.wait_for_message('/spencer/perception/tracked_persons', TrackedPersons, 30)

        try:
            Logger.loginfo('Got list of tracked persons')
            for person in tracked_persons:
                if person.track_id == userdata.person_id and person.is_matched:
                    pose2track = person.track_id
                    Logger.loginfo('Pose of ID to track retrieved')
                    userdata.person_pose = pose2track
                    return 'done'
                elif person.track_id == userdata.person_id:
                    pose2track = person.track_id
                    userdata.person_pose = pose2track
                    Logger.loginfo("Did not find any person close to robot, estimating possible pose")
                    return 'lost'
                else:
                    return 'failed'
            # person2track = tracked_persons[0].track_id

        except rospy.ROSException, e:
            Logger.loginfo("Did not find any person close to robot")
            return 'failed'

