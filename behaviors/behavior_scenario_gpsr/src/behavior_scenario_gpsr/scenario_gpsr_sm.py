#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_scenario_gpsr')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.moveit_move import MoveitMove
from sara_flexbe_states.get_robot_pose import Get_Robot_Pose
from sara_flexbe_states.SetKey import SetKey
from flexbe_states.flexible_calculation_state import FlexibleCalculationState
from flexbe_states.flexible_check_condition_state import FlexibleCheckConditionState
from flexbe_states.calculation_state import CalculationState
from behavior_action_executor.action_executor_sm import Action_ExecutorSM
from sara_flexbe_states.StoryboardSetStepKey import StoryboardSetStepKey
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.for_loop import ForLoop
from sara_flexbe_states.sara_nlu_gpsr import SaraNLUgpsr
from sara_flexbe_states.get_speech import GetSpeech
from sara_flexbe_states.list_entities_by_name import list_entities_by_name
from behavior_action_look_at_face.action_look_at_face_sm import action_look_at_faceSM
from sara_flexbe_states.StoryboardSetStoryKey import StoryboardSetStoryFromAction
from sara_flexbe_states.set_a_step import Set_a_step
from flexbe_states.log_key_state import LogKeyState
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
		self.add_behavior(action_look_at_faceSM, 'Interact operator/look at op/action_look_at_face')
		self.add_behavior(Action_ExecutorSM, 'Action_Executor')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:209 y:596, x:451 y:313
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.ActionGoToStart = ["Move", "spr/waypoint1"]
		_state_machine.userdata.PositionBras = "IdlePose"
		_state_machine.userdata.title = "GPSR"

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:30 y:324
		_sm_look_at_op_0 = OperatableStateMachine(outcomes=['fail'])

		with _sm_look_at_op_0:
			# x:61 y:31
			OperatableStateMachine.add('set name',
										SetKey(Value="person"),
										transitions={'done': 'list persons'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'name'})

			# x:44 y:110
			OperatableStateMachine.add('list persons',
										list_entities_by_name(frontality_level=0.5),
										transitions={'found': 'get closest', 'not_found': 'list persons'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'name': 'name', 'entity_list': 'entity_list', 'number': 'number'})

			# x:45 y:188
			OperatableStateMachine.add('get closest',
										CalculationState(calculation=lambda x: x[0]),
										transitions={'done': 'action_look_at_face'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'entity_list', 'output_value': 'Entity'})

			# x:246 y:182
			OperatableStateMachine.add('action_look_at_face',
										self.use_behavior(action_look_at_faceSM, 'Interact operator/look at op/action_look_at_face'),
										transitions={'finished': 'list persons', 'failed': 'list persons'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'Entity': 'Entity'})


		# x:307 y:35, x:335 y:491
		_sm_get_commands_1 = OperatableStateMachine(outcomes=['fail', 'understood'], output_keys=['ActionForms', 'sentence'])

		with _sm_get_commands_1:
			# x:50 y:48
			OperatableStateMachine.add('say ready',
										SaraSay(sentence="I'm ready for your commands.", emotion=1, block=False),
										transitions={'done': 'GetSpeech'},
										autonomy={'done': Autonomy.Off})

			# x:32 y:392
			OperatableStateMachine.add('SaraNLUgpsr',
										SaraNLUgpsr(),
										transitions={'understood': 'say understood', 'not_understood': 'say sorry', 'fail': 'say sorry'},
										autonomy={'understood': Autonomy.Off, 'not_understood': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'sentence': 'sentence', 'ActionForms': 'ActionForms'})

			# x:231 y:301
			OperatableStateMachine.add('say sorry',
										SaraSay(sentence="Sorry, I could not understand what you said.", emotion=1, block=True),
										transitions={'done': 'GetSpeech'},
										autonomy={'done': Autonomy.Off})

			# x:30 y:491
			OperatableStateMachine.add('say understood',
										SaraSay(sentence="Ok", emotion=1, block=True),
										transitions={'done': 'understood'},
										autonomy={'done': Autonomy.Off})

			# x:39 y:184
			OperatableStateMachine.add('GetSpeech',
										GetSpeech(watchdog=5),
										transitions={'done': 'SaraNLUgpsr', 'nothing': 'GetSpeech', 'fail': 'fail'},
										autonomy={'done': Autonomy.Off, 'nothing': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'words': 'sentence'})


		# x:320 y:82, x:322 y:143, x:265 y:407, x:306 y:225, x:430 y:324
		_sm_interact_operator_2 = ConcurrencyContainer(outcomes=['fail', 'understood'], output_keys=['ActionForms', 'sentence'], conditions=[
										('understood', [('Get Commands', 'understood')]),
										('fail', [('Get Commands', 'fail')]),
										('fail', [('look at op', 'fail')])
										])

		with _sm_interact_operator_2:
			# x:95 y:45
			OperatableStateMachine.add('Get Commands',
										_sm_get_commands_1,
										transitions={'fail': 'fail', 'understood': 'understood'},
										autonomy={'fail': Autonomy.Inherit, 'understood': Autonomy.Inherit},
										remapping={'ActionForms': 'ActionForms', 'sentence': 'sentence'})

			# x:99 y:198
			OperatableStateMachine.add('look at op',
										_sm_look_at_op_0,
										transitions={'fail': 'fail'},
										autonomy={'fail': Autonomy.Inherit})


		# x:30 y:324
		_sm_fail_state_3 = OperatableStateMachine(outcomes=['finished'])

		with _sm_fail_state_3:
			# x:248 y:81
			OperatableStateMachine.add('say failed',
										SaraSay(sentence="I failed. I'm going back to tell my master.", emotion=1, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		# x:588 y:141, x:590 y:545, x:642 y:410
		_sm_do_the_actions_4 = OperatableStateMachine(outcomes=['finished', 'failed', 'critical fail'], input_keys=['ActionForms', 'OriginalPose'])

		with _sm_do_the_actions_4:
			# x:85 y:33
			OperatableStateMachine.add('set i',
										SetKey(Value=0),
										transitions={'done': 'is form?'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'index'})

			# x:48 y:339
			OperatableStateMachine.add('GetForm',
										FlexibleCalculationState(calculation=lambda x: x[0][x[1]], input_keys=["ActionForms", "index"]),
										transitions={'done': 'Action_Executor'},
										autonomy={'done': Autonomy.Off},
										remapping={'ActionForms': 'ActionForms', 'index': 'index', 'output_value': 'ActionForm'})

			# x:57 y:131
			OperatableStateMachine.add('is form?',
										FlexibleCheckConditionState(predicate=lambda x: x[0][x[1]] != None, input_keys=["ActionForms", "index"]),
										transitions={'true': 'set setp', 'false': 'finished'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'ActionForms': 'ActionForms', 'index': 'index'})

			# x:204 y:237
			OperatableStateMachine.add('++i',
										CalculationState(calculation=lambda x: x+1),
										transitions={'done': 'is form?'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'index', 'output_value': 'index'})

			# x:72 y:479
			OperatableStateMachine.add('Action_Executor',
										self.use_behavior(Action_ExecutorSM, 'Do the actions/Action_Executor'),
										transitions={'finished': '++i', 'failed': 'failed', 'critical_fail': 'critical fail'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'ActionForm'})

			# x:45 y:241
			OperatableStateMachine.add('set setp',
										StoryboardSetStepKey(),
										transitions={'done': 'GetForm'},
										autonomy={'done': Autonomy.Off},
										remapping={'step': 'index'})



		with _state_machine:
			# x:36 y:26
			OperatableStateMachine.add('bras en lair',
										MoveitMove(move=True, waitForExecution=False, group="RightArm"),
										transitions={'done': 'say start', 'failed': 'say start'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'PositionBras'})

			# x:14 y:426
			OperatableStateMachine.add('GetOriginalPose',
										Get_Robot_Pose(),
										transitions={'done': 'Interact operator'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose': 'OriginalPose'})

			# x:657 y:405
			OperatableStateMachine.add('Do the actions',
										_sm_do_the_actions_4,
										transitions={'finished': 'say succseed', 'failed': 'Fail state', 'critical fail': 'critical'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical fail': Autonomy.Inherit},
										remapping={'ActionForms': 'ActionForms', 'OriginalPose': 'OriginalPose'})

			# x:431 y:30
			OperatableStateMachine.add('Fail state',
										_sm_fail_state_3,
										transitions={'finished': 'Action_Executor'},
										autonomy={'finished': Autonomy.Inherit})

			# x:246 y:318
			OperatableStateMachine.add('critical',
										SaraSay(sentence="Critical failure! I require medical assistance.", emotion=1, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:35 y:583
			OperatableStateMachine.add('win',
										SaraSay(sentence="I did it. I'm the best robot.", emotion=1, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:34 y:505
			OperatableStateMachine.add('for 3',
										ForLoop(repeat=3),
										transitions={'do': 'GetOriginalPose', 'end': 'win'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index'})

			# x:671 y:539
			OperatableStateMachine.add('say succseed',
										SaraSay(sentence="I succeed my mission. I'm going back", emotion=1, block=True),
										transitions={'done': 'for 3'},
										autonomy={'done': Autonomy.Off})

			# x:196 y:438
			OperatableStateMachine.add('Interact operator',
										_sm_interact_operator_2,
										transitions={'fail': 'critical', 'understood': 'log'},
										autonomy={'fail': Autonomy.Inherit, 'understood': Autonomy.Inherit},
										remapping={'ActionForms': 'ActionForms', 'sentence': 'sentence'})

			# x:18 y:194
			OperatableStateMachine.add('Action_Executor',
										self.use_behavior(Action_ExecutorSM, 'Action_Executor'),
										transitions={'finished': 'GetOriginalPose', 'failed': 'critical', 'critical_fail': 'critical'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'ActionGoToStart'})

			# x:40 y:117
			OperatableStateMachine.add('say start',
										SaraSay(sentence="I'm ready to start the GPSR scenario.", emotion=1, block=True),
										transitions={'done': 'Action_Executor'},
										autonomy={'done': Autonomy.Off})

			# x:476 y:522
			OperatableStateMachine.add('set story',
										StoryboardSetStoryFromAction(),
										transitions={'done': 'Do the actions'},
										autonomy={'done': Autonomy.Off},
										remapping={'titre': 'title', 'actionList': 'ActionForms'})

			# x:359 y:454
			OperatableStateMachine.add('set step',
										Set_a_step(step=0),
										transitions={'done': 'set story'},
										autonomy={'done': Autonomy.Off})

			# x:321 y:647
			OperatableStateMachine.add('log',
										LogKeyState(text="{}", severity=Logger.REPORT_HINT),
										transitions={'done': 'set step'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'ActionForms'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
