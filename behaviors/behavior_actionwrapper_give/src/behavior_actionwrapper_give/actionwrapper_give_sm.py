#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_actionwrapper_give')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.sara_say_key import SaraSayKey
from flexbe_states.check_condition_state import CheckConditionState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Tue Jul 11 2017
@author: Philippe La Madeleine
'''
class ActionWrapper_GiveSM(Behavior):
    '''
    action wrapper pour give
    '''


    def __init__(self):
        super(ActionWrapper_GiveSM, self).__init__()
        self.name = 'ActionWrapper_Give'

        # parameters of this behavior

        # references to used behaviors

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
        
        # [/MANUAL_INIT]

        # Behavior comments:

        # O 288 66 
        # Give|n1- what|n2- to who



    def create(self):
        # x:892 y:284, x:885 y:449
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'critical_fail'], input_keys=['Action'])
        _state_machine.userdata.Action = []

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


        with _state_machine:
            # x:43 y:94
            OperatableStateMachine.add('get ',
                                        CalculationState(calculation=lambda x: x[1]),
                                        transitions={'done': 'cond'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'input_value': 'Action', 'output_value': 'object'})

            # x:232 y:184
            OperatableStateMachine.add('say giving',
                                        SaraSay(sentence="I'm giving it to you", emotion=1, block=True),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off})

            # x:196 y:284
            OperatableStateMachine.add('say giving to person',
                                        SaraSayKey(Format=lambda x: "I'm giving it to "+x[1], emotion=1, block=True),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'sentence': 'Action'})

            # x:40 y:190
            OperatableStateMachine.add('cond',
                                        CheckConditionState(predicate=lambda x: x[2] != ''),
                                        transitions={'true': 'say giving to person', 'false': 'say giving'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                        remapping={'input_value': 'Action'})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
