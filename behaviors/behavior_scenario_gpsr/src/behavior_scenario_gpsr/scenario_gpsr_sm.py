#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_scenario_gpsr')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.for_loop import ForLoop
from sara_flexbe_states.get_speech import GetSpeech
from sara_flexbe_states.sara_nlu_gpsr import SaraNLUgpsr
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.get_robot_pose import Get_Robot_Pose
from sara_flexbe_states.SetKey import SetKey
from flexbe_states.flexible_calculation_state import FlexibleCalculationState
from flexbe_states.flexible_check_condition_state import FlexibleCheckConditionState
from flexbe_states.calculation_state import CalculationState
from behavior_action_executor.action_executor_sm import Action_ExecutorSM
from flexbe_states.wait_state import WaitState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed May 30 2018
@author: Philippe La Madeleine
'''
class Scenario_GPSRSM(Behavior):
	'''
	Implementation du scenario GPSR.
	'''


	def __init__(self):
		super(Scenario_GPSRSM, self).__init__()
		self.name = 'Scenario_GPSR'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(Action_ExecutorSM, 'Do the actions/Action_Executor')
		self.add_behavior(Action_ExecutorSM, 'Action_Executor')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:461 y:37, x:739 y:154
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.ActionGoToStart = ["Move", "table", "kitchen"]

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:30 y:324
		_sm_fail_state_0 = OperatableStateMachine(outcomes=['finished'])

		with _sm_fail_state_0:
			# x:88 y:141
			OperatableStateMachine.add('s',
										WaitState(wait_time=1),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		# x:588 y:141, x:590 y:545, x:642 y:410
		_sm_do_the_actions_1 = OperatableStateMachine(outcomes=['finished', 'failed', 'critical fail'], input_keys=['ActionForms', 'OriginalPose'])

		with _sm_do_the_actions_1:
			# x:85 y:33
			OperatableStateMachine.add('set i',
										SetKey(Value=0),
										transitions={'done': 'is form?'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'index'})

			# x:62 y:236
			OperatableStateMachine.add('GetForm',
										FlexibleCalculationState(calculation=lambda x: x[0][x[1]], input_keys=["ActionForms", "index"]),
										transitions={'done': 'Action_Executor'},
										autonomy={'done': Autonomy.Off},
										remapping={'ActionForms': 'ActionForms', 'index': 'index', 'output_value': 'ActionForm'})

			# x:57 y:131
			OperatableStateMachine.add('is form?',
										FlexibleCheckConditionState(predicate=lambda x: x[0][x[1]] != None, input_keys=["ActionForms", "index"]),
										transitions={'true': 'GetForm', 'false': 'finished'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'ActionForms': 'ActionForms', 'index': 'index'})

			# x:204 y:237
			OperatableStateMachine.add('++i',
										CalculationState(calculation=lambda x: x+1),
										transitions={'done': 'is form?'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'index', 'output_value': 'index'})

			# x:64 y:352
			OperatableStateMachine.add('Action_Executor',
										self.use_behavior(Action_ExecutorSM, 'Do the actions/Action_Executor'),
										transitions={'finished': '++i', 'failed': 'failed', 'critical_fail': 'critical fail'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'ActionForm'})


		# x:30 y:324, x:130 y:324
		_sm_get_commands_2 = OperatableStateMachine(outcomes=['fail', 'understood'], output_keys=['ActionForms'])

		with _sm_get_commands_2:
			# x:33 y:40
			OperatableStateMachine.add('GetSpeech',
										GetSpeech(watchdog=5),
										transitions={'done': 'SaraNLUgpsr', 'nothing': 'GetSpeech', 'fail': 'fail'},
										autonomy={'done': Autonomy.Off, 'nothing': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'words': 'sentence'})

			# x:30 y:226
			OperatableStateMachine.add('SaraNLUgpsr',
										SaraNLUgpsr(),
										transitions={'understood': 'understood', 'not_understood': 'say sorry', 'fail': 'say sorry'},
										autonomy={'understood': Autonomy.Off, 'not_understood': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'sentence': 'sentence', 'ActionForms': 'ActionForms'})

			# x:179 y:137
			OperatableStateMachine.add('say sorry',
										SaraSay(sentence="Sorry, I could not understand what you said.", emotion=1, block=True),
										transitions={'done': 'GetSpeech'},
										autonomy={'done': Autonomy.Off})



		with _state_machine:
			# x:75 y:26
			OperatableStateMachine.add('for 3',
										ForLoop(repeat=3),
										transitions={'do': 'GetOriginalPose', 'end': 'win'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index'})

			# x:44 y:380
			OperatableStateMachine.add('Get Commands',
										_sm_get_commands_2,
										transitions={'fail': 'critical', 'understood': 'Do the actions'},
										autonomy={'fail': Autonomy.Inherit, 'understood': Autonomy.Inherit},
										remapping={'ActionForms': 'ActionForms'})

			# x:52 y:266
			OperatableStateMachine.add('GetOriginalPose',
										Get_Robot_Pose(),
										transitions={'done': 'Get Commands'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose': 'OriginalPose'})

			# x:415 y:377
			OperatableStateMachine.add('Do the actions',
										_sm_do_the_actions_1,
										transitions={'finished': 'for 3', 'failed': 'Fail state', 'critical fail': 'critical'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical fail': Autonomy.Inherit},
										remapping={'ActionForms': 'ActionForms', 'OriginalPose': 'OriginalPose'})

			# x:680 y:380
			OperatableStateMachine.add('Fail state',
										_sm_fail_state_0,
										transitions={'finished': 'Action_Executor'},
										autonomy={'finished': Autonomy.Inherit})

			# x:48 y:134
			OperatableStateMachine.add('Action_Executor',
										self.use_behavior(Action_ExecutorSM, 'Action_Executor'),
										transitions={'finished': 'GetOriginalPose', 'failed': 'critical', 'critical_fail': 'critical'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'ActionGoToStart'})

			# x:480 y:142
			OperatableStateMachine.add('critical',
										SaraSay(sentence="Critical failure! I'm stopping right there.", emotion=1, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:276 y:31
			OperatableStateMachine.add('win',
										SaraSay(sentence="I did it. I'm the best robot.", emotion=1, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
