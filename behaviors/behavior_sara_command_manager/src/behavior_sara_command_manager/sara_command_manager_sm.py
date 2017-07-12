#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_sara_command_manager')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.subscriber_state import SubscriberState
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.lu4r_parser import LU4R_Parser
from flexbe_states.calculation_state import CalculationState
from flexbe_states.check_condition_state import CheckConditionState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Tue Jul 11 2017
@author: Philippe La Madeleine
'''
class sara_command_managerSM(Behavior):
    '''
    the command manager of Sara
    '''


    def __init__(self):
        super(sara_command_managerSM, self).__init__()
        self.name = 'sara_command_manager'

        # parameters of this behavior

        # references to used behaviors

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
        
        # [/MANUAL_INIT]

        # Behavior comments:



    def create(self):
        # x:705 y:127, x:609 y:334
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['HighFIFO', 'MedFIFO', 'LowFIFO', 'DoNow'])
        _state_machine.userdata.HighFIFO = []
        _state_machine.userdata.MedFIFO = []
        _state_machine.userdata.LowFIFO = []
        _state_machine.userdata.DoNow = []
        _state_machine.userdata.Default_message = ""

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


        with _state_machine:
            # x:44 y:112
            OperatableStateMachine.add('sub',
                                        SubscriberState(topic="/sara_command", blocking=False, clear=False),
                                        transitions={'received': 'sss', 'unavailable': 'finished'},
                                        autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
                                        remapping={'message': 'message'})

            # x:404 y:211
            OperatableStateMachine.add('sorry',
                                        SaraSay(sentence="Sorry, I did not understand. Could you repeat please?", emotion=1),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off})

            # x:378 y:40
            OperatableStateMachine.add('parse text',
                                        LU4R_Parser(),
                                        transitions={'done': 'finished', 'fail': 'sorry'},
                                        autonomy={'done': Autonomy.Off, 'fail': Autonomy.Off},
                                        remapping={'sentence': 'sentence', 'HighFIFO': 'HighFIFO', 'MedFIFO': 'MedFIFO', 'LowFIFO': 'LowFIFO', 'DoNow': 'DoNow'})

            # x:216 y:41
            OperatableStateMachine.add('GET TEXT',
                                        CalculationState(calculation=lambda x: x.data),
                                        transitions={'done': 'parse text'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'input_value': 'message', 'output_value': 'sentence'})

            # x:103 y:185
            OperatableStateMachine.add('sss',
                                        CheckConditionState(predicate=lambda x: x != None),
                                        transitions={'true': 'GET TEXT', 'false': 'finished'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                        remapping={'input_value': 'message'})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
