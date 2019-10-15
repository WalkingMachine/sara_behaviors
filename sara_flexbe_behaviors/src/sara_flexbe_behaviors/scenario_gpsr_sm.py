#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_behaviors.action_pass_door_sm import Action_Pass_DoorSM as Action_Pass_DoorSM
from sara_flexbe_states.story import Set_Story
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.set_a_step import Set_a_step
from sara_flexbe_states.moveit_move import MoveitMove
from sara_flexbe_states.SetKey import SetKey
from flexbe_states.flexible_calculation_state import FlexibleCalculationState
from flexbe_states.flexible_check_condition_state import FlexibleCheckConditionState
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_behaviors.action_executor_sm import Action_ExecutorSM as Action_ExecutorSM
from sara_flexbe_states.StoryboardSetStepKey import StoryboardSetStepKey
from sara_flexbe_states.GetRosParam import GetRosParam
from sara_flexbe_behaviors.action_move_sm import Action_MoveSM as Action_MoveSM
from sara_flexbe_states.for_loop import ForLoop
from sara_flexbe_states.sara_nlu_gpsr import SaraNLUgpsr
from sara_flexbe_states.get_speech import GetSpeech
from flexbe_states.check_condition_state import CheckConditionState
from sara_flexbe_states.list_entities_by_name import list_entities_by_name
from sara_flexbe_states.KeepLookingAt import KeepLookingAt
from sara_flexbe_states.StoryboardSetStoryKey import StoryboardSetStoryFromAction
from sara_flexbe_states.get_robot_pose import Get_Robot_Pose
from sara_flexbe_states.sara_set_head_angle import SaraSetHeadAngle
from sara_flexbe_states.continue_button import ContinueButton
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
		self.add_behavior(Action_Pass_DoorSM, 'Initialisation/Action_Pass_Door')
		self.add_behavior(Action_ExecutorSM, 'Do the actions/Action_Executor')
		self.add_behavior(Action_MoveSM, 'Fail state/Action_Move')
		self.add_behavior(Action_Pass_DoorSM, 'End/Action_Pass_Door')
		self.add_behavior(Action_MoveSM, 'Action_Move')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:391 y:586, x:438 y:304
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.StartPosition = "Operator"
		_state_machine.userdata.PositionBras = "IdlePose"
		_state_machine.userdata.title = "GPSR"
		_state_machine.userdata.EntryName = "door1/enter"
		_state_machine.userdata.ExitName = "door2/exit"

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:135 y:542, x:527 y:395
		_sm_validate_0 = OperatableStateMachine(outcomes=['done', 'bad'], input_keys=['sentence'])

		with _sm_validate_0:
			# x:56 y:62
			OperatableStateMachine.add('Say_Command',
										SaraSay(sentence=lambda x: "I heard. " +x+ ". Is that correct?", input_keys=[], emotion=0, block=True),
										transitions={'done': 'get speech'},
										autonomy={'done': Autonomy.Off})

			# x:44 y:165
			OperatableStateMachine.add('get speech',
										GetSpeech(watchdog=10),
										transitions={'done': 'is yes', 'nothing': 'say repeate', 'fail': 'say repeate'},
										autonomy={'done': Autonomy.Off, 'nothing': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'words': 'words'})

			# x:91 y:307
			OperatableStateMachine.add('is yes',
										CheckConditionState(predicate=lambda x: "yes" in x or "right" in x or "sure" in x),
										transitions={'true': 'done', 'false': 'say repeate'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'words'})

			# x:423 y:332
			OperatableStateMachine.add('say repeate',
										SaraSay(sentence="Please, repeat your command.", input_keys=[], emotion=1, block=True),
										transitions={'done': 'bad'},
										autonomy={'done': Autonomy.Off})


		# x:30 y:324
		_sm_look_at_op_1 = OperatableStateMachine(outcomes=['fail'])

		with _sm_look_at_op_1:
			# x:61 y:31
			OperatableStateMachine.add('set name',
										SetKey(Value="person"),
										transitions={'done': 'list persons'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'name'})

			# x:44 y:110
			OperatableStateMachine.add('list persons',
										list_entities_by_name(frontality_level=0.5, distance_max=10),
										transitions={'found': 'get closest', 'none_found': 'list persons'},
										autonomy={'found': Autonomy.Off, 'none_found': Autonomy.Off},
										remapping={'name': 'name', 'entity_list': 'entity_list', 'number': 'number'})

			# x:43 y:211
			OperatableStateMachine.add('get closest',
										CalculationState(calculation=lambda x: x[0].ID),
										transitions={'done': 'look at'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'entity_list', 'output_value': 'ID'})

			# x:210 y:198
			OperatableStateMachine.add('look at',
										KeepLookingAt(),
										transitions={'failed': 'list persons'},
										autonomy={'failed': Autonomy.Off},
										remapping={'ID': 'ID'})


		# x:307 y:35, x:335 y:491
		_sm_get_commands_2 = OperatableStateMachine(outcomes=['fail', 'understood'], output_keys=['ActionForms', 'sentence'])

		with _sm_get_commands_2:
			# x:50 y:48
			OperatableStateMachine.add('say ready',
										SaraSay(sentence="I'm ready for your commands.", input_keys=[], emotion=1, block=False),
										transitions={'done': 'GetSpeech'},
										autonomy={'done': Autonomy.Off})

			# x:32 y:408
			OperatableStateMachine.add('SaraNLUgpsr',
										SaraNLUgpsr(),
										transitions={'understood': 'say understood', 'not_understood': 'say sorry', 'fail': 'say sorry'},
										autonomy={'understood': Autonomy.Off, 'not_understood': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'sentence': 'sentence', 'ActionForms': 'ActionForms'})

			# x:597 y:223
			OperatableStateMachine.add('say sorry',
										SaraSay(sentence="Sorry, I could not understand what you said.", input_keys=[], emotion=1, block=True),
										transitions={'done': 'GetSpeech'},
										autonomy={'done': Autonomy.Off})

			# x:30 y:491
			OperatableStateMachine.add('say understood',
										SaraSay(sentence="Ok", input_keys=[], emotion=1, block=True),
										transitions={'done': 'understood'},
										autonomy={'done': Autonomy.Off})

			# x:44 y:131
			OperatableStateMachine.add('GetSpeech',
										GetSpeech(watchdog=5),
										transitions={'done': 'validate', 'nothing': 'GetSpeech', 'fail': 'fail'},
										autonomy={'done': Autonomy.Off, 'nothing': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'words': 'sentence'})

			# x:29 y:259
			OperatableStateMachine.add('validate',
										_sm_validate_0,
										transitions={'done': 'SaraNLUgpsr', 'bad': 'GetSpeech'},
										autonomy={'done': Autonomy.Inherit, 'bad': Autonomy.Inherit},
										remapping={'sentence': 'sentence'})


		# x:122 y:413
		_sm_end_3 = OperatableStateMachine(outcomes=['done'], input_keys=['ExitName'])

		with _sm_end_3:
			# x:30 y:40
			OperatableStateMachine.add('win',
										SaraSay(sentence="Thank you. I'm going now.", input_keys=[], emotion=1, block=True),
										transitions={'done': 'Action_Pass_Door'},
										autonomy={'done': Autonomy.Off})

			# x:33 y:163
			OperatableStateMachine.add('Action_Pass_Door',
										self.use_behavior(Action_Pass_DoorSM, 'End/Action_Pass_Door'),
										transitions={'Done': 'say yay', 'Fail': 'done'},
										autonomy={'Done': Autonomy.Inherit, 'Fail': Autonomy.Inherit},
										remapping={'DoorName': 'ExitName'})

			# x:210 y:262
			OperatableStateMachine.add('say yay',
										SaraSay(sentence="I did it. I'm the best robot.", input_keys=[], emotion=1, block=True),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off})


		# x:320 y:82, x:322 y:143, x:265 y:407, x:306 y:225, x:430 y:324
		_sm_interact_operator_4 = ConcurrencyContainer(outcomes=['fail', 'understood'], output_keys=['ActionForms', 'sentence'], conditions=[
										('understood', [('Get Commands', 'understood')]),
										('fail', [('Get Commands', 'fail')]),
										('fail', [('look at op', 'fail')])
										])

		with _sm_interact_operator_4:
			# x:95 y:45
			OperatableStateMachine.add('Get Commands',
										_sm_get_commands_2,
										transitions={'fail': 'fail', 'understood': 'understood'},
										autonomy={'fail': Autonomy.Inherit, 'understood': Autonomy.Inherit},
										remapping={'ActionForms': 'ActionForms', 'sentence': 'sentence'})

			# x:99 y:198
			OperatableStateMachine.add('look at op',
										_sm_look_at_op_1,
										transitions={'fail': 'fail'},
										autonomy={'fail': Autonomy.Inherit})


		# x:325 y:387, x:314 y:190
		_sm_fail_state_5 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['StartPosition'])

		with _sm_fail_state_5:
			# x:36 y:29
			OperatableStateMachine.add('say failed',
										SaraSay(sentence="I failed. I'm going back to tell my master.", input_keys=[], emotion=1, block=True),
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Off})

			# x:42 y:301
			OperatableStateMachine.add('get error',
										GetRosParam(ParamName="behavior/GPSR/CauseOfFailure"),
										transitions={'done': 'Say_Error', 'failed': 'finished'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'Value': 'Error'})

			# x:48 y:414
			OperatableStateMachine.add('Say_Error',
										SaraSay(sentence=lambda x: "Sorry, I failed because "+x, input_keys=[], emotion=0, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:25 y:172
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(Action_MoveSM, 'Fail state/Action_Move'),
										transitions={'finished': 'get error', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'StartPosition'})


		# x:588 y:141, x:590 y:545, x:642 y:410
		_sm_do_the_actions_6 = OperatableStateMachine(outcomes=['finished', 'failed', 'critical fail'], input_keys=['ActionForms', 'OriginalPose'])

		with _sm_do_the_actions_6:
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
										FlexibleCheckConditionState(predicate=lambda x: x[1] < len(x[0]), input_keys=["ActionForms", "index"]),
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


		# x:424 y:175
		_sm_initialisation_7 = OperatableStateMachine(outcomes=['done'], input_keys=['PositionBras', 'EntryName'])

		with _sm_initialisation_7:
			# x:62 y:79
			OperatableStateMachine.add('Action_Pass_Door',
										self.use_behavior(Action_Pass_DoorSM, 'Initialisation/Action_Pass_Door'),
										transitions={'Done': 'set step', 'Fail': 'done'},
										autonomy={'Done': Autonomy.Inherit, 'Fail': Autonomy.Inherit},
										remapping={'DoorName': 'EntryName'})

			# x:70 y:306
			OperatableStateMachine.add('set story',
										Set_Story(titre="GPSR", storyline=[]),
										transitions={'done': 'bras en lair'},
										autonomy={'done': Autonomy.Off})

			# x:288 y:375
			OperatableStateMachine.add('say start',
										SaraSay(sentence="I'm ready to start the GPSR scenario.", input_keys=[], emotion=1, block=True),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off})

			# x:78 y:205
			OperatableStateMachine.add('set step',
										Set_a_step(step=0),
										transitions={'done': 'set story'},
										autonomy={'done': Autonomy.Off})

			# x:101 y:395
			OperatableStateMachine.add('bras en lair',
										MoveitMove(move=True, waitForExecution=False, group="RightArm"),
										transitions={'done': 'say start', 'failed': 'say start'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'PositionBras'})



		with _state_machine:
			# x:33 y:103
			OperatableStateMachine.add('Initialisation',
										_sm_initialisation_7,
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Inherit},
										remapping={'PositionBras': 'PositionBras', 'EntryName': 'EntryName'})

			# x:767 y:196
			OperatableStateMachine.add('Do the actions',
										_sm_do_the_actions_6,
										transitions={'finished': 'say succseed', 'failed': 'Fail state', 'critical fail': 'critical'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical fail': Autonomy.Inherit},
										remapping={'ActionForms': 'ActionForms', 'OriginalPose': 'OriginalPose'})

			# x:250 y:126
			OperatableStateMachine.add('Fail state',
										_sm_fail_state_5,
										transitions={'finished': 'lift head', 'failed': 'critical'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'StartPosition': 'StartPosition'})

			# x:250 y:257
			OperatableStateMachine.add('critical',
										SaraSay(sentence="Critical failure! I require medical assistance.", input_keys=[], emotion=1, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:52 y:468
			OperatableStateMachine.add('for 3',
										ForLoop(repeat=3),
										transitions={'do': 'GetOriginalPose', 'end': 'End'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index'})

			# x:747 y:475
			OperatableStateMachine.add('say succseed',
										SaraSay(sentence="I succeed my mission.", input_keys=[], emotion=1, block=True),
										transitions={'done': 'for 3'},
										autonomy={'done': Autonomy.Off})

			# x:204 y:368
			OperatableStateMachine.add('Interact operator',
										_sm_interact_operator_4,
										transitions={'fail': 'critical', 'understood': 'set step'},
										autonomy={'fail': Autonomy.Inherit, 'understood': Autonomy.Inherit},
										remapping={'ActionForms': 'ActionForms', 'sentence': 'sentence'})

			# x:553 y:316
			OperatableStateMachine.add('set story',
										StoryboardSetStoryFromAction(),
										transitions={'done': 'Do the actions'},
										autonomy={'done': Autonomy.Off},
										remapping={'titre': 'title', 'actionList': 'ActionForms'})

			# x:404 y:377
			OperatableStateMachine.add('set step',
										Set_a_step(step=0),
										transitions={'done': 'set story'},
										autonomy={'done': Autonomy.Off})

			# x:41 y:375
			OperatableStateMachine.add('GetOriginalPose',
										Get_Robot_Pose(),
										transitions={'done': 'Interact operator'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose': 'OriginalPose'})

			# x:37 y:564
			OperatableStateMachine.add('End',
										_sm_end_3,
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Inherit},
										remapping={'ExitName': 'ExitName'})

			# x:30 y:288
			OperatableStateMachine.add('lift head',
										SaraSetHeadAngle(pitch=-0.3, yaw=0),
										transitions={'done': 'GetOriginalPose'},
										autonomy={'done': Autonomy.Off})

			# x:48 y:23
			OperatableStateMachine.add('ContinueButton',
										ContinueButton(),
										transitions={'true': 'Initialisation', 'false': 'Initialisation'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off})

			# x:21 y:185
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(Action_MoveSM, 'Action_Move'),
										transitions={'finished': 'lift head', 'failed': 'critical'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'StartPosition'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
