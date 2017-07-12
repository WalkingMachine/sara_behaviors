#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_actionwrapper_bring')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.check_condition_state import CheckConditionState
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.sara_say_key import SaraSayKey
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Tue Jul 11 2017
@author: Philippe La Madeleine
'''
class ActionWrapper_BringSM(Behavior):
    '''
    action wrapper pour bring
    '''


    def __init__(self):
        super(ActionWrapper_BringSM, self).__init__()
        self.name = 'ActionWrapper_Bring'

        # parameters of this behavior

        # references to used behaviors

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
        
        # [/MANUAL_INIT]

        # Behavior comments:

        # O 424 44 
        # Bring|n1- object|n2- area|n3- beneficiary



    def create(self):
        # x:512 y:478, x:224 y:503
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['Action'])
        _state_machine.userdata.Action = ["Bring","love","the world"]

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


        with _state_machine:
            # x:151 y:100
            OperatableStateMachine.add('cond',
                                        CheckConditionState(predicate=lambda x: x[1] != ''),
                                        transitions={'true': 'cond2', 'false': 'say'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                        remapping={'input_value': 'Action'})

            # x:63 y:202
            OperatableStateMachine.add('say',
                                        SaraSay(sentence="You didn't told me what to bring", emotion=1),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off})

            # x:456 y:176
            OperatableStateMachine.add('cond2',
                                        CheckConditionState(predicate=lambda x: x[2] != ''),
                                        transitions={'true': 'say3', 'false': 'say22'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                        remapping={'input_value': 'Action'})

            # x:551 y:348
            OperatableStateMachine.add('say3',
                                        SaraSayKey(Format=lambda x: "I'm now gonna bring the "+x[1]+" to "+x[2], emotion=1),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'sentence': 'Action'})

            # x:411 y:333
            OperatableStateMachine.add('say22',
                                        SaraSayKey(Format=lambda x: "I'm now gonna bring the "+x[1], emotion=1),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'sentence': 'Action'})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
