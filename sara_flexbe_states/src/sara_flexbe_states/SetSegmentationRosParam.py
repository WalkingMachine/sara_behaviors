# !/usr/bin/env python

import rospy
from flexbe_core import EventState, Logger

'''
Created on 21.04.2019
@author: Quentin Gaillot
'''


class SetSegmentationRosParam(EventState):
    '''
    Set the Rosparams /process_table_segmentation and /process_object_segmentation to true or false to activate/desactivate the table/object segmentation.
    ># ValueTableSegmentation      object      The rosparam to set for table segmentation.
    ># ValueObjectSegmentation      object      The rosparam to set for object segmentation.

    <= done                 The rosparams are set
    '''

    def __init__(self, ValueTableSegmentation, ValueObjectSegmentation):
        '''
        Constructor
        '''
        super(SetSegmentationRosParam, self).__init__(outcomes=['done'])
        self.ValueTable = ValueTableSegmentation
        self.ValueObject = ValueObjectSegmentation

    def execute(self, userdata):
        '''
        Execute this state
        '''
        if self.ValueTable:
            rospy.set_param("/process_table_segmentation", self.ValueTable)
        else:
            if rospy.has_param("/process_table_segmentation"):
                rospy.delete_param("/process_table_segmentation")

        if self.ValueObject:
            rospy.set_param("/process_object_segmentation", self.ValueObject)
        else:
            if rospy.has_param("/process_object_segmentation"):
                rospy.delete_param("/process_object_segmentation")

        return "done"
