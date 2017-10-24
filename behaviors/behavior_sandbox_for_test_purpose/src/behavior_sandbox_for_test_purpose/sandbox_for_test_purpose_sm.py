#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_sandbox_for_test_purpose')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.get_box_center import GetBoxCenter
from sara_flexbe_states.gen_gripper_pose import GenGripperPose
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu Sep 21 2017
@author: Philippe La Madeleine
'''
class Sandbox_for_test_purposeSM(Behavior):
    '''
    Sandbox for test purpose.
    '''


    def __init__(self):
        super(Sandbox_for_test_purposeSM, self).__init__()
        self.name = 'Sandbox_for_test_purpose'

        # parameters of this behavior

        # references to used behaviors

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
        
        # [/MANUAL_INIT]

        # Behavior comments:



    def create(self):
        # x:605 y:111, x:130 y:325
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


        with _state_machine:
            # x:87 y:90
            OperatableStateMachine.add('box',
                                        GetBoxCenter(name="cup"),
                                        transitions={'done': 'ee', 'not_found': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'not_found': Autonomy.Off},
                                        remapping={'point': 'point'})

            # x:340 y:95
            OperatableStateMachine.add('ee',
                                        GenGripperPose(x=02, y=0, z=0),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'pose_in': 'point', 'pose_out': 'pose_out'})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
