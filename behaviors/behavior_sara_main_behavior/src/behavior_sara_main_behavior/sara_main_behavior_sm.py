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
from sara_flexbe_states.for_loop import ForLoop
from flexbe_states.calculation_state import CalculationState
from behavior_sara_action_executor.sara_action_executor_sm import SaraactionexecutorSM
from sara_flexbe_states.sara_say import SaraSay
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
		self.add_parameter('ActionTopic', 'sara_action')

		# references to used behaviors
		self.add_behavior(sara_command_managerSM, 'Sara parallel Runtime/Sara brain/sara_command_manager')
		self.add_behavior(SaraactionexecutorSM, 'Sara parallel Runtime/Sara action executor/Sara action executor')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
        
        # [/MANUAL_INIT]

		# Behavior comments:

		# ! 676 291 /Sara parallel Runtime/Shutdown conditions checker
		# true=RUN|nfalse=STOP



	def create(self):
		# x:914 y:505
		_state_machine = OperatableStateMachine(outcomes=['Shutdown'])
		_state_machine.userdata.Command = "no nothing"
		_state_machine.userdata.End = False

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

		# x:841 y:231
		_sm_sara_action_executor_0 = OperatableStateMachine(outcomes=['shutdown'], input_keys=['HighFIFO', 'MedFIFO', 'LowFIFO', 'DoNow', 'End'])

		with _sm_sara_action_executor_0:
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
		_sm_sara_brain_1 = OperatableStateMachine(outcomes=['error'], input_keys=['HighFIFO', 'LowFIFO', 'MedFIFO', 'DoNow', 'End'])

		with _sm_sara_brain_1:
			# x:270 y:346
			OperatableStateMachine.add('sara_command_manager',
										self.use_behavior(sara_command_managerSM, 'Sara parallel Runtime/Sara brain/sara_command_manager'),
										transitions={'finished': 'For loop', 'failed': 'error'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'HighFIFO': 'HighFIFO', 'MedFIFO': 'MedFIFO', 'LowFIFO': 'LowFIFO', 'DoNow': 'DoNow'})

			# x:599 y:251
			OperatableStateMachine.add('For loop',
										ForLoop(repeat=10),
										transitions={'do': 'sara_command_manager', 'end': 'set end'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index'})

			# x:725 y:305
			OperatableStateMachine.add('set end',
										CalculationState(calculation=lambda x: True),
										transitions={'done': 'error'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'End', 'output_value': 'End'})


		# x:55 y:366
		_sm_create_fifos_2 = OperatableStateMachine(outcomes=['done'], output_keys=['HighFIFO', 'MedFIFO', 'LowFIFO', 'DoNow'])

		with _sm_create_fifos_2:
			# x:33 y:40
			OperatableStateMachine.add('Create HighFIFO',
										FIFO_New(),
										transitions={'done': 'Create MedFIFO'},
										autonomy={'done': Autonomy.Off},
										remapping={'FIFO': 'HighFIFO'})

			# x:30 y:114
			OperatableStateMachine.add('Create MedFIFO',
										FIFO_New(),
										transitions={'done': 'Create LowFIFO'},
										autonomy={'done': Autonomy.Off},
										remapping={'FIFO': 'MedFIFO'})

			# x:30 y:189
			OperatableStateMachine.add('Create LowFIFO',
										FIFO_New(),
										transitions={'done': 'Create DoNow'},
										autonomy={'done': Autonomy.Off},
										remapping={'FIFO': 'LowFIFO'})

			# x:34 y:260
			OperatableStateMachine.add('Create DoNow',
										FIFO_New(),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off},
										remapping={'FIFO': 'DoNow'})


		# x:30 y:322
		_sm_sara_shutdown_3 = OperatableStateMachine(outcomes=['finished'])

		with _sm_sara_shutdown_3:
			# x:57 y:86
			OperatableStateMachine.add('log',
										LogState(text="shutdown", severity=Logger.REPORT_HINT),
										transitions={'done': 'say'},
										autonomy={'done': Autonomy.Off})

			# x:122 y:228
			OperatableStateMachine.add('say',
										SaraSay(sentence="I'm goint to shutdown for safetiy reasons", emotion=1, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		# x:291 y:514, x:284 y:353, x:276 y:271
		_sm_sara_parallel_runtime_4 = ConcurrencyContainer(outcomes=['Shutdown'], input_keys=['HighFIFO', 'MedFIFO', 'LowFIFO', 'DoNow', 'End'], conditions=[
										('Shutdown', [('Sara brain', 'error')]),
										('Shutdown', [('Sara action executor', 'shutdown')])
										])

		with _sm_sara_parallel_runtime_4:
			# x:57 y:333
			OperatableStateMachine.add('Sara brain',
										_sm_sara_brain_1,
										transitions={'error': 'Shutdown'},
										autonomy={'error': Autonomy.Inherit},
										remapping={'HighFIFO': 'HighFIFO', 'LowFIFO': 'LowFIFO', 'MedFIFO': 'MedFIFO', 'DoNow': 'DoNow', 'End': 'End'})

			# x:52 y:416
			OperatableStateMachine.add('Sara action executor',
										_sm_sara_action_executor_0,
										transitions={'shutdown': 'Shutdown'},
										autonomy={'shutdown': Autonomy.Inherit},
										remapping={'HighFIFO': 'HighFIFO', 'MedFIFO': 'MedFIFO', 'LowFIFO': 'LowFIFO', 'DoNow': 'DoNow', 'End': 'End'})



		with _state_machine:
			# x:43 y:60
			OperatableStateMachine.add('log',
										LogState(text="Start Sara", severity=Logger.REPORT_HINT),
										transitions={'done': 'Create_FIFOs'},
										autonomy={'done': Autonomy.Off})

			# x:400 y:331
			OperatableStateMachine.add('Sara parallel Runtime',
										_sm_sara_parallel_runtime_4,
										transitions={'Shutdown': 'Sara shutdown'},
										autonomy={'Shutdown': Autonomy.Inherit},
										remapping={'HighFIFO': 'HighFIFO', 'MedFIFO': 'MedFIFO', 'LowFIFO': 'LowFIFO', 'DoNow': 'DoNow', 'End': 'End'})

			# x:701 y:485
			OperatableStateMachine.add('Sara shutdown',
										_sm_sara_shutdown_3,
										transitions={'finished': 'Shutdown'},
										autonomy={'finished': Autonomy.Inherit})

			# x:187 y:210
			OperatableStateMachine.add('Create_FIFOs',
										_sm_create_fifos_2,
										transitions={'done': 'Sara parallel Runtime'},
										autonomy={'done': Autonomy.Inherit},
										remapping={'HighFIFO': 'HighFIFO', 'MedFIFO': 'MedFIFO', 'LowFIFO': 'LowFIFO', 'DoNow': 'DoNow'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
