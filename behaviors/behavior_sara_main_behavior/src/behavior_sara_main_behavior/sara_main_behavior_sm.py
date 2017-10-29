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
from behavior_sara_action_executor.sara_action_executor_sm import SaraactionexecutorSM
from behavior_sara_command_manager.sara_command_manager_sm import sara_command_managerSM
from flexbe_states.calculation_state import CalculationState
from flexbe_states.check_condition_state import CheckConditionState
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.FIFO_New import FIFO_New
from sara_flexbe_states.get_speech import GetSpeech
from sara_flexbe_states.sara_set_angle import SaraSetHeadAngle
from sara_flexbe_states.move_arm_named_pose import MoveArmNamedPose
from sara_flexbe_states.sara_set_expression import SetExpression
from sara_flexbe_states.regex_tester import RegexTester
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
		self.add_behavior(SaraactionexecutorSM, 'Sara parallel Runtime/Sara action executor/Sara action executor')
		self.add_behavior(sara_command_managerSM, 'Sara parallel Runtime/Sara brain/sara_command_manager')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
        
        # [/MANUAL_INIT]

		# Behavior comments:

		# ! 676 291 /Sara parallel Runtime/Shutdown conditions checker
		# true=RUN|nfalse=STOP



	def create(self):
		# x:137 y:362
		_state_machine = OperatableStateMachine(outcomes=['Shutdown'])
		_state_machine.userdata.Command = "no nothing"
		_state_machine.userdata.End = False

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

		# x:887 y:420
		_sm_sara_brain_0 = OperatableStateMachine(outcomes=['error'], input_keys=['HighFIFO', 'LowFIFO', 'MedFIFO', 'DoNow', 'End'])

		with _sm_sara_brain_0:
			# x:270 y:346
			OperatableStateMachine.add('sara_command_manager',
										self.use_behavior(sara_command_managerSM, 'Sara parallel Runtime/Sara brain/sara_command_manager'),
										transitions={'finished': 'if stop', 'failed': 'set end'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'HighFIFO': 'HighFIFO', 'MedFIFO': 'MedFIFO', 'LowFIFO': 'LowFIFO', 'DoNow': 'DoNow'})

			# x:725 y:388
			OperatableStateMachine.add('set end',
										CalculationState(calculation=lambda x: True),
										transitions={'done': 'error'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'End', 'output_value': 'End'})

			# x:516 y:448
			OperatableStateMachine.add('if stop',
										CheckConditionState(predicate=lambda x: x[0][0]=="Stop"),
										transitions={'true': 'set end', 'false': 'sara_command_manager'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'DoNow'})


		# x:841 y:231
		_sm_sara_action_executor_1 = OperatableStateMachine(outcomes=['shutdown'], input_keys=['HighFIFO', 'MedFIFO', 'LowFIFO', 'DoNow', 'End'])

		with _sm_sara_action_executor_1:
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


		# x:30 y:365
		_sm_sara_init_2 = OperatableStateMachine(outcomes=['done'])

		with _sm_sara_init_2:
			# x:30 y:40
			OperatableStateMachine.add('set head',
										SaraSetHeadAngle(angle=0.1),
										transitions={'done': 'set face'},
										autonomy={'done': Autonomy.Off})

			# x:47 y:119
			OperatableStateMachine.add('set arm',
										MoveArmNamedPose(pose_name="PreGripPose", wait=False),
										transitions={'done': 'hello', 'failed': 'hello'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

			# x:242 y:288
			OperatableStateMachine.add('hello',
										SaraSay(sentence="Good morning. I am Sara the robot. Please give me orders.", emotion=1, block=True),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off})

			# x:239 y:47
			OperatableStateMachine.add('set face',
										SetExpression(emotion=1, brightness=255),
										transitions={'done': 'set arm'},
										autonomy={'done': Autonomy.Off})


		# x:55 y:366
		_sm_create_fifos_3 = OperatableStateMachine(outcomes=['done'], output_keys=['HighFIFO', 'MedFIFO', 'LowFIFO', 'DoNow'])

		with _sm_create_fifos_3:
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
		_sm_sara_shutdown_4 = OperatableStateMachine(outcomes=['finished'])

		with _sm_sara_shutdown_4:
			# x:57 y:86
			OperatableStateMachine.add('log',
										LogState(text="shutdown", severity=Logger.REPORT_HINT),
										transitions={'done': 'say'},
										autonomy={'done': Autonomy.Off})

			# x:122 y:228
			OperatableStateMachine.add('say',
										SaraSay(sentence="I'm goint to shutdown for safety reasons", emotion=1, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		# x:336 y:314, x:315 y:433, x:276 y:271
		_sm_sara_parallel_runtime_5 = ConcurrencyContainer(outcomes=['Shutdown'], input_keys=['HighFIFO', 'MedFIFO', 'LowFIFO', 'DoNow', 'End'], conditions=[
										('Shutdown', [('Sara brain', 'error')]),
										('Shutdown', [('Sara action executor', 'shutdown')])
										])

		with _sm_sara_parallel_runtime_5:
			# x:52 y:416
			OperatableStateMachine.add('Sara action executor',
										_sm_sara_action_executor_1,
										transitions={'shutdown': 'Shutdown'},
										autonomy={'shutdown': Autonomy.Inherit},
										remapping={'HighFIFO': 'HighFIFO', 'MedFIFO': 'MedFIFO', 'LowFIFO': 'LowFIFO', 'DoNow': 'DoNow', 'End': 'End'})

			# x:57 y:333
			OperatableStateMachine.add('Sara brain',
										_sm_sara_brain_0,
										transitions={'error': 'Shutdown'},
										autonomy={'error': Autonomy.Inherit},
										remapping={'HighFIFO': 'HighFIFO', 'LowFIFO': 'LowFIFO', 'MedFIFO': 'MedFIFO', 'DoNow': 'DoNow', 'End': 'End'})



		with _state_machine:
			# x:43 y:60
			OperatableStateMachine.add('log',
										LogState(text="Start Sara", severity=Logger.REPORT_HINT),
										transitions={'done': 'listen'},
										autonomy={'done': Autonomy.Off})

			# x:306 y:365
			OperatableStateMachine.add('Sara parallel Runtime',
										_sm_sara_parallel_runtime_5,
										transitions={'Shutdown': 'Sara shutdown'},
										autonomy={'Shutdown': Autonomy.Inherit},
										remapping={'HighFIFO': 'HighFIFO', 'MedFIFO': 'MedFIFO', 'LowFIFO': 'LowFIFO', 'DoNow': 'DoNow', 'End': 'End'})

			# x:315 y:462
			OperatableStateMachine.add('Sara shutdown',
										_sm_sara_shutdown_4,
										transitions={'finished': 'listen'},
										autonomy={'finished': Autonomy.Inherit})

			# x:328 y:284
			OperatableStateMachine.add('Create_FIFOs',
										_sm_create_fifos_3,
										transitions={'done': 'Sara parallel Runtime'},
										autonomy={'done': Autonomy.Inherit},
										remapping={'HighFIFO': 'HighFIFO', 'MedFIFO': 'MedFIFO', 'LowFIFO': 'LowFIFO', 'DoNow': 'DoNow'})

			# x:112 y:249
			OperatableStateMachine.add('listen',
										GetSpeech(watchdog=10),
										transitions={'done': 'check hello', 'nothing': 'listen', 'fail': 'Shutdown'},
										autonomy={'done': Autonomy.Off, 'nothing': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'words': 'words'})

			# x:345 y:195
			OperatableStateMachine.add('Sara init',
										_sm_sara_init_2,
										transitions={'done': 'Create_FIFOs'},
										autonomy={'done': Autonomy.Inherit})

			# x:337 y:74
			OperatableStateMachine.add('check hello',
										RegexTester(regex=".*((wake up)|(sarah?)|(shut up)|(hello)(robot)|(hi)|(morning)|(greet)).*"),
										transitions={'true': 'Sara init', 'false': 'listen'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'text': 'words', 'result': 'result'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
