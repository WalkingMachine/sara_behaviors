#!/usr/bin/env python
# -*- coding: utf-8 -*- 
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.decision_state import DecisionState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
@author: Raphaël Duchaîne
'''
class simpleSM(Behavior):
    '''
    Behavior to test dsl parsing to flexbe
    '''


    def __init__(self):
        super(simpleSM, self).__init__()
        self.name = 'simple'

        # parameters of this behavior

        # references to used behaviors

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
    
        # [/MANUAL_INIT]

        # Behavior comments:



    def create(self):
        # x:1200 y:570, x:12 y:570
        _state_machine = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['input_value'])
        _state_machine.userdata.input_value = ''

        # x:130 y:465, x:230 y:465
        _sm_group_01 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['input_value'])

        with _sm_group_01:
            # x:98 y:96
            OperatableStateMachine.add('01',
                                    DecisionState(outcomes=['done','failed'], conditions=lambda x:'done'),
                                    transitions={'done': 'done', 'failed': 'failed'},
                                    autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                    remapping={'input_value': 'input_value'})

        # x:130 y:465, x:230 y:465
        _sm_group_02 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['input_value'])

        with _sm_group_02:
            # x:98 y:96
            OperatableStateMachine.add('02',
                                    DecisionState(outcomes=['done','failed'], conditions=lambda x:'done'),
                                    transitions={'done': 'done', 'failed': 'failed'},
                                    autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                    remapping={'input_value': 'input_value'})

        with _state_machine:

            # x:181 y:94
            OperatableStateMachine.add('group',
                                    _sm_group_01,
                                    transitions={'done': 'group1', 'failed': 'failed'},
                                    autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                    remapping={'input_value': 'input_value'})

            # x:181 y:154
            OperatableStateMachine.add('group1',
                                    _sm_group_02,
                                    transitions={'done': 'done', 'failed': 'failed'},
                                    autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                    remapping={'input_value': 'input_value'})

        return _state_machine


