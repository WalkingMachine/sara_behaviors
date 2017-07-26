#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_new_qualif')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.AMCL_initial_pose import AmclInit
from behavior_door_detector.door_detector_sm import DoorDetectorSM
from sara_flexbe_states.pose_gen2 import GenPose2
from sara_flexbe_states.sara_move_base import SaraMoveBase
from sara_flexbe_states.continue_button import ContinueButton
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed Jul 26 2017
@author: Philippe La Madeleine
'''
class NewqualifSM(Behavior):
    '''
    qualification 2017
    '''


    def __init__(self):
        super(NewqualifSM, self).__init__()
        self.name = 'New qualif'

        # parameters of this behavior

        # references to used behaviors
        self.add_behavior(DoorDetectorSM, 'Door Detector')

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
        
        # [/MANUAL_INIT]

        # Behavior comments:



    def create(self):
        # x:733 y:513, x:337 y:267
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


        with _state_machine:
            # x:43 y:79
            OperatableStateMachine.add('init',
                                        AmclInit(x=0.494079113007, y=0.182213068008, z=0, ox=0, oy=0, oz=-0.00849557845025, ow=0.999963911922),
                                        transitions={'done': 'Door Detector', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'pose': 'pose'})

            # x:24 y:168
            OperatableStateMachine.add('Door Detector',
                                        self.use_behavior(DoorDetectorSM, 'Door Detector'),
                                        transitions={'finished': 'gen', 'failed': 'Door Detector'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

            # x:43 y:274
            OperatableStateMachine.add('gen',
                                        GenPose2(x=1.69569063187, y=0.229661718011, z=0, ox=0, oy=0, oz=-0.0101022152482, ow=0.999948971322),
                                        transitions={'done': 'move', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'pose': 'pose'})

            # x:37 y:350
            OperatableStateMachine.add('move',
                                        SaraMoveBase(),
                                        transitions={'arrived': 'continue', 'failed': 'failed'},
                                        autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'pose': 'pose'})

            # x:26 y:435
            OperatableStateMachine.add('continue',
                                        ContinueButton(),
                                        transitions={'Continue': 'gen2'},
                                        autonomy={'Continue': Autonomy.Off})

            # x:35 y:512
            OperatableStateMachine.add('gen2',
                                        GenPose2(x=6.04513931274, y=3.34974265099, z=0, ox=0, oy=0, oz=0.413818975028, ow=0.910359190598),
                                        transitions={'done': 'move2', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'pose': 'pose'})

            # x:215 y:514
            OperatableStateMachine.add('move2',
                                        SaraMoveBase(),
                                        transitions={'arrived': 'gen3', 'failed': 'failed'},
                                        autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'pose': 'pose'})

            # x:388 y:514
            OperatableStateMachine.add('gen3',
                                        GenPose2(x=11.4574050903, y=2.73497796059, z=0, ox=0, oy=0, oz=-0.284027256457, ow=0.958816206366),
                                        transitions={'done': 'move3', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'pose': 'pose'})

            # x:527 y:514
            OperatableStateMachine.add('move3',
                                        SaraMoveBase(),
                                        transitions={'arrived': 'finished', 'failed': 'failed'},
                                        autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'pose': 'pose'})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
