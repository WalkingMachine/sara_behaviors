#!/usr/bin/env python
from flexbe_core import EventState, Logger
import os


class ObjectDetection_CreatePDF(EventState):
    '''
    Detect if door is open
    REF : https://github.com/WalkingMachine/wm_door_detector

    -- timeout  Max wait for a door detection (in sec)

    <= done     Finish job.
    <= failed   Job as failed.
    '''

    def __init__(self, timeout):
        # See example_state.py for basic explanations.
        super(ObjectDetection_CreatePDF, self).__init__(outcomes=['done', 'failed'],
                                                        input_keys=['try_n'])

    def execute(self, userdata):
        try:
            os.system('python ~/PDF_StoringGroceries/pdfMaker.py '+str(userdata.try_n))
            return 'done'
        except os.error:
            return 'failed'
