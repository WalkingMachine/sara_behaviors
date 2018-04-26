#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_actionwrapper_lookat')
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
class ActionWrapper_LookAtSM(Behavior):
    '''
    action wrapper pour look_at
    '''


    def __init__(self):
        super(ActionWrapper_LookAtSM, self).__init__()
        self.name = 'ActionWrapper_LookAt'

        # parameters of this behavior

        # references to used behaviors

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
        
        # [/MANUAL_INIT]

        # Behavior comments:

        # O 308 5 
        # LookAt|n1- where to look at



    def create(self):
        # x:885 y:235, x:116 y:381
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['Action'])
        _state_machine.userdata.Action = ["LookAt", "you"]

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


        with _state_machine:
            # x:41 y:55
            OperatableStateMachine.add('cond',
                                        CheckConditionState(predicate=lambda x: x[1] != ''),
                                        transitions={'true': 'get', 'false': 'failed'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                        remapping={'input_value': 'Action'})

            # x:239 y:203
            OperatableStateMachine.add('say look at you',
                                        SaraSay(sentence="I'm looking at you", emotion=1, block=True),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off})

            # x:455 y:59
            OperatableStateMachine.add('say look at thing',
                                        SaraSayKey(Format=lambda x: "I'm looking at "+x[1], emotion=1, block=True),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'sentence': 'Action'})

            # x:245 y:51
            OperatableStateMachine.add('get',
                                        CheckConditionState(predicate=lambda x: x[1] != ''),
                                        transitions={'true': 'say look at you', 'false': 'say look at thing'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                        remapping={'input_value': 'Action'})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
