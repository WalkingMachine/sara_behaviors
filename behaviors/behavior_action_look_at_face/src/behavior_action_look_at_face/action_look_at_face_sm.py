#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_action_look_at_face')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.Get_Entity_By_ID import GetEntityByID
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.Get_direction_to_point import Get_direction_to_point
from sara_flexbe_states.sara_set_head_angle_key import SaraSetHeadAngleKey
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu Apr 26 2018
@author: Veronica Romero
'''
class action_look_at_faceSM(Behavior):
    '''
    Moves Sara's head towards the face recognized by Yolo
    '''


    def __init__(self):
        super(action_look_at_faceSM, self).__init__()
        self.name = 'action_look_at_face'

        # parameters of this behavior

        # references to used behaviors

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
        
        # [/MANUAL_INIT]

        # Behavior comments:



    def create(self):
        # x:797 y:212, x:89 y:236
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['Position', 'ID'])
        _state_machine.userdata.Position = None
        _state_machine.userdata.ID = 0

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


        with _state_machine:
            # x:30 y:40
            OperatableStateMachine.add('Entity',
                                        GetEntityByID(),
                                        transitions={'found': 'ExtractPos', 'not_found': 'failed'},
                                        autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
                                        remapping={'ID': 'ID', 'Entity': 'Entity'})

            # x:174 y:62
            OperatableStateMachine.add('ExtractPos',
                                        CalculationState(calculation=lambda x: x.position),
                                        transitions={'done': 'direction'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'input_value': 'Entity', 'output_value': 'Position'})

            # x:310 y:118
            OperatableStateMachine.add('direction',
                                        Get_direction_to_point(frame_origin="base_link", frame_reference="head_link"),
                                        transitions={'done': 'InvertPitch', 'fail': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'fail': Autonomy.Off},
                                        remapping={'targetPoint': 'Position', 'yaw': 'yaw', 'pitch': 'pitch'})

            # x:480 y:159
            OperatableStateMachine.add('InvertPitch',
                                        CalculationState(calculation=lambda x: -x),
                                        transitions={'done': 'Head'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'input_value': 'pitch', 'output_value': 'pitch'})

            # x:618 y:201
            OperatableStateMachine.add('Head',
                                        SaraSetHeadAngleKey(),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'yaw': 'yaw', 'pitch': 'pitch'})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
