#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_actionwrapper_place')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.check_condition_state import CheckConditionState
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.sara_say_key import SaraSayKey
from flexbe_states.wait_state import WaitState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Tue Jul 11 2017
@author: Philippe La Madeleine
'''
class ActionWrapper_PlaceSM(Behavior):
    '''
    action wrapper pour place
    '''


    def __init__(self):
        super(ActionWrapper_PlaceSM, self).__init__()
        self.name = 'ActionWrapper_Place'

        # parameters of this behavior

        # references to used behaviors

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
        
        # [/MANUAL_INIT]

        # Behavior comments:

        # O 288 67 
        # Place|n1- where to put the object



    def create(self):
        # x:808 y:274, x:728 y:377
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['Action'])
        _state_machine.userdata.Action = ["Place", "table"]

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

        # x:30 y:322, x:130 y:322
        _sm_place_object_0 = OperatableStateMachine(outcomes=['finished', 'failed'])

        with _sm_place_object_0:
            # x:52 y:108
            OperatableStateMachine.add('wait',
                                        WaitState(wait_time=2),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off})



        with _state_machine:
            # x:37 y:67
            OperatableStateMachine.add('cond',
                                        CheckConditionState(predicate=lambda x: x[1] != ''),
                                        transitions={'true': 'say place object', 'false': 'say no place given'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                        remapping={'input_value': 'Action'})

            # x:31 y:544
            OperatableStateMachine.add('say no place given',
                                        SaraSay(sentence="I'm now going to place it right there", emotion=1),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off})

            # x:83 y:225
            OperatableStateMachine.add('say place object',
                                        SaraSayKey(Format=lambda x: "I'm now going to place it on that "+x[1], emotion=1),
                                        transitions={'done': 'Place object'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'sentence': 'Action'})

            # x:326 y:227
            OperatableStateMachine.add('Place object',
                                        _sm_place_object_0,
                                        transitions={'finished': 'finished', 'failed': 'failed'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
