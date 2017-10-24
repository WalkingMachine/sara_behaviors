#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_actionwrapper_pick')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.check_condition_state import CheckConditionState
from sara_flexbe_states.sara_say_key import SaraSayKey
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Tue Jul 11 2017
@author: Philippe La Madeleine
'''
class ActionWrapper_PickSM(Behavior):
    '''
    action wrapper pour pick
    '''


    def __init__(self):
        super(ActionWrapper_PickSM, self).__init__()
        self.name = 'ActionWrapper_Pick'

        # parameters of this behavior

        # references to used behaviors

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
        
        # [/MANUAL_INIT]

        # Behavior comments:

        # O 357 51 
        # Pick|n1- object|n2- where to find it



    def create(self):
        # x:652 y:286, x:750 y:245
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['Action'])
        _state_machine.userdata.Action = ["Pick","elephant","room"]

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


        with _state_machine:
            # x:129 y:29
            OperatableStateMachine.add('cond',
                                        CheckConditionState(predicate=lambda x: x[2] != ''),
                                        transitions={'true': 'say Pick object', 'false': 'say no object given'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                        remapping={'input_value': 'Action'})

            # x:18 y:420
            OperatableStateMachine.add('say Pick object',
                                        SaraSayKey(Format=lambda x: " in the "+x[2], emotion=1, block=True),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'sentence': 'Action'})

            # x:192 y:167
            OperatableStateMachine.add('say no object given',
                                        SaraSayKey(Format=lambda x: "I'm going to pick that "+x[1], emotion=None, block=True),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'sentence': 'Action'})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
