#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_selectobject')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.wait_state import WaitState
from sara_flexbe_states.recognize_objects import ObjectsRecognize
from flexbe_states.subscriber_state import SubscriberState
from sara_flexbe_states.select_object import ObjectSelect
from sara_flexbe_states.ObjectDetection_GetImages import ObjectDetection_GetImages
from sara_flexbe_states.ObjectDetection_CreatePDF import ObjectDetection_CreatePDF

# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sat Jul 08 2017
@author: Samuel Otis
'''
class SelectObjectSM(Behavior):
    '''
    This behavior runs ork for recognition and publishes the pose of a requested object
    '''


    def __init__(self):
        super(SelectObjectSM, self).__init__()
        self.name = 'SelectObject'

        # parameters of this behavior

        # references to used behaviors

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
        
        # [/MANUAL_INIT]

        # Behavior comments:



    def create(self):
        # x:900 y:225, x:472 y:176, x:466 y:406
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'timeout'], input_keys=['Name', 'detection_1', 'try_1'], output_keys=['pose'])
        _state_machine.userdata.Name = "unknown"
        _state_machine.userdata.detection_1 = 1
        _state_machine.userdata.try_1 = 1
        _state_machine.userdata.pose = 0


        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

        # x:476 y:158, x:666 y:50
        _sm_group_0 = OperatableStateMachine(outcomes=['failed', 'done'], input_keys=['Name'], output_keys=['Pose', 'workspace'])

        with _sm_group_0:
            # x:32 y:40
            OperatableStateMachine.add('ObjectRecognize',
                                        ObjectsRecognize(),
                                        transitions={'done': 'GetObjects', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'image': 'Image'})

            # x:259 y:173
            OperatableStateMachine.add('GetObjects',
                                        SubscriberState(topic="/recognized_object_array", blocking=True, clear=False),
                                        transitions={'received': 'SelectObject', 'unavailable': 'GetObjects'},
                                        autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
                                        remapping={'message': 'Objects'})

            # x:452 y:43
            OperatableStateMachine.add('SelectObject',
                                        ObjectSelect(),
                                        transitions={'done': 'done', 'failed': 'failed', 'looping': 'ObjectRecognize'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off, 'looping': Autonomy.Off},
                                        remapping={'objects_array': 'Objects', 'object_name': 'Name', 'image': 'Image', 'pose': 'Pose', 'workspace': 'workspace'})


        # x:25 y:353, x:12 y:448, x:230 y:382, x:7 y:487, x:7 y:528, x:530 y:342
        _sm_group_2_1 = ConcurrencyContainer(outcomes=['done', 'failed', 'timeout'], input_keys=['Name', 'Image'], output_keys=['Pose', 'workspace'], conditions=[
                                        ('timeout', [('Timeout', 'done')]),
                                        ('failed', [('Group', 'failed')]),
                                        ('done', [('Group', 'done')])
                                        ])

        with _sm_group_2_1:
            # x:37 y:169
            OperatableStateMachine.add('Group',
                                        _sm_group_0,
                                        transitions={'failed': 'failed', 'done': 'done'},
                                        autonomy={'failed': Autonomy.Inherit, 'done': Autonomy.Inherit},
                                        remapping={'Name': 'Name', 'Pose': 'Pose', 'workspace': 'workspace'})

            # x:209 y:170
            OperatableStateMachine.add('Timeout',
                                        WaitState(wait_time=30),
                                        transitions={'done': 'timeout'},
                                        autonomy={'done': Autonomy.Off})



        with _state_machine:
            # x:70 y:28
            OperatableStateMachine.add('InitWait',
                                        WaitState(wait_time=0.1),
                                        transitions={'done': 'ObjectRecog'},
                                        autonomy={'done': Autonomy.Off})

            # x:251 y:27
            OperatableStateMachine.add('ObjectRecog',
                                        ObjectsRecognize(),
                                        transitions={'done': 'Group_2', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'image': 'Image'})

            # x:277 y:303
            OperatableStateMachine.add('Group_2',
                                        _sm_group_2_1,
                                        transitions={'done': 'GetImageForPDF', 'failed': 'failed', 'timeout': 'timeout'},
                                        autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'timeout': Autonomy.Inherit},
                                        remapping={'Name': 'Name', 'Image': 'Image', 'Pose': 'Pose', 'workspace': 'workspace'})

            # x:544 y:301
            OperatableStateMachine.add('GetGrasp',
                                        GraspObject(),
                                        transitions={'done': 'finished', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'workspace': 'workspace', 'grasps': 'grasps'})

            # x:542 y:310
            OperatableStateMachine.add('GetImageForPDF',
                                        ObjectDetection_GetImages(timeout=1),
                                        transitions={'done': 'PDFDo', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'detection_n': 'detection_1'})

            # x:696 y:197
            OperatableStateMachine.add('PDFDo',
                                        ObjectDetection_CreatePDF(timeout=1),
                                        transitions={'done': 'finished', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'try_n': 'try_1'})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
