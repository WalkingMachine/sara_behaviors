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
from flexbe_states.wait_state import WaitState
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

        # O 508 30 
        # Bring|n1- object|n2- area|n3- beneficiary



    def create(self):
        # x:868 y:291, x:857 y:562
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['Action'])
        _state_machine.userdata.Action = ["Bring","love","the world"]

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

        # x:30 y:322, x:130 y:322
        _sm_get_person_by_name_0 = OperatableStateMachine(outcomes=['finished', 'failed'])

        with _sm_get_person_by_name_0:
            # x:36 y:106
            OperatableStateMachine.add('wait',
                                        WaitState(wait_time=2),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off})


        # x:30 y:322, x:130 y:322
        _sm_get_operator_1 = OperatableStateMachine(outcomes=['finished', 'failed'])

        with _sm_get_operator_1:
            # x:71 y:186
            OperatableStateMachine.add('wait',
                                        WaitState(wait_time=2),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off})


        # x:30 y:322, x:130 y:322
        _sm_bring_to_2 = OperatableStateMachine(outcomes=['finished', 'failed'])

        with _sm_bring_to_2:
            # x:53 y:151
            OperatableStateMachine.add('wait',
                                        WaitState(wait_time=2),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off})



        with _state_machine:
            # x:53 y:75
            OperatableStateMachine.add('cond',
                                        CheckConditionState(predicate=lambda x: x[1] != ''),
                                        transitions={'true': 'cond2', 'false': 'say no object given'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                        remapping={'input_value': 'Action'})

            # x:266 y:85
            OperatableStateMachine.add('say no object given',
                                        SaraSay(sentence="You didn't told me what to bring", emotion=1),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off})

            # x:53 y:176
            OperatableStateMachine.add('cond2',
                                        CheckConditionState(predicate=lambda x: x[2] != ''),
                                        transitions={'true': 'say3', 'false': 'say22'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                        remapping={'input_value': 'Action'})

            # x:84 y:485
            OperatableStateMachine.add('say3',
                                        SaraSayKey(Format=lambda x: "I'm now gonna bring the "+x[1]+" to "+x[2], emotion=1),
                                        transitions={'done': 'Get operator'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'sentence': 'Action'})

            # x:133 y:279
            OperatableStateMachine.add('say22',
                                        SaraSayKey(Format=lambda x: "I'm now gonna bring the "+x[1], emotion=1),
                                        transitions={'done': 'Get person by name'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'sentence': 'Action'})

            # x:647 y:320
            OperatableStateMachine.add('Bring to',
                                        _sm_bring_to_2,
                                        transitions={'finished': 'finished', 'failed': 'failed'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

            # x:298 y:466
            OperatableStateMachine.add('Get operator',
                                        _sm_get_operator_1,
                                        transitions={'finished': 'Bring to', 'failed': 'failed'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

            # x:304 y:275
            OperatableStateMachine.add('Get person by name',
                                        _sm_get_person_by_name_0,
                                        transitions={'finished': 'Bring to', 'failed': 'failed'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
