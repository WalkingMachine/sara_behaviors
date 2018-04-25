#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_action_look_at')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.Get_direction_to_point import Get_direction_to_point
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.Get_Entity_By_ID import GetEntityByID
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed Apr 25 2018
@author: Veronica
'''
class action_look_atSM(Behavior):
    '''
    Makes sara look at a given point
    '''


    def __init__(self):
        super(action_look_atSM, self).__init__()
        self.name = 'action_look_at'

        # parameters of this behavior

        # references to used behaviors

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
        
        # [/MANUAL_INIT]

        # Behavior comments:



    def create(self):
        # x:647 y:158, x:648 y:65
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['Position', 'ID'])
        _state_machine.userdata.Position = None
        _state_machine.userdata.ID = 0

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


        with _state_machine:
            # x:47 y:53
            OperatableStateMachine.add('entity',
                                        GetEntityByID(),
                                        transitions={'found': 'ExtractPos', 'not_found': 'failed'},
                                        autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
                                        remapping={'ID': 'ID', 'Entity': 'Entity'})

            # x:187 y:84
            OperatableStateMachine.add('ExtractPos',
                                        CalculationState(calculation=lambda x: x.position),
                                        transitions={'done': 'Direction'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'input_value': 'Entity', 'output_value': 'Position'})

            # x:352 y:107
            OperatableStateMachine.add('Direction',
                                        Get_direction_to_point(frame_origin="base_link", frame_reference="head_link"),
                                        transitions={'done': 'finished', 'fail': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'fail': Autonomy.Off},
                                        remapping={'targetPoint': 'Position', 'yaw': 'yaw', 'pitch': 'pitch'})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
