#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_actionmovearm')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.move_arm import MoveArm
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu Jul 06 2017
@author: Philippe La Madleine
'''
class ActionMoveArmSM(Behavior):
    '''
    Send a pose to moveit to move the arm.
    '''


    def __init__(self):
        super(ActionMoveArmSM, self).__init__()
        self.name = 'ActionMoveArm'

        # parameters of this behavior

        # references to used behaviors

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
        
        # [/MANUAL_INIT]

        # Behavior comments:



    def create(self):
        # x:495 y:154, x:506 y:225
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['ActionForm'])
        _state_machine.userdata.ActionForm = ["MoveArm",1]

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


        with _state_machine:
            # x:74 y:108
            OperatableStateMachine.add('get pose',
                                        CalculationState(calculation=lambda x: x[1]),
                                        transitions={'done': 'move the arm'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'input_value': 'ActionForm', 'output_value': 'pose'})

            # x:228 y:165
            OperatableStateMachine.add('move the arm',
                                        MoveArm(),
                                        transitions={'done': 'finished', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'pose': 'pose'})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
