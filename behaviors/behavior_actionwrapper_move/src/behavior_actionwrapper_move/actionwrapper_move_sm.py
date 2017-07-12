#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_actionwrapper_move')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
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
class ActionWrapper_MoveSM(Behavior):
    '''
    action wrapper pour move_base
    '''


    def __init__(self):
        super(ActionWrapper_MoveSM, self).__init__()
        self.name = 'ActionWrapper_Move'

        # parameters of this behavior

        # references to used behaviors

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
        
        # [/MANUAL_INIT]

        # Behavior comments:

        # O 287 66 
        # move|n1- where to go|n2- direction to go (oferriden by 1-)|n3- distance to go (oferriden by 1-)



    def create(self):
        # x:822 y:356, x:859 y:573
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['Action'])
        _state_machine.userdata.Action = ['Move','kitchen','forward','1 meter']

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


        with _state_machine:
            # x:52 y:28
            OperatableStateMachine.add('say okay',
                                        SaraSay(sentence="Okay", emotion=1),
                                        transitions={'done': 'check'},
                                        autonomy={'done': Autonomy.Off})

            # x:111 y:242
            OperatableStateMachine.add('say area',
                                        SaraSayKey(Format=lambda x: "I'm going to the "+x[1], emotion=1),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'sentence': 'Action'})

            # x:33 y:116
            OperatableStateMachine.add('check',
                                        CheckConditionState(predicate=lambda x: x[1] != ''),
                                        transitions={'true': 'say area', 'false': 'say vector'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                        remapping={'input_value': 'Action'})

            # x:100 y:479
            OperatableStateMachine.add('say vector',
                                        SaraSayKey(Format=lambda x: "I'm going to move "+x[2]+x[3], emotion=1),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'sentence': 'Action'})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
