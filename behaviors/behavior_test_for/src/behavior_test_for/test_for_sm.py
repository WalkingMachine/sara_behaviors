#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_test_for')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.log_state import LogState
from sara_flexbe_states.for_loop import ForLoop
from sara_flexbe_states.regex_tester import RegexTester
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu Jul 27 2017
@author: Philippe La Madeleine
'''
class testforSM(Behavior):
    '''
    test the for state
    '''


    def __init__(self):
        super(testforSM, self).__init__()
        self.name = 'test for'

        # parameters of this behavior

        # references to used behaviors

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
        
        # [/MANUAL_INIT]

        # Behavior comments:



    def create(self):
        # x:30 y:322, x:388 y:382
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
        _state_machine.userdata.text = "it tests"

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


        with _state_machine:
            # x:132 y:39
            OperatableStateMachine.add('log',
                                        LogState(text="test", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'reg'},
                                        autonomy={'done': Autonomy.Off})

            # x:129 y:155
            OperatableStateMachine.add('for',
                                        ForLoop(repeat=4),
                                        transitions={'do': 'failed', 'end': 'finished'},
                                        autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
                                        remapping={'index': 'index'})

            # x:370 y:185
            OperatableStateMachine.add('reg',
                                        RegexTester(regex=".*test.*"),
                                        transitions={'true': 'success', 'false': 'failed'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                        remapping={'text': 'text', 'result': 'result'})

            # x:217 y:298
            OperatableStateMachine.add('success',
                                        LogState(text="success", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
