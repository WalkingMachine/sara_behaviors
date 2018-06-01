#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_scenario_gpsr')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.get_robot_pose import Get_Robot_Pose
from sara_flexbe_states.SetKey import SetKey
from flexbe_states.decision_state import DecisionState
from behavior_actionwrapper_answer.actionwrapper_answer_sm import ActionWrapper_AnswerSM
from behavior_actionwrapper_ask.actionwrapper_ask_sm import ActionWrapper_AskSM
from behavior_actionwrapper_bring.actionwrapper_bring_sm import ActionWrapper_BringSM
from behavior_actionwrapper_confirm.actionwrapper_confirm_sm import ActionWrapper_ConfirmSM
from behavior_actionwrapper_count.actionwrapper_count_sm import ActionWrapper_CountSM
from behavior_actionwrapper_find.actionwrapper_find_sm import ActionWrapper_FindSM
from behavior_actionwrapper_follow.actionwrapper_follow_sm import ActionWrapper_FollowSM
from behavior_actionwrapper_give.actionwrapper_give_sm import ActionWrapper_GiveSM
from behavior_actionwrapper_move.actionwrapper_move_sm import ActionWrapper_MoveSM
from behavior_actionwrapper_pick.actionwrapper_pick_sm import ActionWrapper_PickSM
from behavior_actionwrapper_place.actionwrapper_place_sm import ActionWrapper_PlaceSM
from behavior_actionwrapper_say.actionwrapper_say_sm import ActionWrapper_SaySM
from flexbe_states.flexible_calculation_state import FlexibleCalculationState
from flexbe_states.flexible_check_condition_state import FlexibleCheckConditionState
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.sara_say_key import SaraSayKey
from behavior_action_move.action_move_sm import Action_MoveSM
from sara_flexbe_states.get_speech import GetSpeech
from sara_flexbe_states.sara_nlu import SaraNLU
from sara_flexbe_states.sara_say import SaraSay
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
		self.add_behavior(ActionWrapper_AnswerSM, 'Do the actions/Do TheAction/ActionWrapper_Answer')
		self.add_behavior(ActionWrapper_AskSM, 'Do the actions/Do TheAction/ActionWrapper_Ask')
		self.add_behavior(ActionWrapper_BringSM, 'Do the actions/Do TheAction/ActionWrapper_Bring')
		self.add_behavior(ActionWrapper_ConfirmSM, 'Do the actions/Do TheAction/ActionWrapper_Confirm')
		self.add_behavior(ActionWrapper_CountSM, 'Do the actions/Do TheAction/ActionWrapper_Count')
		self.add_behavior(ActionWrapper_FindSM, 'Do the actions/Do TheAction/ActionWrapper_Find')
		self.add_behavior(ActionWrapper_FollowSM, 'Do the actions/Do TheAction/ActionWrapper_Follow')
		self.add_behavior(ActionWrapper_GiveSM, 'Do the actions/Do TheAction/ActionWrapper_Give')
		self.add_behavior(ActionWrapper_MoveSM, 'Do the actions/Do TheAction/ActionWrapper_Move')
		self.add_behavior(ActionWrapper_PickSM, 'Do the actions/Do TheAction/ActionWrapper_Pick')
		self.add_behavior(ActionWrapper_PlaceSM, 'Do the actions/Do TheAction/ActionWrapper_Place')
		self.add_behavior(ActionWrapper_SaySM, 'Do the actions/Do TheAction/ActionWrapper_Say')
		self.add_behavior(Action_MoveSM, 'Do the actions/FailedAction/Action_Move')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:498 y:508, x:473 y:150
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:852 y:421
		_sm_failedaction_0 = OperatableStateMachine(outcomes=['finished'], input_keys=['Action', 'OriginalPose'])

		with _sm_failedaction_0:
			# x:76 y:55
			OperatableStateMachine.add('say',
										SaraSayKey(Format=lambda x: "Hum, I failed to "+str(x[0])+" the "+str(x[1])+". I need to tell my master.", emotion=1, block=True),
										transitions={'done': 'not rel'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'Action'})

			# x:376 y:62
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(Action_MoveSM, 'Do the actions/FailedAction/Action_Move'),
										transitions={'finished': 'finished', 'failed': 'finished'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'OriginalPose', 'relative': 'relative'})

			# x:235 y:60
			OperatableStateMachine.add('not rel',
										SetKey(Value=False),
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'relative'})


		# x:887 y:149, x:1172 y:362, x:1040 y:305
		_sm_do_theaction_1 = OperatableStateMachine(outcomes=['finished', 'failed', 'critical_fail'], input_keys=['Action'])

		with _sm_do_theaction_1:
			# x:28 y:298
			OperatableStateMachine.add('decideAction',
										DecisionState(outcomes=["Answer", "Ask", "Bring", "Confirm", "Count", "Find", "Follow", "Give", "Move", "Pick", "Place", "Say"], conditions=lambda x: x[0]),
										transitions={'Answer': 'ActionWrapper_Answer', 'Ask': 'ActionWrapper_Ask', 'Bring': 'ActionWrapper_Bring', 'Confirm': 'ActionWrapper_Confirm', 'Count': 'ActionWrapper_Count', 'Find': 'ActionWrapper_Find', 'Follow': 'ActionWrapper_Follow', 'Give': 'ActionWrapper_Give', 'Move': 'ActionWrapper_Move', 'Pick': 'ActionWrapper_Pick', 'Place': 'ActionWrapper_Place', 'Say': 'ActionWrapper_Say'},
										autonomy={'Answer': Autonomy.Off, 'Ask': Autonomy.Off, 'Bring': Autonomy.Off, 'Confirm': Autonomy.Off, 'Count': Autonomy.Off, 'Find': Autonomy.Off, 'Follow': Autonomy.Off, 'Give': Autonomy.Off, 'Move': Autonomy.Off, 'Pick': Autonomy.Off, 'Place': Autonomy.Off, 'Say': Autonomy.Off},
										remapping={'input_value': 'Action'})

			# x:356 y:3
			OperatableStateMachine.add('ActionWrapper_Answer',
										self.use_behavior(ActionWrapper_AnswerSM, 'Do the actions/Do TheAction/ActionWrapper_Answer'),
										transitions={'finished': 'finished', 'failed': 'failed', 'critical_fail': 'critical_fail'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit})

			# x:366 y:61
			OperatableStateMachine.add('ActionWrapper_Ask',
										self.use_behavior(ActionWrapper_AskSM, 'Do the actions/Do TheAction/ActionWrapper_Ask'),
										transitions={'finished': 'finished', 'failed': 'failed', 'critical_fail': 'critical_fail'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit})

			# x:359 y:120
			OperatableStateMachine.add('ActionWrapper_Bring',
										self.use_behavior(ActionWrapper_BringSM, 'Do the actions/Do TheAction/ActionWrapper_Bring'),
										transitions={'finished': 'finished', 'failed': 'failed', 'critical_fail': 'critical_fail'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'Action'})

			# x:351 y:178
			OperatableStateMachine.add('ActionWrapper_Confirm',
										self.use_behavior(ActionWrapper_ConfirmSM, 'Do the actions/Do TheAction/ActionWrapper_Confirm'),
										transitions={'finished': 'finished', 'failed': 'failed', 'critical_fail': 'critical_fail'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit})

			# x:358 y:237
			OperatableStateMachine.add('ActionWrapper_Count',
										self.use_behavior(ActionWrapper_CountSM, 'Do the actions/Do TheAction/ActionWrapper_Count'),
										transitions={'finished': 'finished', 'failed': 'failed', 'critical_fail': 'critical_fail'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit})

			# x:362 y:295
			OperatableStateMachine.add('ActionWrapper_Find',
										self.use_behavior(ActionWrapper_FindSM, 'Do the actions/Do TheAction/ActionWrapper_Find'),
										transitions={'finished': 'finished', 'failed': 'failed', 'critical_fail': 'critical_fail'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'Action'})

			# x:355 y:353
			OperatableStateMachine.add('ActionWrapper_Follow',
										self.use_behavior(ActionWrapper_FollowSM, 'Do the actions/Do TheAction/ActionWrapper_Follow'),
										transitions={'finished': 'finished', 'failed': 'failed', 'critical_fail': 'critical_fail'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'Action'})

			# x:359 y:412
			OperatableStateMachine.add('ActionWrapper_Give',
										self.use_behavior(ActionWrapper_GiveSM, 'Do the actions/Do TheAction/ActionWrapper_Give'),
										transitions={'finished': 'finished', 'failed': 'failed', 'critical_fail': 'critical_fail'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'Action'})

			# x:354 y:470
			OperatableStateMachine.add('ActionWrapper_Move',
										self.use_behavior(ActionWrapper_MoveSM, 'Do the actions/Do TheAction/ActionWrapper_Move'),
										transitions={'finished': 'finished', 'failed': 'failed', 'critical_fail': 'critical_fail'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'Action'})

			# x:355 y:528
			OperatableStateMachine.add('ActionWrapper_Pick',
										self.use_behavior(ActionWrapper_PickSM, 'Do the actions/Do TheAction/ActionWrapper_Pick'),
										transitions={'finished': 'finished', 'failed': 'failed', 'critical_fail': 'critical_fail'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'Action', 'ObjectInGripper': 'Action'})

			# x:353 y:587
			OperatableStateMachine.add('ActionWrapper_Place',
										self.use_behavior(ActionWrapper_PlaceSM, 'Do the actions/Do TheAction/ActionWrapper_Place'),
										transitions={'finished': 'finished', 'failed': 'failed', 'critical_fail': 'critical_fail'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'Action'})

			# x:352 y:645
			OperatableStateMachine.add('ActionWrapper_Say',
										self.use_behavior(ActionWrapper_SaySM, 'Do the actions/Do TheAction/ActionWrapper_Say'),
										transitions={'finished': 'finished', 'failed': 'failed', 'critical_fail': 'critical_fail'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit})


		# x:30 y:324, x:130 y:324
		_sm_get_commands_2 = OperatableStateMachine(outcomes=['fail', 'understood'], output_keys=['ActionForms'])

		with _sm_get_commands_2:
			# x:33 y:40
			OperatableStateMachine.add('GetSpeech',
										GetSpeech(watchdog=5),
										transitions={'done': 'SaraNLU', 'nothing': 'GetSpeech', 'fail': 'fail'},
										autonomy={'done': Autonomy.Off, 'nothing': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'words': 'sentence'})

			# x:30 y:226
			OperatableStateMachine.add('SaraNLU',
										SaraNLU(),
										transitions={'understood': 'understood', 'not_understood': 'say sorry', 'fail': 'say sorry'},
										autonomy={'understood': Autonomy.Off, 'not_understood': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'sentence': 'sentence', 'ActionForms': 'ActionForms'})

			# x:179 y:137
			OperatableStateMachine.add('say sorry',
										SaraSay(sentence="Sorry, I could not understand what you said.", emotion=1, block=True),
										transitions={'done': 'GetSpeech'},
										autonomy={'done': Autonomy.Off})


		# x:588 y:141, x:590 y:545, x:642 y:410
		_sm_do_the_actions_3 = OperatableStateMachine(outcomes=['finished', 'failed', 'critical fail'], input_keys=['ActionForms', 'OriginalPose'])

		with _sm_do_the_actions_3:
			# x:85 y:33
			OperatableStateMachine.add('set i',
										SetKey(Value=0),
										transitions={'done': 'is form?'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'index'})

			# x:27 y:352
			OperatableStateMachine.add('Do TheAction',
										_sm_do_theaction_1,
										transitions={'finished': '++i', 'failed': 'FailedAction', 'critical_fail': 'critical fail'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'Action'})

			# x:62 y:232
			OperatableStateMachine.add('GetForm',
										FlexibleCalculationState(calculation=lambda x: x[0][x[1]], input_keys=["ActionForms", "index"]),
										transitions={'done': 'Do TheAction'},
										autonomy={'done': Autonomy.Off},
										remapping={'ActionForms': 'ActionForms', 'index': 'index', 'output_value': 'Action'})

			# x:57 y:131
			OperatableStateMachine.add('is form?',
										FlexibleCheckConditionState(predicate=lambda x: x[0][x[1]] != None, input_keys=["ActionForms", "index"]),
										transitions={'true': 'GetForm', 'false': 'finished'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'ActionForms': 'ActionForms', 'index': 'index'})

			# x:331 y:223
			OperatableStateMachine.add('++i',
										CalculationState(calculation=lambda x: x+1),
										transitions={'done': 'is form?'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'index', 'output_value': 'index'})

			# x:27 y:522
			OperatableStateMachine.add('FailedAction',
										_sm_failedaction_0,
										transitions={'finished': 'failed'},
										autonomy={'finished': Autonomy.Inherit},
										remapping={'Action': 'Action', 'OriginalPose': 'OriginalPose'})



		with _state_machine:
			# x:82 y:43
			OperatableStateMachine.add('GetOriginalPose',
										Get_Robot_Pose(),
										transitions={'done': 'Get Commands'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose': 'OriginalPose'})

			# x:436 y:339
			OperatableStateMachine.add('Do the actions',
										_sm_do_the_actions_3,
										transitions={'finished': 'finished', 'failed': 'failed', 'critical fail': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical fail': Autonomy.Inherit},
										remapping={'ActionForms': 'ActionForms', 'OriginalPose': 'OriginalPose'})

			# x:76 y:134
			OperatableStateMachine.add('Get Commands',
										_sm_get_commands_2,
										transitions={'fail': 'failed', 'understood': 'Do the actions'},
										autonomy={'fail': Autonomy.Inherit, 'understood': Autonomy.Inherit},
										remapping={'ActionForms': 'ActionForms'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
