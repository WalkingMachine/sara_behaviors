#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_testbooltopic')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.subscriber_state import SubscriberState
from flexbe_states.check_condition_state import CheckConditionState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sun May 21 2017
@author: Philippe La Madeleine
'''
class TestBoolTopicSM(Behavior):
    '''
    Test a Boolean topic.
    '''


    def __init__(self):
        super(TestBoolTopicSM, self).__init__()
        self.name = 'TestBoolTopic'

        # parameters of this behavior

        # references to used behaviors

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
        
        # [/MANUAL_INIT]

        # Behavior comments:



    def create(self):
        # x:488 y:137, x:444 y:183
        _state_machine = OperatableStateMachine(outcomes=['True', 'False'])
        _state_machine.userdata.Clear = False
        _state_machine.userdata.Blocking = True
        _state_machine.userdata.Topic = "/Topic"

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


        with _state_machine:
            # x:60 y:110
            OperatableStateMachine.add('sub',
                                        SubscriberState(topic="/Topic", blocking=True, clear=True),
                                        transitions={'received': 'cond', 'unavailable': 'False'},
                                        autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
                                        remapping={'message': 'message'})

            # x:273 y:57
            OperatableStateMachine.add('cond',
                                        CheckConditionState(predicate=lambda x: x.data),
                                        transitions={'true': 'True', 'false': 'False'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                        remapping={'input_value': 'message'})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
