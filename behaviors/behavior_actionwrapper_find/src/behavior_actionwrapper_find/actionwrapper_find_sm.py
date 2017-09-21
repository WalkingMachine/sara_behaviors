#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_actionwrapper_find')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.check_condition_state import CheckConditionState
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.sara_say_key import SaraSayKey
from flexbe_states.calculation_state import CalculationState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Tue Jul 11 2017
@author: Philippe La Madeleine
'''
class ActionWrapper_FindSM(Behavior):
    '''
    action wrapper pour find
    '''


    def __init__(self):
        super(ActionWrapper_FindSM, self).__init__()
        self.name = 'ActionWrapper_Find'

        # parameters of this behavior

        # references to used behaviors

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
        
        # [/MANUAL_INIT]

        # Behavior comments:

        # O 308 15 
        # Find|n1- what to find|n2- where to look for



    def create(self):
        # x:846 y:287, x:842 y:366
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['Action'])
        _state_machine.userdata.Action = ["Find","power","universe"]

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

        # x:30 y:325
        _sm_look_at_location_0 = OperatableStateMachine(outcomes=['done'], input_keys=['Action'])

        with _sm_look_at_location_0:
            # x:30 y:40
            OperatableStateMachine.add('get location name',
                                        CalculationState(calculation=lambda x: x[1]),
                                        transitions={'done': 'done'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'input_value': 'Action', 'output_value': 'name'})



        with _state_machine:
            # x:24 y:18
            OperatableStateMachine.add('cond',
                                        CheckConditionState(predicate=lambda x: x[1] != ''),
                                        transitions={'true': 'cond2', 'false': 'say no object given'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                        remapping={'input_value': 'Action'})

            # x:243 y:76
            OperatableStateMachine.add('say no object given',
                                        SaraSay(sentence="You didn't told me what to find.", emotion=1),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off})

            # x:33 y:289
            OperatableStateMachine.add('cond2',
                                        CheckConditionState(predicate=lambda x: x[2] != ''),
                                        transitions={'true': 'say find object in area', 'false': 'say find object'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                        remapping={'input_value': 'Action'})

            # x:241 y:290
            OperatableStateMachine.add('say find object',
                                        SaraSayKey(Format=lambda x: "I'm now looking for the "+x[1], emotion=1),
                                        transitions={'done': 'Look at location'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'sentence': 'Action'})

            # x:223 y:532
            OperatableStateMachine.add('say find object in area',
                                        SaraSayKey(Format=lambda x: "I'm now looking for the "+x[1]+" in the "+x[2], emotion=1),
                                        transitions={'done': 'Look at location'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'sentence': 'Action'})

            # x:445 y:300
            OperatableStateMachine.add('Look at location',
                                        _sm_look_at_location_0,
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Inherit},
                                        remapping={'Action': 'Action'})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
