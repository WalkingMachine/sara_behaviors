#!/usr/bin/env python
from flexbe_core import EventState, Logger
import os


class ObjectDetection_GetImages(EventState):
    '''
    Detect if door is open
    REF : https://github.com/WalkingMachine/wm_door_detector

    -- timeout  Max wait for a door detection (in sec)

    <= done     Finish job.
    <= failed   Job as failed.
    '''

    def __init__(self, timeout):
        # See example_state.py for basic explanations.
        super(ObjectDetection_GetImages, self).__init__(outcomes=['done', 'failed'],
                                                        input_keys=['detection_n'])

    def execute(self, userdata):
        if userdata.detection_n == 1:
            os.system('mkdir ~/detection')
        os.system('mkdir ~/detection_' + str(userdata.detection_n))
        try:
            os.system('cp ~/roi_images_objects/* ~/detection_' + str(userdata.detection_n))
            return 'done'
        except os.error:
            return 'failed'
