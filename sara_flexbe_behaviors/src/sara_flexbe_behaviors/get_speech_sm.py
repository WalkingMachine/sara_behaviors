#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_get_speech')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.subscriber_state import SubscriberState
from flexbe_states.calculation_state import CalculationState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu Aug 24 2017
@author: Philippe La Madeleine
'''
class Get_speechSM(Behavior):
    '''
    get the text from speech
    '''


    def __init__(self):
        super(Get_speechSM, self).__init__()
        self.name = 'Get_speech'

        # parameters of this behavior

        # references to used behaviors

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
        
        # [/MANUAL_INIT]

        # Behavior comments:



    def create(self):
        # x:67 y:337, x:285 y:147
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], output_keys=['words'])
        _state_machine.userdata.words = ""

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


        with _state_machine:
            # x:38 y:133
            OperatableStateMachine.add('subber',
                                        SubscriberState(topic="/sara_command", blocking=True, clear=True),
                                        transitions={'received': 'get speech', 'unavailable': 'failed'},
                                        autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
                                        remapping={'message': 'message'})

            # x:40 y:234
            OperatableStateMachine.add('get speech',
                                        CalculationState(calculation=lambda x: x.data),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'input_value': 'message', 'output_value': 'words'})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
