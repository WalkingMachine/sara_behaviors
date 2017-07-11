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
from behavior_sara_command_manager.sara_command_manager_sm import sara_command_managerSM
from behavior_sara_action_executor.sara_action_executor_sm import SaraactionexecutorSM
from behavior_testbooltopic.testbooltopic_sm import TestBoolTopicSM
from flexbe_states.wait_state import WaitState
from flexbe_states.check_condition_state import CheckConditionState
from flexbe_states.calculation_state import CalculationState
from flexbe_states.subscriber_state import SubscriberState
from sara_flexbe_states.FIFO_New import FIFO_New
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
        self.add_parameter('ShutdownTopic', '/shutdown')
        self.add_parameter('EStopTopic', '/e_stop')
        self.add_parameter('ActionTopic', 'sara_action')

        # references to used behaviors
        self.add_behavior(sara_command_managerSM, 'Sara parallel Runtime/Sara brain/sara_command_manager')
        self.add_behavior(SaraactionexecutorSM, 'Sara parallel Runtime/Sara action executor/Sara action executor')
        self.add_behavior(TestBoolTopicSM, 'Sara parallel Runtime/Shutdown conditions checker/TestBoolTopic')
        self.add_behavior(TestBoolTopicSM, 'Sara parallel Runtime/EStop/TestBoolTopic')

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
        
        # [/MANUAL_INIT]

        # Behavior comments:

        # ! 388 146 /Sara parallel Runtime/Shutdown conditions checker
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


        # x:616 y:135
        _sm_sara_move_head_1 = OperatableStateMachine(outcomes=['error'])

        with _sm_sara_move_head_1:
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
        _sm_estop_2 = OperatableStateMachine(outcomes=['Fail'])

        with _sm_estop_2:
            # x:84 y:110
            OperatableStateMachine.add('TestBoolTopic',
                                        self.use_behavior(TestBoolTopicSM, 'Sara parallel Runtime/EStop/TestBoolTopic'),
                                        transitions={'True': 'Stop', 'False': 'TestBoolTopic'},
                                        autonomy={'True': Autonomy.Inherit, 'False': Autonomy.Inherit})

            # x:430 y:253
            OperatableStateMachine.add('wait1',
                                        WaitState(wait_time=1),
                                        transitions={'done': 'TestBoolTopic'},
                                        autonomy={'done': Autonomy.Off})

            # x:768 y:179
            OperatableStateMachine.add('Stop',
                                        _sm_stop_0,
                                        transitions={'OK': 'wait1', 'Fail': 'Fail'},
                                        autonomy={'OK': Autonomy.Inherit, 'Fail': Autonomy.Inherit})


        # x:852 y:132
        _sm_shutdown_conditions_checker_3 = OperatableStateMachine(outcomes=['shutdown'])

        with _sm_shutdown_conditions_checker_3:
            # x:200 y:171
            OperatableStateMachine.add('TestBoolTopic',
                                        self.use_behavior(TestBoolTopicSM, 'Sara parallel Runtime/Shutdown conditions checker/TestBoolTopic'),
                                        transitions={'True': 'log', 'False': 'TestBoolTopic'},
                                        autonomy={'True': Autonomy.Inherit, 'False': Autonomy.Inherit})

            # x:584 y:175
            OperatableStateMachine.add('log',
                                        LogState(text="shutdown command detected", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'shutdown'},
                                        autonomy={'done': Autonomy.Off})


        # x:841 y:231
        _sm_sara_action_executor_4 = OperatableStateMachine(outcomes=['shutdown'], input_keys=['HighFIFO', 'MedFIFO', 'LowFIFO', 'DoNow'])

        with _sm_sara_action_executor_4:
            # x:128 y:134
            OperatableStateMachine.add('log',
                                        LogState(text="Start action executor", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'Sara action executor'},
                                        autonomy={'done': Autonomy.Off})

            # x:636 y:111
            OperatableStateMachine.add('Critical failure',
                                        LogState(text="Critical fail in action executer!", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'shutdown'},
                                        autonomy={'done': Autonomy.Off})

            # x:366 y:149
            OperatableStateMachine.add('Sara action executor',
                                        self.use_behavior(SaraactionexecutorSM, 'Sara parallel Runtime/Sara action executor/Sara action executor'),
                                        transitions={'CriticalFail': 'Critical failure', 'Shutdown': 'shutdown'},
                                        autonomy={'CriticalFail': Autonomy.Inherit, 'Shutdown': Autonomy.Inherit},
                                        remapping={'HighFIFO': 'HighFIFO', 'MedFIFO': 'MedFIFO', 'LowFIFO': 'LowFIFO'})


        # x:887 y:420
        _sm_sara_brain_5 = OperatableStateMachine(outcomes=['error'], input_keys=['HighFIFO', 'LowFIFO', 'MedFIFO', 'DoNow'])

        with _sm_sara_brain_5:
            # x:270 y:346
            OperatableStateMachine.add('sara_command_manager',
                                        self.use_behavior(sara_command_managerSM, 'Sara parallel Runtime/Sara brain/sara_command_manager'),
                                        transitions={'finished': 'sara_command_manager', 'failed': 'error'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'HighFIFO': 'HighFIFO', 'MedFIFO': 'MedFIFO', 'LowFIFO': 'LowFIFO', 'DoNow': 'DoNow'})


        # x:30 y:322
        _sm_sara_shutdown_6 = OperatableStateMachine(outcomes=['finished'])

        with _sm_sara_shutdown_6:
            # x:57 y:86
            OperatableStateMachine.add('log',
                                        LogState(text="shutdown", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off})


        # x:57 y:485, x:182 y:508
        _sm_sara_init_7 = OperatableStateMachine(outcomes=['finished', 'failed'])

        with _sm_sara_init_7:
            # x:56 y:144
            OperatableStateMachine.add('log',
                                        LogState(text="initialisation", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off})


        # x:334 y:507, x:284 y:361, x:208 y:587, x:294 y:269, x:1050 y:76, x:1202 y:605
        _sm_sara_parallel_runtime_8 = ConcurrencyContainer(outcomes=['Shutdown'], input_keys=['HighFIFO', 'MedFIFO', 'LowFIFO', 'DoNow'], conditions=[
                                        ('Shutdown', [('Shutdown conditions checker', 'shutdown')]),
                                        ('Shutdown', [('Sara brain', 'error')]),
                                        ('Shutdown', [('EStop', 'Fail')]),
                                        ('Shutdown', [('Sara move head', 'error')]),
                                        ('Shutdown', [('Sara action executor', 'shutdown')])
                                        ])

        with _sm_sara_parallel_runtime_8:
            # x:59 y:335
            OperatableStateMachine.add('Sara brain',
                                        _sm_sara_brain_5,
                                        transitions={'error': 'Shutdown'},
                                        autonomy={'error': Autonomy.Inherit},
                                        remapping={'HighFIFO': 'HighFIFO', 'LowFIFO': 'LowFIFO', 'MedFIFO': 'MedFIFO', 'DoNow': 'DoNow'})

            # x:52 y:416
            OperatableStateMachine.add('Sara action executor',
                                        _sm_sara_action_executor_4,
                                        transitions={'shutdown': 'Shutdown'},
                                        autonomy={'shutdown': Autonomy.Inherit},
                                        remapping={'HighFIFO': 'HighFIFO', 'MedFIFO': 'MedFIFO', 'LowFIFO': 'LowFIFO', 'DoNow': 'DoNow'})

            # x:50 y:498
            OperatableStateMachine.add('Shutdown conditions checker',
                                        _sm_shutdown_conditions_checker_3,
                                        transitions={'shutdown': 'Shutdown'},
                                        autonomy={'shutdown': Autonomy.Inherit})

            # x:52 y:561
            OperatableStateMachine.add('EStop',
                                        _sm_estop_2,
                                        transitions={'Fail': 'Shutdown'},
                                        autonomy={'Fail': Autonomy.Inherit})

            # x:55 y:253
            OperatableStateMachine.add('Sara move head',
                                        _sm_sara_move_head_1,
                                        transitions={'error': 'Shutdown'},
                                        autonomy={'error': Autonomy.Inherit})



        with _state_machine:
            # x:60 y:213
            OperatableStateMachine.add('log',
                                        LogState(text="Start Sara", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'Sara init'},
                                        autonomy={'done': Autonomy.Off})

            # x:402 y:499
            OperatableStateMachine.add('Sara parallel Runtime',
                                        _sm_sara_parallel_runtime_8,
                                        transitions={'Shutdown': 'Sara shutdown'},
                                        autonomy={'Shutdown': Autonomy.Inherit},
                                        remapping={'HighFIFO': 'HighFIFO', 'MedFIFO': 'MedFIFO', 'LowFIFO': 'LowFIFO', 'DoNow': 'DoNow'})

            # x:225 y:210
            OperatableStateMachine.add('Sara init',
                                        _sm_sara_init_7,
                                        transitions={'finished': 'Create HighFIFO', 'failed': 'Shutdown'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

            # x:638 y:451
            OperatableStateMachine.add('Sara shutdown',
                                        _sm_sara_shutdown_6,
                                        transitions={'finished': 'Shutdown'},
                                        autonomy={'finished': Autonomy.Inherit})

            # x:227 y:326
            OperatableStateMachine.add('Create HighFIFO',
                                        FIFO_New(),
                                        transitions={'done': 'Create MedFIFO'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'FIFO': 'HighFIFO'})

            # x:226 y:392
            OperatableStateMachine.add('Create MedFIFO',
                                        FIFO_New(),
                                        transitions={'done': 'Create LowFIFO'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'FIFO': 'MedFIFO'})

            # x:226 y:459
            OperatableStateMachine.add('Create LowFIFO',
                                        FIFO_New(),
                                        transitions={'done': 'Create DoNow'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'FIFO': 'LowFIFO'})

            # x:228 y:515
            OperatableStateMachine.add('Create DoNow',
                                        FIFO_New(),
                                        transitions={'done': 'Sara parallel Runtime'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'FIFO': 'DoNow'})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
