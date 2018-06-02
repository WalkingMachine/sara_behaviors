#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_actionwrapper_give')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.sara_say import SaraSay
from flexbe_states.check_condition_state import CheckConditionState
from behavior_action_findperson.action_findperson_sm import Action_findPersonSM
from sara_flexbe_states.sara_say_key import SaraSayKey
from sara_flexbe_states.get_speech import GetSpeech
from behavior_action_give.action_give_sm import Action_GiveSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on 2018-June-2
@author: Veronica
'''
class ActionWrapper_GiveSM(Behavior):
    '''
    action wrapper pour give
    '''


    def __init__(self):
        super(ActionWrapper_GiveSM, self).__init__()
        self.name = 'ActionWrapper_Give'

        # parameters of this behavior

        # references to used behaviors
        self.add_behavior(Action_findPersonSM, 'Action_findPerson')
        self.add_behavior(Action_GiveSM, 'Action_Give')

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
        
        # [/MANUAL_INIT]

        # Behavior comments:

        # O 333 0 
        # Give|n1- to who



    def create(self):
        # x:892 y:284, x:469 y:512, x:714 y:496
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'critical_fail'], input_keys=['Action', 'person_name'])
        _state_machine.userdata.Action = []
        _state_machine.userdata.person_name = " "

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


        with _state_machine:
            # x:48 y:31
            OperatableStateMachine.add('get ',
                                        CalculationState(calculation=lambda x: x[1]),
                                        transitions={'done': 'cond'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'input_value': 'Action', 'output_value': 'object'})

            # x:337 y:409
            OperatableStateMachine.add('say giving',
                                        SaraSay(sentence="I'm giving it to you", emotion=1, block=True),
                                        transitions={'done': 'Action_Give'},
                                        autonomy={'done': Autonomy.Off})

            # x:47 y:126
            OperatableStateMachine.add('cond',
                                        CheckConditionState(predicate=lambda x: x[2] != ''),
                                        transitions={'true': 'Action_findPerson', 'false': 'cond'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                        remapping={'input_value': 'Action'})

            # x:28 y:213
            OperatableStateMachine.add('Action_findPerson',
                                        self.use_behavior(Action_findPersonSM, 'Action_findPerson'),
                                        transitions={'done': 'name', 'pas_done': 'Action_findPerson'},
                                        autonomy={'done': Autonomy.Inherit, 'pas_done': Autonomy.Inherit},
                                        remapping={'className': 'Action', 'entity': 'person_name'})

            # x:122 y:314
            OperatableStateMachine.add('is_person',
                                        SaraSayKey(Format="bonjur", emotion=1, block=True),
                                        transitions={'done': 'name'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'sentence': 'sentence'})

            # x:33 y:391
            OperatableStateMachine.add('name',
                                        GetSpeech(watchdog=5),
                                        transitions={'done': 'confirming_name', 'nothing': 'Action_findPerson', 'fail': 'Action_findPerson'},
                                        autonomy={'done': Autonomy.Off, 'nothing': Autonomy.Off, 'fail': Autonomy.Off},
                                        remapping={'words': 'sentence'})

            # x:218 y:348
            OperatableStateMachine.add('confirming_name',
                                        CheckConditionState(predicate=lambda x: "yes" in x),
                                        transitions={'true': 'say giving', 'false': 'failed'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                        remapping={'input_value': 'sentence'})

            # x:501 y:325
            OperatableStateMachine.add('Action_Give',
                                        self.use_behavior(Action_GiveSM, 'Action_Give'),
                                        transitions={'Given': 'finished', 'Person_not_found': 'failed', 'No_object_in_hand': 'failed', 'fail': 'critical_fail'},
                                        autonomy={'Given': Autonomy.Inherit, 'Person_not_found': Autonomy.Inherit, 'No_object_in_hand': Autonomy.Inherit, 'fail': Autonomy.Inherit},
                                        remapping={'person_id': 'person_name'})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
