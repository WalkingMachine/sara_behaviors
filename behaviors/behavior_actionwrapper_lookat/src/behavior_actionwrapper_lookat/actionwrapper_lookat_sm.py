#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_actionwrapper_lookat')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.sara_say_key import SaraSayKey
from sara_flexbe_states.sara_set_head_angle import SaraSetHeadAngle
from flexbe_states.check_condition_state import CheckConditionState
from behavior_action_look_at.action_look_at_sm import action_look_atSM
from sara_flexbe_states.list_entities_by_name import list_entities_by_name
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on 19 mai 2018
@author: Veronica R
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
        self.add_behavior(action_look_atSM, 'action_look_at')

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
        
        # [/MANUAL_INIT]

        # Behavior comments:

        # O 191 1 
        # LookAt|n1- where to look at



    def create(self):
        # x:1213 y:438
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'critical_fail'], input_keys=['Action'])
        _state_machine.userdata.Action = ["LookAt", "you"]
        _state_machine.userdata.ID = 0
        _state_machine.userdata.name = ["bottle"]

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


        with _state_machine:
            # x:49 y:42
            OperatableStateMachine.add('getName',
                                        CalculationState(calculation=lambda x: x[1]),
                                        transitions={'done': 'cond'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'input_value': 'Action', 'output_value': 'name'})

            # x:229 y:429
            OperatableStateMachine.add('say nothing to look at',
                                        SaraSayKey(Format=lambda x: "You didn't told me what to look at.", emotion=1, block=True),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'sentence': 'Action'})

            # x:977 y:45
            OperatableStateMachine.add('Say look at object',
                                        SaraSayKey(Format=lambda x: "I am looking at the "+ x, emotion=1, block=True),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'sentence': 'name'})

            # x:390 y:123
            OperatableStateMachine.add('Look for object',
                                        SaraSetHeadAngle(pitch=-0.2, yaw=1.5),
                                        transitions={'done': 'Looking'},
                                        autonomy={'done': Autonomy.Off})

            # x:563 y:288
            OperatableStateMachine.add('Look the other side',
                                        SaraSetHeadAngle(pitch=-0.2, yaw=-1.5),
                                        transitions={'done': 'look again'},
                                        autonomy={'done': Autonomy.Off})

            # x:402 y:207
            OperatableStateMachine.add('Looking',
                                        SaraSayKey(Format=lambda x: "I am looking for "+ x[1], emotion=1, block=True),
                                        transitions={'done': 'look for'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'sentence': 'Action'})

            # x:958 y:289
            OperatableStateMachine.add('not found',
                                        SaraSayKey(Format=lambda x: "I couldn't find the " +x[1], emotion=1, block=True),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'sentence': 'Action'})

            # x:593 y:38
            OperatableStateMachine.add('GetPosition',
                                        CalculationState(calculation=lambda x: x[0].position),
                                        transitions={'done': 'action_look_at'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'input_value': 'entity_list', 'output_value': 'Position'})

            # x:219 y:43
            OperatableStateMachine.add('cond',
                                        CheckConditionState(predicate=lambda x: x != ''),
                                        transitions={'true': 'Entity', 'false': 'say nothing to look at'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                        remapping={'input_value': 'name'})

            # x:778 y:34
            OperatableStateMachine.add('action_look_at',
                                        self.use_behavior(action_look_atSM, 'action_look_at'),
                                        transitions={'finished': 'Say look at object'},
                                        autonomy={'finished': Autonomy.Inherit},
                                        remapping={'Position': 'Position'})

            # x:387 y:42
            OperatableStateMachine.add('Entity',
                                        list_entities_by_name(frontality_level=0.5),
                                        transitions={'found': 'GetPosition', 'not_found': 'Look for object'},
                                        autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
                                        remapping={'name': 'name', 'entity_list': 'entity_list', 'number': 'number'})

            # x:384 y:287
            OperatableStateMachine.add('look for',
                                        list_entities_by_name(frontality_level=0.5),
                                        transitions={'found': 'GetPosition', 'not_found': 'Look the other side'},
                                        autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
                                        remapping={'name': 'name', 'entity_list': 'entity_list', 'number': 'number'})

            # x:738 y:288
            OperatableStateMachine.add('look again',
                                        list_entities_by_name(frontality_level=0.5),
                                        transitions={'found': 'GetPosition', 'not_found': 'not found'},
                                        autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
                                        remapping={'name': 'name', 'entity_list': 'entity_list', 'number': 'number'})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
