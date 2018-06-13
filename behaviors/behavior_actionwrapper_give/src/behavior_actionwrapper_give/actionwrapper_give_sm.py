#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_actionwrapper_give')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.GetRosParam import GetRosParam
from behavior_action_give.action_give_sm import Action_GiveSM
from sara_flexbe_states.sara_say import SaraSay
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.sara_say_key import SaraSayKey
from flexbe_states.check_condition_state import CheckConditionState
from sara_flexbe_states.get_speech import GetSpeech
from behavior_action_findperson.action_findperson_sm import Action_findPersonSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sat June 2 2018
@author: Véronica
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
        self.add_behavior(Action_GiveSM, 'Action_Give')
        self.add_behavior(Action_findPersonSM, 'get_person/Action_findPerson_2')
        self.add_behavior(Action_findPersonSM, 'get_person/Action_findPerson')

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
        
        # [/MANUAL_INIT]

        # Behavior comments:

        # O 333 0 
        # Give|n1- to whom



    def create(self):
        # x:965 y:192, x:993 y:500, x:975 y:314
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'critical_fail'], input_keys=['Action', 'person_name'])
        _state_machine.userdata.Action = []
        _state_machine.userdata.person_name = " "

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

        # x:30 y:326, x:130 y:326, x:230 y:326
        _sm_get_person_0 = OperatableStateMachine(outcomes=['true', 'done', 'pas_done'], input_keys=['Action'], output_keys=['entity'])

        with _sm_get_person_0:
            # x:30 y:40
            OperatableStateMachine.add('cond',
                                        CheckConditionState(predicate=lambda x: x[1] != ''),
                                        transitions={'true': 'get ', 'false': 'Action_findPerson_2'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                        remapping={'input_value': 'Action'})

            # x:111 y:306
            OperatableStateMachine.add('is_person',
                                        SaraSayKey(Format=lambda x: "Hello, are you "+x+"?", emotion=1, block=True),
                                        transitions={'done': 'name'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'sentence': 'person_name'})

            # x:46 y:430
            OperatableStateMachine.add('name',
                                        GetSpeech(watchdog=5),
                                        transitions={'done': 'confirming_persons_name', 'nothing': 'name', 'fail': 'Action_findPerson'},
                                        autonomy={'done': Autonomy.Off, 'nothing': Autonomy.Off, 'fail': Autonomy.Off},
                                        remapping={'words': 'person_name'})

            # x:244 y:426
            OperatableStateMachine.add('confirming_persons_name',
                                        CheckConditionState(predicate=lambda x: "yes" in x),
                                        transitions={'true': 'true', 'false': 'Action_findPerson'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                        remapping={'input_value': 'person_name'})

            # x:338 y:105
            OperatableStateMachine.add('Action_findPerson_2',
                                        self.use_behavior(Action_findPersonSM, 'get_person/Action_findPerson_2'),
                                        transitions={'done': 'done', 'pas_done': 'pas_done'},
                                        autonomy={'done': Autonomy.Inherit, 'pas_done': Autonomy.Inherit},
                                        remapping={'className': 'Action', 'entity': 'person_name'})

            # x:30 y:187
            OperatableStateMachine.add('Action_findPerson',
                                        self.use_behavior(Action_findPersonSM, 'get_person/Action_findPerson'),
                                        transitions={'done': 'is_person', 'pas_done': 'Action_findPerson_2'},
                                        autonomy={'done': Autonomy.Inherit, 'pas_done': Autonomy.Inherit},
                                        remapping={'className': 'Action', 'entity': 'entity'})

            # x:46 y:116
            OperatableStateMachine.add('get ',
                                        CalculationState(calculation=lambda x: x[1]),
                                        transitions={'done': 'Action_findPerson'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'input_value': 'Action', 'output_value': 'person_name'})



        with _state_machine:
            # x:43 y:40
            OperatableStateMachine.add('Object',
                                        GetRosParam(ParamName=behavior/GripperContent),
                                        transitions={'done': 'get_person', 'failed': 'no_object'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'Value': 'gripperContent'})

            # x:576 y:259
            OperatableStateMachine.add('Action_Give',
                                        self.use_behavior(Action_GiveSM, 'Action_Give'),
                                        transitions={'Given': 'finished', 'Person_not_found': 'person_lost', 'No_object_in_hand': 'failed', 'fail': 'critical_fail'},
                                        autonomy={'Given': Autonomy.Inherit, 'Person_not_found': Autonomy.Inherit, 'No_object_in_hand': Autonomy.Inherit, 'fail': Autonomy.Inherit})

            # x:501 y:66
            OperatableStateMachine.add('Nobody_here',
                                        SaraSay(sentence="I can't find a person. Goodbye.", emotion=1, block=True),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off})

            # x:594 y:425
            OperatableStateMachine.add('getID',
                                        CalculationState(calculation=lambda x: x.ID),
                                        transitions={'done': 'Action_Give'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'input_value': 'entity', 'output_value': 'ID'})

            # x:738 y:446
            OperatableStateMachine.add('person_lost',
                                        SaraSayKey(Format=lambda x: "I've lost "+x+"!", emotion=1, block=True),
                                        transitions={'done': 'failed'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'sentence': 'person_name'})

            # x:159 y:259
            OperatableStateMachine.add('get_person',
                                        _sm_get_person_0,
                                        transitions={'true': 'confirm giving', 'done': 'confirm giving', 'pas_done': 'Nobody_here'},
                                        autonomy={'true': Autonomy.Inherit, 'done': Autonomy.Inherit, 'pas_done': Autonomy.Inherit},
                                        remapping={'Action': 'Action', 'entity': 'entity'})

            # x:53 y:480
            OperatableStateMachine.add('no_object',
                                        SaraSay(sentence="There is nothing in my gripper.", emotion=1, block=True),
                                        transitions={'done': 'failed'},
                                        autonomy={'done': Autonomy.Off})

            # x:462 y:428
            OperatableStateMachine.add('confirm giving',
                                        SaraSay(sentence="Let me give you this object.", emotion=1, block=True),
                                        transitions={'done': 'getID'},
                                        autonomy={'done': Autonomy.Off})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
