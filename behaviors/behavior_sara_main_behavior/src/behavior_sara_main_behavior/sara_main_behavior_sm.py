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


        # x:30 y:308, x:130 y:308
        _sm_sara_move_to_1 = OperatableStateMachine(outcomes=['finished', 'failed'])

        with _sm_sara_move_to_1:
            # x:77 y:140
            OperatableStateMachine.add('log',
                                        LogState(text="Move to", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off})


        # x:990 y:195
        _sm_estop_2 = OperatableStateMachine(outcomes=['Fail'])

        with _sm_estop_2:
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
        _sm_shutdown_conditions_checker_3 = OperatableStateMachine(outcomes=['shutdown'])

        with _sm_shutdown_conditions_checker_3:
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


        # x:926 y:568
        _sm_sara_action_executor_4 = OperatableStateMachine(outcomes=['critical fail'])

        with _sm_sara_action_executor_4:
            # x:39 y:151
            OperatableStateMachine.add('log',
                                        LogState(text="Start action executor", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'Sara move to'},
                                        autonomy={'done': Autonomy.Off})

            # x:507 y:146
            OperatableStateMachine.add('wait',
                                        WaitState(wait_time=50),
                                        transitions={'done': 'fail'},
                                        autonomy={'done': Autonomy.Off})

            # x:805 y:501
            OperatableStateMachine.add('fail',
                                        LogState(text="Critical fail in action executer!", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'critical fail'},
                                        autonomy={'done': Autonomy.Off})

            # x:229 y:138
            OperatableStateMachine.add('Sara move to',
                                        _sm_sara_move_to_1,
                                        transitions={'finished': 'wait', 'failed': 'critical fail'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})


        # x:646 y:55
        _sm_sara_brain_5 = OperatableStateMachine(outcomes=['error'])

        with _sm_sara_brain_5:
            # x:136 y:49
            OperatableStateMachine.add('log',
                                        LogState(text="Start brain", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'dumb wait until dead brain'},
                                        autonomy={'done': Autonomy.Off})

            # x:390 y:50
            OperatableStateMachine.add('dumb wait until dead brain',
                                        WaitState(wait_time=1000000),
                                        transitions={'done': 'error'},
                                        autonomy={'done': Autonomy.Off})


        # x:30 y:322
        _sm_sara_shutdown_6 = OperatableStateMachine(outcomes=['finished'])

        with _sm_sara_shutdown_6:
            # x:57 y:86
            OperatableStateMachine.add('log',
                                        LogState(text="shutdown", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off})


        # x:30 y:322, x:130 y:322
        _sm_sara_init_7 = OperatableStateMachine(outcomes=['finished', 'failed'])

        with _sm_sara_init_7:
            # x:56 y:144
            OperatableStateMachine.add('log',
                                        LogState(text="initialisation", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off})


        # x:965 y:435, x:380 y:496, x:268 y:350, x:245 y:569, x:1090 y:556
        _sm_sara_parallel_runtime_8 = ConcurrencyContainer(outcomes=['Shutdown'], conditions=[
                                        ('Shutdown', [('Sara action executor', 'critical fail')]),
                                        ('Shutdown', [('Shutdown conditions checker', 'shutdown')]),
                                        ('Shutdown', [('Sara brain', 'error')]),
                                        ('Shutdown', [('EStop', 'Fail')])
                                        ])

        with _sm_sara_parallel_runtime_8:
            # x:49 y:338
            OperatableStateMachine.add('Sara brain',
                                        _sm_sara_brain_5,
                                        transitions={'error': 'Shutdown'},
                                        autonomy={'error': Autonomy.Inherit})

            # x:52 y:416
            OperatableStateMachine.add('Sara action executor',
                                        _sm_sara_action_executor_4,
                                        transitions={'critical fail': 'Shutdown'},
                                        autonomy={'critical fail': Autonomy.Inherit})

            # x:50 y:487
            OperatableStateMachine.add('Shutdown conditions checker',
                                        _sm_shutdown_conditions_checker_3,
                                        transitions={'shutdown': 'Shutdown'},
                                        autonomy={'shutdown': Autonomy.Inherit})

            # x:52 y:561
            OperatableStateMachine.add('EStop',
                                        _sm_estop_2,
                                        transitions={'Fail': 'Shutdown'},
                                        autonomy={'Fail': Autonomy.Inherit})



        with _state_machine:
            # x:63 y:223
            OperatableStateMachine.add('log',
                                        LogState(text="Start Sara", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'Sara init'},
                                        autonomy={'done': Autonomy.Off})

            # x:397 y:99
            OperatableStateMachine.add('Sara parallel Runtime',
                                        _sm_sara_parallel_runtime_8,
                                        transitions={'Shutdown': 'Sara shutdown'},
                                        autonomy={'Shutdown': Autonomy.Inherit})

            # x:225 y:210
            OperatableStateMachine.add('Sara init',
                                        _sm_sara_init_7,
                                        transitions={'finished': 'Sara parallel Runtime', 'failed': 'Shutdown'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

            # x:668 y:99
            OperatableStateMachine.add('Sara shutdown',
                                        _sm_sara_shutdown_6,
                                        transitions={'finished': 'Shutdown'},
                                        autonomy={'finished': Autonomy.Inherit})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
