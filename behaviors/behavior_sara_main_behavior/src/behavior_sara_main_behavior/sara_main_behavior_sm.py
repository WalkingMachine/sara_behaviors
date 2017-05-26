#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_sara_main_behavior')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.log_state import LogState
from sara_flexbe_states.speech_to_text import SpeechToText
from flexbe_states.log_key_state import LogKeyState
from flexbe_states.decision_state import DecisionState
from flexbe_states.wait_state import WaitState
from flexbe_states.subscriber_state import SubscriberState
from flexbe_states.check_condition_state import CheckConditionState
from flexbe_states.calculation_state import CalculationState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sun May 21 2017
@author: Philippe La Madeleine
'''
class Sara_main_behaviorSM(Behavior):
    '''
    Main behavior or Sara the robot
    '''


    def __init__(self):
        super(Sara_main_behaviorSM, self).__init__()
        self.name = 'Sara_main_behavior'

        # parameters of this behavior
        self.add_parameter('EStopTopic', '"/EStop"')
        self.add_parameter('ActionTopic', '"action_topic"')

        # references to used behaviors

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
        
        # [/MANUAL_INIT]

        # Behavior comments:

        # ! 318 82 /Sara parallel Runtime/Shutdown conditions checker
        # true=shutdown behavior



    def create(self):
        # x:900 y:215
        _state_machine = OperatableStateMachine(outcomes=['Shutdown'])
        _state_machine.userdata.EStopStatus = False
        _state_machine.userdata.Command = "no nothing"

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

        # x:921 y:71, x:922 y:175
        _sm_stop_0 = PriorityContainer(outcomes=['OK', 'Fail'])

        with _sm_stop_0:
            # x:88 y:71
            OperatableStateMachine.add('log1',
                                        LogState(text="EStop activated!", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'sub'},
                                        autonomy={'done': Autonomy.Off})

            # x:704 y:64
            OperatableStateMachine.add('cond',
                                        CheckConditionState(predicate=lambda x: x),
                                        transitions={'true': 'wait1', 'false': 'OK'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                        remapping={'input_value': 'EStopStatus'})

            # x:505 y:198
            OperatableStateMachine.add('wait1',
                                        WaitState(wait_time=1),
                                        transitions={'done': 'sub'},
                                        autonomy={'done': Autonomy.Off})

            # x:741 y:160
            OperatableStateMachine.add('log',
                                        LogState(text="No EStop Topic found", severity=Logger.REPORT_ERROR),
                                        transitions={'done': 'Fail'},
                                        autonomy={'done': Autonomy.Off})

            # x:505 y:28
            OperatableStateMachine.add('calc',
                                        CalculationState(calculation=lambda x: x.data),
                                        transitions={'done': 'cond'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'input_value': 'EStopMessage', 'output_value': 'EStopStatus'})

            # x:254 y:73
            OperatableStateMachine.add('sub',
                                        SubscriberState(topic=self.EStopTopic, blocking=True, clear=True),
                                        transitions={'received': 'calc', 'unavailable': 'log'},
                                        autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
                                        remapping={'message': 'EStopMessage'})


        # x:556 y:399, x:627 y:351, x:697 y:292
        _sm_sara_take_this_1 = OperatableStateMachine(outcomes=['Success', 'fail', 'critical fail'])

        with _sm_sara_take_this_1:
            # x:125 y:30
            OperatableStateMachine.add('wait',
                                        WaitState(wait_time=5),
                                        transitions={'done': 'ff'},
                                        autonomy={'done': Autonomy.Off})

            # x:106 y:187
            OperatableStateMachine.add('f',
                                        DecisionState(outcomes=["1","2","3"], conditions=lambda x: x),
                                        transitions={'1': 'Success', '2': 'fail', '3': 'critical fail'},
                                        autonomy={'1': Autonomy.Off, '2': Autonomy.Off, '3': Autonomy.Off},
                                        remapping={'input_value': 'message'})

            # x:235 y:99
            OperatableStateMachine.add('ff',
                                        SubscriberState(topic="/r", blocking=True, clear=False),
                                        transitions={'received': 'f', 'unavailable': 'Success'},
                                        autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
                                        remapping={'message': 'message'})


        # x:30 y:308, x:230 y:322, x:230 y:322
        _sm_sara_go_here_2 = OperatableStateMachine(outcomes=['finished', 'critical fail', 'fail'])

        with _sm_sara_go_here_2:
            # x:77 y:140
            OperatableStateMachine.add('log',
                                        LogState(text="Move to", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off})


        # x:407 y:328
        _sm_sara_sorry_3 = OperatableStateMachine(outcomes=['finished'])

        with _sm_sara_sorry_3:
            # x:201 y:153
            OperatableStateMachine.add('log',
                                        LogState(text="Sorry, I failed  :(", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off})


        # x:426 y:328
        _sm_sara_succes_4 = OperatableStateMachine(outcomes=['finished'])

        with _sm_sara_succes_4:
            # x:148 y:154
            OperatableStateMachine.add('log',
                                        LogState(text="success", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off})


        # x:298 y:252
        _sm_call_for_orders_5 = OperatableStateMachine(outcomes=['finished'])

        with _sm_call_for_orders_5:
            # x:104 y:131
            OperatableStateMachine.add('log',
                                        LogState(text="call for order", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off})


        # x:616 y:135
        _sm_sara_move_head_6 = OperatableStateMachine(outcomes=['error'])

        with _sm_sara_move_head_6:
            # x:145 y:117
            OperatableStateMachine.add('log',
                                        LogState(text="move head", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'wait'},
                                        autonomy={'done': Autonomy.Off})

            # x:328 y:116
            OperatableStateMachine.add('wait',
                                        WaitState(wait_time=1000000),
                                        transitions={'done': 'error'},
                                        autonomy={'done': Autonomy.Low})


        # x:990 y:195
        _sm_estop_7 = OperatableStateMachine(outcomes=['Fail'])

        with _sm_estop_7:
            # x:112 y:183
            OperatableStateMachine.add('sub',
                                        SubscriberState(topic=self.EStopTopic, blocking=True, clear=True),
                                        transitions={'received': 'setEStopStatus', 'unavailable': 'Stop'},
                                        autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Low},
                                        remapping={'message': 'EStopMessage'})

            # x:524 y:120
            OperatableStateMachine.add('cond',
                                        CheckConditionState(predicate=lambda x: x),
                                        transitions={'true': 'Stop', 'false': 'wait2'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                        remapping={'input_value': 'EStopStatus'})

            # x:768 y:179
            OperatableStateMachine.add('Stop',
                                        _sm_stop_0,
                                        transitions={'OK': 'wait1', 'Fail': 'Fail'},
                                        autonomy={'OK': Autonomy.Inherit, 'Fail': Autonomy.Inherit})

            # x:430 y:253
            OperatableStateMachine.add('wait1',
                                        WaitState(wait_time=1),
                                        transitions={'done': 'sub'},
                                        autonomy={'done': Autonomy.Off})

            # x:347 y:32
            OperatableStateMachine.add('wait2',
                                        WaitState(wait_time=0.1),
                                        transitions={'done': 'sub'},
                                        autonomy={'done': Autonomy.Off})

            # x:333 y:125
            OperatableStateMachine.add('setEStopStatus',
                                        CalculationState(calculation=lambda x: x.data),
                                        transitions={'done': 'cond'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'input_value': 'EStopMessage', 'output_value': 'EStopStatus'})


        # x:852 y:132
        _sm_shutdown_conditions_checker_8 = OperatableStateMachine(outcomes=['shutdown'])

        with _sm_shutdown_conditions_checker_8:
            # x:93 y:121
            OperatableStateMachine.add('sub',
                                        SubscriberState(topic="/shutdown", blocking=True, clear=True),
                                        transitions={'received': 'con', 'unavailable': 'shutdown'},
                                        autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Low},
                                        remapping={'message': 'message'})

            # x:326 y:177
            OperatableStateMachine.add('con',
                                        CheckConditionState(predicate=lambda x: x.data),
                                        transitions={'true': 'log', 'false': 'sub'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                        remapping={'input_value': 'message'})

            # x:584 y:175
            OperatableStateMachine.add('log',
                                        LogState(text="shutdown command detected", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'shutdown'},
                                        autonomy={'done': Autonomy.Off})


        # x:1229 y:464
        _sm_sara_action_executor_9 = OperatableStateMachine(outcomes=['critical fail'])

        with _sm_sara_action_executor_9:
            # x:17 y:247
            OperatableStateMachine.add('log',
                                        LogState(text="Start action executor", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'Call for orders'},
                                        autonomy={'done': Autonomy.Off})

            # x:1176 y:389
            OperatableStateMachine.add('Critical failure',
                                        LogState(text="Critical fail in action executer!", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'critical fail'},
                                        autonomy={'done': Autonomy.Off})

            # x:340 y:241
            OperatableStateMachine.add('decision',
                                        DecisionState(outcomes=["nothing", "go", "take"], conditions=lambda x: x),
                                        transitions={'nothing': 'sub', 'go': 'Sara go here', 'take': 'Sara take this'},
                                        autonomy={'nothing': Autonomy.Off, 'go': Autonomy.Off, 'take': Autonomy.Off},
                                        remapping={'input_value': 'message'})

            # x:14 y:570
            OperatableStateMachine.add('Call for orders',
                                        _sm_call_for_orders_5,
                                        transitions={'finished': 'sub'},
                                        autonomy={'finished': Autonomy.Inherit})

            # x:1070 y:490
            OperatableStateMachine.add('Sara succes',
                                        _sm_sara_succes_4,
                                        transitions={'finished': 'Call for orders'},
                                        autonomy={'finished': Autonomy.Inherit})

            # x:1022 y:570
            OperatableStateMachine.add('Sara sorry',
                                        _sm_sara_sorry_3,
                                        transitions={'finished': 'Call for orders'},
                                        autonomy={'finished': Autonomy.Inherit})

            # x:579 y:19
            OperatableStateMachine.add('Sara go here',
                                        _sm_sara_go_here_2,
                                        transitions={'finished': 'Sara succes', 'critical fail': 'Critical failure', 'fail': 'Sara sorry'},
                                        autonomy={'finished': Autonomy.Inherit, 'critical fail': Autonomy.Inherit, 'fail': Autonomy.Inherit})

            # x:580 y:119
            OperatableStateMachine.add('Sara take this',
                                        _sm_sara_take_this_1,
                                        transitions={'Success': 'Sara succes', 'fail': 'Sara sorry', 'critical fail': 'Critical failure'},
                                        autonomy={'Success': Autonomy.Inherit, 'fail': Autonomy.Inherit, 'critical fail': Autonomy.Inherit})

            # x:125 y:294
            OperatableStateMachine.add('sub',
                                        SubscriberState(topic=self.ActionTopic, blocking=True, clear=False),
                                        transitions={'received': 'decision', 'unavailable': 'critical fail'},
                                        autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
                                        remapping={'message': 'message'})


        # x:468 y:131
        _sm_sara_brain_10 = OperatableStateMachine(outcomes=['error'])

        with _sm_sara_brain_10:
            # x:136 y:49
            OperatableStateMachine.add('log',
                                        LogState(text="Start brain", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'get command'},
                                        autonomy={'done': Autonomy.Off})

            # x:274 y:53
            OperatableStateMachine.add('get command',
                                        SpeechToText(),
                                        transitions={'done': 'log2', 'failed': 'error'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Low},
                                        remapping={'words': 'Command'})

            # x:469 y:31
            OperatableStateMachine.add('log2',
                                        LogKeyState(text=lambda x: x, severity=Logger.REPORT_HINT),
                                        transitions={'done': 'get command'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'data': 'Command'})


        # x:30 y:322
        _sm_sara_shutdown_11 = OperatableStateMachine(outcomes=['finished'])

        with _sm_sara_shutdown_11:
            # x:57 y:86
            OperatableStateMachine.add('log',
                                        LogState(text="shutdown", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off})


        # x:30 y:322, x:130 y:322
        _sm_sara_init_12 = OperatableStateMachine(outcomes=['finished', 'failed'])

        with _sm_sara_init_12:
            # x:56 y:144
            OperatableStateMachine.add('log',
                                        LogState(text="initialisation", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off})


        # x:350 y:430, x:374 y:518, x:239 y:353, x:275 y:580, x:1050 y:76, x:1202 y:605
        _sm_sara_parallel_runtime_13 = ConcurrencyContainer(outcomes=['Shutdown'], conditions=[
                                        ('Shutdown', [('Sara action executor', 'critical fail')]),
                                        ('Shutdown', [('Shutdown conditions checker', 'shutdown')]),
                                        ('Shutdown', [('Sara brain', 'error')]),
                                        ('Shutdown', [('EStop', 'Fail')]),
                                        ('Shutdown', [('Sara move head', 'error')])
                                        ])

        with _sm_sara_parallel_runtime_13:
            # x:52 y:341
            OperatableStateMachine.add('Sara brain',
                                        _sm_sara_brain_10,
                                        transitions={'error': 'Shutdown'},
                                        autonomy={'error': Autonomy.Inherit})

            # x:52 y:416
            OperatableStateMachine.add('Sara action executor',
                                        _sm_sara_action_executor_9,
                                        transitions={'critical fail': 'Shutdown'},
                                        autonomy={'critical fail': Autonomy.Inherit})

            # x:50 y:487
            OperatableStateMachine.add('Shutdown conditions checker',
                                        _sm_shutdown_conditions_checker_8,
                                        transitions={'shutdown': 'Shutdown'},
                                        autonomy={'shutdown': Autonomy.Inherit})

            # x:52 y:561
            OperatableStateMachine.add('EStop',
                                        _sm_estop_7,
                                        transitions={'Fail': 'Shutdown'},
                                        autonomy={'Fail': Autonomy.Inherit})

            # x:802 y:69
            OperatableStateMachine.add('Sara move head',
                                        _sm_sara_move_head_6,
                                        transitions={'error': 'Shutdown'},
                                        autonomy={'error': Autonomy.Inherit})



        with _state_machine:
            # x:60 y:213
            OperatableStateMachine.add('log',
                                        LogState(text="Start Sara", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'Sara init'},
                                        autonomy={'done': Autonomy.Off})

            # x:397 y:99
            OperatableStateMachine.add('Sara parallel Runtime',
                                        _sm_sara_parallel_runtime_13,
                                        transitions={'Shutdown': 'Sara shutdown'},
                                        autonomy={'Shutdown': Autonomy.Inherit})

            # x:225 y:210
            OperatableStateMachine.add('Sara init',
                                        _sm_sara_init_12,
                                        transitions={'finished': 'Sara parallel Runtime', 'failed': 'Shutdown'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

            # x:668 y:99
            OperatableStateMachine.add('Sara shutdown',
                                        _sm_sara_shutdown_11,
                                        transitions={'finished': 'Shutdown'},
                                        autonomy={'finished': Autonomy.Inherit})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
