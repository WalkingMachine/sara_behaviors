#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_action_count')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.sara_set_head_angle import SaraSetHeadAngle
from flexbe_states.log_key_state import LogKeyState
from flexbe_states.wait_state import WaitState
from sara_flexbe_states.list_entities_by_name import list_entities_by_name
from sara_flexbe_states.SetKey import SetKey
from flexbe_states.flexible_calculation_state import FlexibleCalculationState
from behavior_action_turn.action_turn_sm import action_turnSM
from flexbe_states.decision_state import DecisionState
from sara_flexbe_states.SetRosParamKey import SetRosParamKey
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sat Jun 1 2018
@author: Raphael Duchaine
'''
class Action_countSM(Behavior):
    '''
    Count instances of entity class around sara (will only rotate, won't move).
    '''


    def __init__(self):
        super(Action_countSM, self).__init__()
        self.name = 'Action_count'

        # parameters of this behavior

        # references to used behaviors
        self.add_behavior(action_turnSM, 'Count instances WHILE Turning360/Rotation360/action_turn')

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
        
        # [/MANUAL_INIT]

        # Behavior comments:



    def create(self):
        # x:775 y:149, x:556 y:207
        _state_machine = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['className'], output_keys=['counter'])
        _state_machine.userdata.className = "person"
        _state_machine.userdata.counter = 0

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

        # x:691 y:456, x:442 y:120, x:506 y:322
        _sm_rotation360_0 = OperatableStateMachine(outcomes=['end', 'in_progress', 'failed'], input_keys=['progress'])

        with _sm_rotation360_0:
            # x:11 y:227
            OperatableStateMachine.add('DecisionState',
                                        DecisionState(outcomes=["0","0.25","0.5","0.75","1"], conditions=lambda x: x),
                                        transitions={'0': 'Look Left', '0.25': 'Look Right', '0.5': 'Set 180 degres', '0.75': 'Look Right 2', '1': 'Look Left 2'},
                                        autonomy={'0': Autonomy.Off, '0.25': Autonomy.Off, '0.5': Autonomy.Off, '0.75': Autonomy.Off, '1': Autonomy.Off},
                                        remapping={'input_value': 'progress'})

            # x:258 y:199
            OperatableStateMachine.add('action_turn',
                                        self.use_behavior(action_turnSM, 'Count instances WHILE Turning360/Rotation360/action_turn'),
                                        transitions={'finished': 'in_progress', 'failed': 'failed'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'rotation': 'rotation'})

            # x:157 y:114
            OperatableStateMachine.add('Look Right',
                                        SaraSetHeadAngle(pitch=0.5, yaw=-1.5),
                                        transitions={'done': 'Rotate Right'},
                                        autonomy={'done': Autonomy.Off})

            # x:290 y:31
            OperatableStateMachine.add('Rotate Left',
                                        WaitState(wait_time=8),
                                        transitions={'done': 'in_progress'},
                                        autonomy={'done': Autonomy.Off})

            # x:307 y:108
            OperatableStateMachine.add('Rotate Right',
                                        WaitState(wait_time=12),
                                        transitions={'done': 'in_progress'},
                                        autonomy={'done': Autonomy.Off})

            # x:134 y:34
            OperatableStateMachine.add('Look Left',
                                        SaraSetHeadAngle(pitch=0.5, yaw=1.5),
                                        transitions={'done': 'Rotate Left'},
                                        autonomy={'done': Autonomy.Off})

            # x:124 y:382
            OperatableStateMachine.add('Look Left 2',
                                        SaraSetHeadAngle(pitch=0.5, yaw=1.5),
                                        transitions={'done': 'Rotate Left 2'},
                                        autonomy={'done': Autonomy.Off})

            # x:130 y:298
            OperatableStateMachine.add('Look Right 2',
                                        SaraSetHeadAngle(pitch=0.5, yaw=-1.5),
                                        transitions={'done': 'Rotate Right 2'},
                                        autonomy={'done': Autonomy.Off})

            # x:270 y:381
            OperatableStateMachine.add('Rotate Left 2',
                                        WaitState(wait_time=12),
                                        transitions={'done': 'end'},
                                        autonomy={'done': Autonomy.Off})

            # x:278 y:292
            OperatableStateMachine.add('Rotate Right 2',
                                        WaitState(wait_time=8),
                                        transitions={'done': 'in_progress'},
                                        autonomy={'done': Autonomy.Off})

            # x:143 y:221
            OperatableStateMachine.add('Set 180 degres',
                                        SetKey(Value=3.1416),
                                        transitions={'done': 'action_turn'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'Key': 'rotation'})


        # x:500 y:303
        _sm_count_instancies_1 = OperatableStateMachine(outcomes=['counted'], input_keys=['className'])

        with _sm_count_instancies_1:
            # x:84 y:255
            OperatableStateMachine.add('SetKey',
                                        SetKey(Value=0),
                                        transitions={'done': 'find_an_instance'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'Key': 'counter'})

            # x:453 y:163
            OperatableStateMachine.add('counter+len(instances)',
                                        FlexibleCalculationState(calculation=lambda x: x[0]+x[1], input_keys=["counter","number"]),
                                        transitions={'done': 'counted'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'counter': 'counter', 'number': 'number', 'output_value': 'counter'})

            # x:181 y:178
            OperatableStateMachine.add('find_an_instance',
                                        list_entities_by_name(frontality_level=0.5),
                                        transitions={'found': 'counter+len(instances)', 'not_found': 'counted'},
                                        autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
                                        remapping={'name': 'className', 'entity_list': 'entity_list', 'number': 'number'})


        # x:451 y:193, x:441 y:295
        _sm_count_instances_while_turning360_2 = OperatableStateMachine(outcomes=['found', 'failed'], input_keys=['className', 'progress'])

        with _sm_count_instances_while_turning360_2:
            # x:131 y:44
            OperatableStateMachine.add('Count Instancies',
                                        _sm_count_instancies_1,
                                        transitions={'counted': 'Rotation360'},
                                        autonomy={'counted': Autonomy.Inherit},
                                        remapping={'className': 'className'})

            # x:281 y:191
            OperatableStateMachine.add('Rotation360',
                                        _sm_rotation360_0,
                                        transitions={'end': 'found', 'in_progress': 'Count Instancies', 'failed': 'failed'},
                                        autonomy={'end': Autonomy.Inherit, 'in_progress': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'progress': 'progress'})



        with _state_machine:
            # x:110 y:88
            OperatableStateMachine.add('Look Front Center',
                                        SaraSetHeadAngle(pitch=0.5, yaw=0),
                                        transitions={'done': 'SetProgress'},
                                        autonomy={'done': Autonomy.Off})

            # x:574 y:63
            OperatableStateMachine.add('Look Center Found',
                                        SaraSetHeadAngle(pitch=0.5, yaw=0),
                                        transitions={'done': 'Log Count'},
                                        autonomy={'done': Autonomy.Off})

            # x:773 y:38
            OperatableStateMachine.add('Log Count',
                                        LogKeyState(text="Found: {}", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'done'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'data': 'counter'})

            # x:635 y:153
            OperatableStateMachine.add('WaitState',
                                        WaitState(wait_time=1),
                                        transitions={'done': 'Look Center Found'},
                                        autonomy={'done': Autonomy.Off})

            # x:318 y:103
            OperatableStateMachine.add('Count instances WHILE Turning360',
                                        _sm_count_instances_while_turning360_2,
                                        transitions={'found': 'SetParamName', 'failed': 'failed'},
                                        autonomy={'found': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'className': 'className', 'progress': 'progress'})

            # x:558 y:256
            OperatableStateMachine.add('SetRosParamKeyCounter',
                                        SetRosParamKey(),
                                        transitions={'done': 'WaitState'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'Value': 'counter', 'ParamName': 'ParamName'})

            # x:345 y:257
            OperatableStateMachine.add('SetParamName',
                                        SetKey(Value=counter),
                                        transitions={'done': 'SetRosParamKeyCounter'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'Key': 'ParamName'})

            # x:159 y:171
            OperatableStateMachine.add('SetProgress',
                                        SetKey(Value=0),
                                        transitions={'done': 'Count instances WHILE Turning360'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'Key': 'progress'})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
