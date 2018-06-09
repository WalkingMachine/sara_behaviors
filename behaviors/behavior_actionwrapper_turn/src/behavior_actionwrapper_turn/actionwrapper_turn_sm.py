#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_actionwrapper_turn')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.sara_say_key import SaraSayKey
from flexbe_states.check_condition_state import CheckConditionState
from sara_flexbe_states.sara_say import SaraSay
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Tue Jul 11 2017
@author: Philippe La Madeleine
'''
class ActionWrapper_TurnSM(Behavior):
    '''
    action wrapper pour turn
    '''


    def __init__(self):
        super(ActionWrapper_TurnSM, self).__init__()
        self.name = 'ActionWrapper_Turn'

        # parameters of this behavior

        # references to used behaviors

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
        
        # [/MANUAL_INIT]

        # Behavior comments:

        # O 295 63 
        # Turn|n1- direction



    def create(self):
        # x:892 y:301, x:888 y:436
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'critical_fail'], input_keys=['Action'])
        _state_machine.userdata.Action = ["Turn","Right"]

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


        with _state_machine:
            # x:42 y:47
            OperatableStateMachine.add('cond',
                                        CheckConditionState(predicate=lambda x: x[1] != ''),
                                        transitions={'true': 'say turn', 'false': 'say no direction given'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                        remapping={'input_value': 'Action'})

            # x:59 y:355
            OperatableStateMachine.add('say no direction given',
                                        SaraSay(sentence="You didn't told me witch direction to turn", emotion=1),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off})

            # x:112 y:159
            OperatableStateMachine.add('say turn',
                                        SaraSayKey(Format=lambda x: "I gonna turn "+x[1], emotion=1),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'sentence': 'Action'})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
