#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_scenario_gpsr')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_states.moveit_move import MoveitMove
from sara_flexbe_states.story import Set_Story
from sara_flexbe_states.WonderlandGetEntityVerbal import WonderlandGetEntityVerbal
from behavior_action_pass_door.action_pass_door_sm import Action_Pass_DoorSM
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.set_a_step import Set_a_step
from sara_flexbe_states.sara_say import SaraSay
from flexbe_states.flexible_calculation_state import FlexibleCalculationState
from flexbe_states.flexible_check_condition_state import FlexibleCheckConditionState
from behavior_action_executor.action_executor_sm import Action_ExecutorSM
from sara_flexbe_states.StoryboardSetStepKey import StoryboardSetStepKey
from sara_flexbe_states.GetRosParam import GetRosParam
from sara_flexbe_states.sara_say_key import SaraSayKey
from behavior_actionwrapper_move.actionwrapper_move_sm import ActionWrapper_MoveSM
from sara_flexbe_states.for_loop import ForLoop
from sara_flexbe_states.sara_nlu_gpsr import SaraNLUgpsr
from sara_flexbe_states.get_speech import GetSpeech
from sara_flexbe_states.list_entities_by_name import list_entities_by_name
from behavior_action_look_at_face.action_look_at_face_sm import action_look_at_faceSM
from sara_flexbe_states.StoryboardSetStoryKey import StoryboardSetStoryFromAction
from sara_flexbe_states.get_robot_pose import Get_Robot_Pose
from sara_flexbe_states.sara_set_head_angle import SaraSetHeadAngle
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
		self.add_behavior(ActionWrapper_MoveSM, 'Fail state/ActionWrapper_Move')
		self.add_behavior(action_look_at_faceSM, 'Interact operator/look at op/action_look_at_face')
		self.add_behavior(Action_ExecutorSM, 'Action_Executor')
		self.add_behavior(Action_Pass_DoorSM, 'End/Action_Pass_Door')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:391 y:586, x:438 y:304
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.ActionGoToStart = ["Move", "spr/waypoint1"]
		_state_machine.userdata.PositionBras = "IdlePose"
		_state_machine.userdata.title = "GPSR"
		_state_machine.userdata.EntryName = "rips/waypoint1"
		_state_machine.userdata.ExitName = "rips/waypoint2"

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
										list_entities_by_name(frontality_level=0.5, distance_max=10),
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


		# x:97 y:612
		_sm_end_2 = OperatableStateMachine(outcomes=['done'], input_keys=['ExitName'])

		with _sm_end_2:
			# x:30 y:40
			OperatableStateMachine.add('win',
										SaraSay(sentence="Thank you. I'm going now.", emotion=1, block=True),
										transitions={'done': 'set cont'},
										autonomy={'done': Autonomy.Off})

			# x:186 y:221
			OperatableStateMachine.add('get exit',
										WonderlandGetEntityVerbal(),
										transitions={'one': 'get exit pose', 'multiple': 'get exit pose', 'none': 'get exit pose', 'error': 'get exit pose'},
										autonomy={'one': Autonomy.Off, 'multiple': Autonomy.Off, 'none': Autonomy.Off, 'error': Autonomy.Off},
										remapping={'name': 'ExitName', 'containers': 'containers', 'entities': 'entities'})

			# x:197 y:337
			OperatableStateMachine.add('get exit pose',
										CalculationState(calculation=lambda x: x.waypoint),
										transitions={'done': 'Action_Pass_Door'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'entities', 'output_value': 'pose'})

			# x:166 y:436
			OperatableStateMachine.add('Action_Pass_Door',
										self.use_behavior(Action_Pass_DoorSM, 'End/Action_Pass_Door'),
										transitions={'Done': 'say yay', 'Fail': 'done'},
										autonomy={'Done': Autonomy.Inherit, 'Fail': Autonomy.Inherit},
										remapping={'DoorPose1': 'pose'})

			# x:209 y:59
			OperatableStateMachine.add('set cont',
										SetKey(Value=""),
										transitions={'done': 'get exit'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'containers'})

			# x:191 y:570
			OperatableStateMachine.add('say yay',
										SaraSay(sentence="I did it. I'm the best robot.", emotion=1, block=True),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off})


		# x:320 y:82, x:322 y:143, x:265 y:407, x:306 y:225, x:430 y:324
		_sm_interact_operator_3 = ConcurrencyContainer(outcomes=['fail', 'understood'], output_keys=['ActionForms', 'sentence'], conditions=[
										('understood', [('Get Commands', 'understood')]),
										('fail', [('Get Commands', 'fail')]),
										('fail', [('look at op', 'fail')])
										])

		with _sm_interact_operator_3:
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


		# x:356 y:519, x:581 y:195
		_sm_fail_state_4 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['ActionGoToStart'])

		with _sm_fail_state_4:
			# x:36 y:29
			OperatableStateMachine.add('say failed',
										SaraSay(sentence="I failed. I'm going back to tell my master.", emotion=1, block=True),
										transitions={'done': 'ActionWrapper_Move'},
										autonomy={'done': Autonomy.Off})

			# x:22 y:505
			OperatableStateMachine.add('get error',
										GetRosParam(ParamName="behavior/GPSR/CauseOfFailure"),
										transitions={'done': 'say error', 'failed': 'finished'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'Value': 'Error'})

			# x:110 y:584
			OperatableStateMachine.add('say error',
										SaraSayKey(Format=lambda x: "Sorry, I failed because "+x, emotion=1, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'Error'})

			# x:21 y:163
			OperatableStateMachine.add('ActionWrapper_Move',
										self.use_behavior(ActionWrapper_MoveSM, 'Fail state/ActionWrapper_Move'),
										transitions={'finished': 'get error', 'failed': 'failed', 'critical_fail': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'ActionGoToStart'})


		# x:588 y:141, x:590 y:545, x:642 y:410
		_sm_do_the_actions_5 = OperatableStateMachine(outcomes=['finished', 'failed', 'critical fail'], input_keys=['ActionForms', 'OriginalPose'])

		with _sm_do_the_actions_5:
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


		# x:371 y:386
		_sm_initialisation_6 = OperatableStateMachine(outcomes=['done'], input_keys=['PositionBras', 'EntryName'])

		with _sm_initialisation_6:
			# x:47 y:25
			OperatableStateMachine.add('set container',
										SetKey(Value=None),
										transitions={'done': 'get entry door'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'containers'})

			# x:135 y:523
			OperatableStateMachine.add('bras en lair',
										MoveitMove(move=True, waitForExecution=False, group="RightArm"),
										transitions={'done': 'say start', 'failed': 'say start'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'PositionBras'})

			# x:33 y:516
			OperatableStateMachine.add('set story',
										Set_Story(titre="GPSR", storyline=[]),
										transitions={'done': 'bras en lair'},
										autonomy={'done': Autonomy.Off})

			# x:31 y:119
			OperatableStateMachine.add('get entry door',
										WonderlandGetEntityVerbal(),
										transitions={'one': 'get pos', 'multiple': 'get pos', 'none': 'say no entry', 'error': 'say no entry'},
										autonomy={'one': Autonomy.Off, 'multiple': Autonomy.Off, 'none': Autonomy.Off, 'error': Autonomy.Off},
										remapping={'name': 'EntryName', 'containers': 'containers', 'entities': 'entitie'})

			# x:30 y:317
			OperatableStateMachine.add('Action_Pass_Door',
										self.use_behavior(Action_Pass_DoorSM, 'Initialisation/Action_Pass_Door'),
										transitions={'Done': 'set step', 'Fail': 'done'},
										autonomy={'Done': Autonomy.Inherit, 'Fail': Autonomy.Inherit},
										remapping={'DoorPose1': 'pose'})

			# x:54 y:248
			OperatableStateMachine.add('get pos',
										CalculationState(calculation=lambda x: x.waypoint),
										transitions={'done': 'Action_Pass_Door'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'entitie', 'output_value': 'pose'})

			# x:45 y:425
			OperatableStateMachine.add('set step',
										Set_a_step(step=0),
										transitions={'done': 'set story'},
										autonomy={'done': Autonomy.Off})

			# x:284 y:527
			OperatableStateMachine.add('say start',
										SaraSay(sentence="I'm ready to start the GPSR scenario.", emotion=1, block=True),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off})

			# x:273 y:103
			OperatableStateMachine.add('say no entry',
										SaraSay(sentence="Wait. There is no entry door? What!", emotion=1, block=True),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off})



		with _state_machine:
			# x:30 y:288
			OperatableStateMachine.add('lift head',
										SaraSetHeadAngle(pitch=0.3, yaw=0),
										transitions={'done': 'GetOriginalPose'},
										autonomy={'done': Autonomy.Off})

			# x:767 y:196
			OperatableStateMachine.add('Do the actions',
										_sm_do_the_actions_5,
										transitions={'finished': 'say succseed', 'failed': 'Fail state', 'critical fail': 'critical'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical fail': Autonomy.Inherit},
										remapping={'ActionForms': 'ActionForms', 'OriginalPose': 'OriginalPose'})

			# x:376 y:115
			OperatableStateMachine.add('Fail state',
										_sm_fail_state_4,
										transitions={'finished': 'lift head', 'failed': 'critical'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'ActionGoToStart': 'ActionGoToStart'})

			# x:238 y:272
			OperatableStateMachine.add('critical',
										SaraSay(sentence="Critical failure! I require medical assistance.", emotion=1, block=True),
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
										SaraSay(sentence="I succeed my mission. I'm going back", emotion=1, block=True),
										transitions={'done': 'for 3'},
										autonomy={'done': Autonomy.Off})

			# x:204 y:368
			OperatableStateMachine.add('Interact operator',
										_sm_interact_operator_3,
										transitions={'fail': 'critical', 'understood': 'set step'},
										autonomy={'fail': Autonomy.Inherit, 'understood': Autonomy.Inherit},
										remapping={'ActionForms': 'ActionForms', 'sentence': 'sentence'})

			# x:29 y:186
			OperatableStateMachine.add('Action_Executor',
										self.use_behavior(Action_ExecutorSM, 'Action_Executor'),
										transitions={'finished': 'lift head', 'failed': 'critical', 'critical_fail': 'critical'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'ActionGoToStart'})

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
										_sm_end_2,
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Inherit},
										remapping={'ExitName': 'ExitName'})

			# x:36 y:26
			OperatableStateMachine.add('Initialisation',
										_sm_initialisation_6,
										transitions={'done': 'Action_Executor'},
										autonomy={'done': Autonomy.Inherit},
										remapping={'PositionBras': 'PositionBras', 'EntryName': 'EntryName'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
