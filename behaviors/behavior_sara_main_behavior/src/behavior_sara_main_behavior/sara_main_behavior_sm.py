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
from sara_flexbe_states.FOR_loop import ForState
from flexbe_states.calculation_state import CalculationState
from behavior_go_to_exit.go_to_exit_sm import Go_to_exitSM
from behavior_sara_action_executor.sara_action_executor_sm import SaraactionexecutorSM
from flexbe_states.subscriber_state import SubscriberState
from flexbe_states.check_condition_state import CheckConditionState
from flexbe_states.wait_state import WaitState
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.FIFO_New import FIFO_New
from behavior_init_sequence.init_sequence_sm import Init_SequenceSM
from behavior_new_qualif.new_qualif_sm import NewqualifSM
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
		self.add_parameter('ActionTopic', 'sara_action')

		# references to used behaviors
		self.add_behavior(sara_command_managerSM, 'Sara parallel Runtime/Sara brain/sara_command_manager')
		self.add_behavior(Go_to_exitSM, 'Sara parallel Runtime/Sara brain/Go_to_exit')
		self.add_behavior(SaraactionexecutorSM, 'Sara parallel Runtime/Sara action executor/Sara action executor')
		self.add_behavior(Init_SequenceSM, 'Init_Sequence')
		self.add_behavior(NewqualifSM, 'New qualif')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
        
        # [/MANUAL_INIT]

		# Behavior comments:

		# ! 676 291 /Sara parallel Runtime/Shutdown conditions checker
		# true=RUN|nfalse=STOP



	def create(self):
		# x:914 y:505, x:574 y:74
		_state_machine = OperatableStateMachine(outcomes=['Shutdown', 'Failed'])
		_state_machine.userdata.Command = "no nothing"
		_state_machine.userdata.End = False

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

		# x:693 y:298
		_sm_stopped_mode_0 = PriorityContainer(outcomes=['finished'])

		with _sm_stopped_mode_0:
			# x:64 y:117
			OperatableStateMachine.add('oups',
										SaraSay(sentence="Oh! You pushed my stop button", emotion=1),
										transitions={'done': 'wait for true'},
										autonomy={'done': Autonomy.Off})

			# x:236 y:179
			OperatableStateMachine.add('wait for true',
										SubscriberState(topic="/estop_status", blocking=True, clear=False),
										transitions={'received': 'condition', 'unavailable': 'wait for true'},
										autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
										remapping={'message': 'message'})

			# x:456 y:242
			OperatableStateMachine.add('condition',
										CheckConditionState(predicate=lambda x: x.data),
										transitions={'true': 'finished', 'false': 'wait for true'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'message'})


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


		# x:212 y:285
		_sm_estop_2 = OperatableStateMachine(outcomes=['shutdown'])

		with _sm_estop_2:
			# x:164 y:122
			OperatableStateMachine.add('EStop Subscriber',
										SubscriberState(topic="/estop_status", blocking=True, clear=False),
										transitions={'received': 'EStop State', 'unavailable': 'shutdown'},
										autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
										remapping={'message': 'message'})

			# x:467 y:342
			OperatableStateMachine.add('EStop State',
										CheckConditionState(predicate=lambda x: x.data),
										transitions={'true': 'wait', 'false': 'Stopped mode'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'message'})

			# x:645 y:57
			OperatableStateMachine.add('wait',
										WaitState(wait_time=0.1),
										transitions={'done': 'EStop Subscriber'},
										autonomy={'done': Autonomy.Off})

			# x:812 y:242
			OperatableStateMachine.add('Stopped mode',
										_sm_stopped_mode_0,
										transitions={'finished': 'wait'},
										autonomy={'finished': Autonomy.Inherit})


		# x:841 y:231
		_sm_sara_action_executor_3 = OperatableStateMachine(outcomes=['shutdown'], input_keys=['HighFIFO', 'MedFIFO', 'LowFIFO', 'DoNow', 'End'])

		with _sm_sara_action_executor_3:
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
										remapping={'HighFIFO': 'HighFIFO', 'MedFIFO': 'MedFIFO', 'LowFIFO': 'LowFIFO', 'End': 'End'})


		# x:887 y:420
		_sm_sara_brain_4 = OperatableStateMachine(outcomes=['error'], input_keys=['HighFIFO', 'LowFIFO', 'MedFIFO', 'DoNow', 'End'])

		with _sm_sara_brain_4:
			# x:270 y:346
			OperatableStateMachine.add('sara_command_manager',
										self.use_behavior(sara_command_managerSM, 'Sara parallel Runtime/Sara brain/sara_command_manager'),
										transitions={'finished': 'For loop', 'failed': 'error'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'HighFIFO': 'HighFIFO', 'MedFIFO': 'MedFIFO', 'LowFIFO': 'LowFIFO', 'DoNow': 'DoNow'})

			# x:599 y:251
			OperatableStateMachine.add('For loop',
										ForState(repeat=3),
										transitions={'do': 'sara_command_manager', 'end': 'set end'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index'})

			# x:725 y:305
			OperatableStateMachine.add('set end',
										CalculationState(calculation=lambda x: True),
										transitions={'done': 'Go_to_exit'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'End', 'output_value': 'End'})

			# x:856 y:167
			OperatableStateMachine.add('Go_to_exit',
										self.use_behavior(Go_to_exitSM, 'Sara parallel Runtime/Sara brain/Go_to_exit'),
										transitions={'finished': 'error', 'failed': 'error'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})


		# x:30 y:322
		_sm_sara_shutdown_5 = OperatableStateMachine(outcomes=['finished'])

		with _sm_sara_shutdown_5:
			# x:57 y:86
			OperatableStateMachine.add('log',
										LogState(text="shutdown", severity=Logger.REPORT_HINT),
										transitions={'done': 'say'},
										autonomy={'done': Autonomy.Off})

			# x:122 y:228
			OperatableStateMachine.add('say',
										SaraSay(sentence="I'm goint to shutdown for safetiy reasons", emotion=1),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		# x:291 y:514, x:284 y:353, x:276 y:271, x:286 y:427, x:1050 y:76
		_sm_sara_parallel_runtime_6 = ConcurrencyContainer(outcomes=['Shutdown'], input_keys=['HighFIFO', 'MedFIFO', 'LowFIFO', 'DoNow', 'End'], conditions=[
										('Shutdown', [('Estop', 'shutdown')]),
										('Shutdown', [('Sara brain', 'error')]),
										('Shutdown', [('Sara move head', 'error')]),
										('Shutdown', [('Sara action executor', 'shutdown')])
										])

		with _sm_sara_parallel_runtime_6:
			# x:57 y:333
			OperatableStateMachine.add('Sara brain',
										_sm_sara_brain_4,
										transitions={'error': 'Shutdown'},
										autonomy={'error': Autonomy.Inherit},
										remapping={'HighFIFO': 'HighFIFO', 'LowFIFO': 'LowFIFO', 'MedFIFO': 'MedFIFO', 'DoNow': 'DoNow', 'End': 'End'})

			# x:52 y:416
			OperatableStateMachine.add('Sara action executor',
										_sm_sara_action_executor_3,
										transitions={'shutdown': 'Shutdown'},
										autonomy={'shutdown': Autonomy.Inherit},
										remapping={'HighFIFO': 'HighFIFO', 'MedFIFO': 'MedFIFO', 'LowFIFO': 'LowFIFO', 'DoNow': 'DoNow', 'End': 'End'})

			# x:50 y:498
			OperatableStateMachine.add('Estop',
										_sm_estop_2,
										transitions={'shutdown': 'Shutdown'},
										autonomy={'shutdown': Autonomy.Inherit})

			# x:55 y:253
			OperatableStateMachine.add('Sara move head',
										_sm_sara_move_head_1,
										transitions={'error': 'Shutdown'},
										autonomy={'error': Autonomy.Inherit})



		with _state_machine:
			# x:69 y:66
			OperatableStateMachine.add('log',
										LogState(text="Start Sara", severity=Logger.REPORT_HINT),
										transitions={'done': 'New qualif'},
										autonomy={'done': Autonomy.Off})

			# x:448 y:483
			OperatableStateMachine.add('Sara parallel Runtime',
										_sm_sara_parallel_runtime_6,
										transitions={'Shutdown': 'Sara shutdown'},
										autonomy={'Shutdown': Autonomy.Inherit},
										remapping={'HighFIFO': 'HighFIFO', 'MedFIFO': 'MedFIFO', 'LowFIFO': 'LowFIFO', 'DoNow': 'DoNow', 'End': 'End'})

			# x:701 y:485
			OperatableStateMachine.add('Sara shutdown',
										_sm_sara_shutdown_5,
										transitions={'finished': 'Shutdown'},
										autonomy={'finished': Autonomy.Inherit})

			# x:236 y:191
			OperatableStateMachine.add('Create HighFIFO',
										FIFO_New(),
										transitions={'done': 'Create MedFIFO'},
										autonomy={'done': Autonomy.Off},
										remapping={'FIFO': 'HighFIFO'})

			# x:233 y:265
			OperatableStateMachine.add('Create MedFIFO',
										FIFO_New(),
										transitions={'done': 'Create LowFIFO'},
										autonomy={'done': Autonomy.Off},
										remapping={'FIFO': 'MedFIFO'})

			# x:233 y:340
			OperatableStateMachine.add('Create LowFIFO',
										FIFO_New(),
										transitions={'done': 'Create DoNow'},
										autonomy={'done': Autonomy.Off},
										remapping={'FIFO': 'LowFIFO'})

			# x:237 y:411
			OperatableStateMachine.add('Create DoNow',
										FIFO_New(),
										transitions={'done': 'Sara parallel Runtime'},
										autonomy={'done': Autonomy.Off},
										remapping={'FIFO': 'DoNow'})

			# x:324 y:99
			OperatableStateMachine.add('Init_Sequence',
										self.use_behavior(Init_SequenceSM, 'Init_Sequence'),
										transitions={'finished': 'Create HighFIFO', 'failed': 'Failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:157 y:67
			OperatableStateMachine.add('New qualif',
										self.use_behavior(NewqualifSM, 'New qualif'),
										transitions={'finished': 'Init_Sequence', 'failed': 'Failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
