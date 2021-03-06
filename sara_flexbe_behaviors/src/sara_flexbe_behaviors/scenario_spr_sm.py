#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.continue_button import ContinueButton
from flexbe_states.wait_state import WaitState
from sara_flexbe_states.WonderlandGetPersonStat import WonderlandGetPersonStat
from sara_flexbe_states.sara_say import SaraSay
from flexbe_states.flexible_calculation_state import FlexibleCalculationState
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.SetRosParamKey import SetRosParamKey
from flexbe_states.log_key_state import LogKeyState
from sara_flexbe_states.list_entities_by_name import list_entities_by_name
from sara_flexbe_states.get_speech import GetSpeech
from sara_flexbe_states.sara_nlu_spr import SaraNLUspr
from sara_flexbe_states.set_a_step import Set_a_step
from sara_flexbe_states.for_loop import ForLoop
from sara_flexbe_states.KeepLookingAt import KeepLookingAt
from sara_flexbe_behaviors.action_turn_sm import action_turnSM
from sara_flexbe_states.sara_set_head_angle import SaraSetHeadAngle
from sara_flexbe_behaviors.actionwrapper_move_sm import ActionWrapper_MoveSM
from sara_flexbe_states.story import Set_Story
from sara_flexbe_states.WonderlandClearPeoples import WonderlandClearPeoples
from sara_flexbe_states.moveit_move import MoveitMove
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_states.WonderlandAddUpdatePeople import WonderlandAddUpdatePeople
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu Jun 07 2018
@author: Lucas Maurice
'''
class Scenario_SPRSM(Behavior):
	'''
	Contient le scenario SPR.
	'''


	def __init__(self):
		super(Scenario_SPRSM, self).__init__()
		self.name = 'Scenario_SPR'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(action_turnSM, 'Waiting And Turn/action_turn')
		self.add_behavior(ActionWrapper_MoveSM, 'Leave Arena')
		self.add_behavior(ActionWrapper_MoveSM, 'Join Area/Join Arena')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:

		# O 100 629 
		# 0 - Waiting Begining|n1 - Join Game Room|n2 - Waiting Crowd Placement|n3 - Analysing Crowd|n4 - Begin Game|n5 - Find Operator|n6 - Question 1|n7 - Question 2|n8 - Question 3|n9 - Question 4|n10 - Question 5|n11 - Go out



	def create(self):
		# x:1474 y:331, x:56 y:575
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.half_turn = 3.1416
		_state_machine.userdata.person = "person"
		_state_machine.userdata.operator_param = "behavior/Operaror/Id"
		_state_machine.userdata.join = ["Move", "spr/initialpose"]
		_state_machine.userdata.leave = ["Move", "door2/exit"]

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:1182 y:163
		_sm_rotate_0 = OperatableStateMachine(outcomes=['finished'])

		with _sm_rotate_0:
			# x:103 y:61
			OperatableStateMachine.add('Look Left',
										SaraSetHeadAngle(pitch=-0.35, yaw=0.5),
										transitions={'done': 'Rotate Left'},
										autonomy={'done': Autonomy.Off})

			# x:794 y:54
			OperatableStateMachine.add('Look Right',
										SaraSetHeadAngle(pitch=-0.35, yaw=-0.5),
										transitions={'done': 'Rotate Right'},
										autonomy={'done': Autonomy.Off})

			# x:325 y:61
			OperatableStateMachine.add('Rotate Left',
										WaitState(wait_time=8),
										transitions={'done': 'Look Center'},
										autonomy={'done': Autonomy.Off})

			# x:961 y:65
			OperatableStateMachine.add('Rotate Right',
										WaitState(wait_time=4),
										transitions={'done': 'Look Center 2'},
										autonomy={'done': Autonomy.Off})

			# x:1115 y:62
			OperatableStateMachine.add('Look Center 2',
										SaraSetHeadAngle(pitch=0.1, yaw=0),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:484 y:54
			OperatableStateMachine.add('Look Center',
										SaraSetHeadAngle(pitch=-0.35, yaw=0),
										transitions={'done': 'Rotate Center'},
										autonomy={'done': Autonomy.Off})

			# x:657 y:49
			OperatableStateMachine.add('Rotate Center',
										WaitState(wait_time=4),
										transitions={'done': 'Look Right'},
										autonomy={'done': Autonomy.Off})


		# x:30 y:458
		_sm_follow_head_1 = OperatableStateMachine(outcomes=['end'], input_keys=['person'])

		with _sm_follow_head_1:
			# x:214 y:48
			OperatableStateMachine.add('list all entities',
										list_entities_by_name(frontality_level=0.5, distance_max=10),
										transitions={'found': 'Get Nearest', 'none_found': 'list all entities'},
										autonomy={'found': Autonomy.Off, 'none_found': Autonomy.Off},
										remapping={'name': 'person', 'entity_list': 'entity_list', 'number': 'number'})

			# x:456 y:51
			OperatableStateMachine.add('Get Nearest',
										CalculationState(calculation=lambda x: x[0].ID),
										transitions={'done': 'look'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'entity_list', 'output_value': 'ID'})

			# x:291 y:177
			OperatableStateMachine.add('look',
										KeepLookingAt(),
										transitions={'failed': 'list all entities'},
										autonomy={'failed': Autonomy.Off},
										remapping={'ID': 'ID'})


		# x:12 y:125, x:1130 y:515
		_sm_nlu_2 = OperatableStateMachine(outcomes=['finished', 'failed'])

		with _sm_nlu_2:
			# x:156 y:37
			OperatableStateMachine.add('say ask',
										SaraSay(sentence="You can ask me your questions.", input_keys=[], emotion=1, block=True),
										transitions={'done': 'Loop Questions'},
										autonomy={'done': Autonomy.Off})

			# x:1091 y:84
			OperatableStateMachine.add('Listen',
										GetSpeech(watchdog=10),
										transitions={'done': 'Engine', 'nothing': 'Listen', 'fail': 'Listen'},
										autonomy={'done': Autonomy.Off, 'nothing': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'words': 'sentence'})

			# x:1324 y:110
			OperatableStateMachine.add('Engine',
										SaraNLUspr(),
										transitions={'understood': 'Say_Answer', 'not_understood': 'Listen', 'fail': 'Listen'},
										autonomy={'understood': Autonomy.Off, 'not_understood': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'sentence': 'sentence', 'answer': 'answer'})

			# x:632 y:77
			OperatableStateMachine.add('Select Story',
										CalculationState(calculation=lambda x: x+6),
										transitions={'done': 'Set_a_step'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'index', 'output_value': 'story'})

			# x:874 y:78
			OperatableStateMachine.add('Set_a_step',
										Set_a_step(step=1),
										transitions={'done': 'Listen'},
										autonomy={'done': Autonomy.Off})

			# x:398 y:81
			OperatableStateMachine.add('Loop Questions',
										ForLoop(repeat=5),
										transitions={'do': 'Select Story', 'end': 'loop step'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index'})

			# x:439 y:252
			OperatableStateMachine.add('Say Blind Game',
										SaraSay(sentence="Let's play the blind game !", input_keys=[], emotion=1, block=True),
										transitions={'done': 'Loop Questions'},
										autonomy={'done': Autonomy.Off})

			# x:189 y:193
			OperatableStateMachine.add('loop step',
										ForLoop(repeat=1),
										transitions={'do': 'Say Blind Game', 'end': 'finished'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index'})

			# x:721 y:205
			OperatableStateMachine.add('Say_Answer',
										SaraSay(sentence=lambda x: str(x), input_keys=[], emotion=0, block=True),
										transitions={'done': 'Loop Questions'},
										autonomy={'done': Autonomy.Off})


		# x:817 y:123, x:130 y:458
		_sm_analyse_crowd_3 = OperatableStateMachine(outcomes=['finished', 'error'])

		with _sm_analyse_crowd_3:
			# x:87 y:97
			OperatableStateMachine.add('clear database',
										WonderlandClearPeoples(),
										transitions={'done': 'Rotate', 'error': 'error'},
										autonomy={'done': Autonomy.Off, 'error': Autonomy.Off})

			# x:531 y:112
			OperatableStateMachine.add('Add Update Persons',
										WonderlandAddUpdatePeople(),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:311 y:97
			OperatableStateMachine.add('Rotate',
										_sm_rotate_0,
										transitions={'finished': 'Add Update Persons'},
										autonomy={'finished': Autonomy.Inherit})


		# x:1203 y:11, x:1006 y:366
		_sm_init_scenario_4 = OperatableStateMachine(outcomes=['done', 'error'])

		with _sm_init_scenario_4:
			# x:30 y:42
			OperatableStateMachine.add('Generate Vizbox Story',
										Set_Story(titre="Speech and Person Recognition", storyline=["Waiting Begining","Join Game Room","Waiting Crowd Placement","Analysing Crowd","Begin Game","Find Operator","Question 1","Question 2","Question 3","Question 4","Question 5", "Leave Arena"]),
										transitions={'done': 'Set Story Step'},
										autonomy={'done': Autonomy.Off})

			# x:559 y:44
			OperatableStateMachine.add('WaitForBegining',
										ContinueButton(),
										transitions={'true': 'Reset Persons', 'false': 'Reset Persons'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off})

			# x:807 y:61
			OperatableStateMachine.add('Reset Persons',
										WonderlandClearPeoples(),
										transitions={'done': 'done', 'error': 'error'},
										autonomy={'done': Autonomy.Off, 'error': Autonomy.Off})

			# x:247 y:49
			OperatableStateMachine.add('Set Story Step',
										Set_a_step(step=0),
										transitions={'done': 'setIDLE'},
										autonomy={'done': Autonomy.Off})

			# x:388 y:208
			OperatableStateMachine.add('Reset Arm',
										MoveitMove(move=True, waitForExecution=True, group="RightArm", watchdog=15),
										transitions={'done': 'Reset Persons', 'failed': 'error'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'target'})

			# x:427 y:40
			OperatableStateMachine.add('setIDLE',
										SetKey(Value="IdlePose"),
										transitions={'done': 'Reset Arm'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'target'})


		# x:30 y:458, x:230 y:458
		_sm_join_area_5 = OperatableStateMachine(outcomes=['failed', 'finished'], input_keys=['join'])

		with _sm_join_area_5:
			# x:95 y:40
			OperatableStateMachine.add('Say Join Area',
										SaraSay(sentence="I will join the playing room !", input_keys=[], emotion=1, block=True),
										transitions={'done': 'Join Arena'},
										autonomy={'done': Autonomy.Off})

			# x:92 y:134
			OperatableStateMachine.add('Join Arena',
										self.use_behavior(ActionWrapper_MoveSM, 'Join Area/Join Arena'),
										transitions={'finished': 'finished', 'failed': 'failed', 'critical_fail': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'join'})


		# x:489 y:56, x:604 y:278
		_sm_waiting_and_turn_6 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['half_turn'])

		with _sm_waiting_and_turn_6:
			# x:50 y:51
			OperatableStateMachine.add('Want Play',
										SaraSay(sentence="Hum, I want to play riddles !", input_keys=[], emotion=1, block=True),
										transitions={'done': 'Wait 10s'},
										autonomy={'done': Autonomy.Off})

			# x:272 y:121
			OperatableStateMachine.add('action_turn',
										self.use_behavior(action_turnSM, 'Waiting And Turn/action_turn'),
										transitions={'finished': 'finished', 'failed': 'Cant turn'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'rotation': 'half_turn'})

			# x:437 y:240
			OperatableStateMachine.add('Cant turn',
										SaraSay(sentence="I can't turn !", input_keys=[], emotion=1, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:63 y:178
			OperatableStateMachine.add('Wait 10s',
										WaitState(wait_time=10),
										transitions={'done': 'Look In Front Of'},
										autonomy={'done': Autonomy.Off})

			# x:61 y:260
			OperatableStateMachine.add('Look In Front Of',
										SaraSetHeadAngle(pitch=0, yaw=0),
										transitions={'done': 'action_turn'},
										autonomy={'done': Autonomy.Off})


		# x:472 y:69, x:476 y:113, x:470 y:196, x:330 y:458, x:430 y:458
		_sm_questions_7 = ConcurrencyContainer(outcomes=['finished', 'failed'], input_keys=['person'], conditions=[
										('finished', [('NLU', 'finished')]),
										('failed', [('NLU', 'failed')]),
										('finished', [('Follow Head', 'end')])
										])

		with _sm_questions_7:
			# x:85 y:58
			OperatableStateMachine.add('NLU',
										_sm_nlu_2,
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:84 y:185
			OperatableStateMachine.add('Follow Head',
										_sm_follow_head_1,
										transitions={'end': 'finished'},
										autonomy={'end': Autonomy.Inherit},
										remapping={'person': 'person'})


		# x:283 y:294, x:60 y:571
		_sm_find_operator_8 = OperatableStateMachine(outcomes=['not_found', 'done'], input_keys=['person', 'operator_param'])

		with _sm_find_operator_8:
			# x:51 y:40
			OperatableStateMachine.add('Ask Player',
										SaraSay(sentence="Who wan't to play with me ?", input_keys=[], emotion=1, block=True),
										transitions={'done': 'Wait Operator'},
										autonomy={'done': Autonomy.Off})

			# x:39 y:297
			OperatableStateMachine.add('Get operator id',
										CalculationState(calculation=lambda x: x.entities[0].face.id),
										transitions={'done': 'Set Operator Id'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'entity_list', 'output_value': 'operator'})

			# x:33 y:384
			OperatableStateMachine.add('Set Operator Id',
										SetRosParamKey(),
										transitions={'done': 'Operator Id'},
										autonomy={'done': Autonomy.Off},
										remapping={'Value': 'operator_param', 'ParamName': 'operator'})

			# x:46 y:117
			OperatableStateMachine.add('Wait Operator',
										WaitState(wait_time=6),
										transitions={'done': 'Find Operator'},
										autonomy={'done': Autonomy.Off})

			# x:35 y:495
			OperatableStateMachine.add('Operator Id',
										LogKeyState(text="Operator find. Id: {}", severity=Logger.REPORT_HINT),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'operator'})

			# x:30 y:205
			OperatableStateMachine.add('Find Operator',
										list_entities_by_name(frontality_level=0.5, distance_max=10),
										transitions={'found': 'Get operator id', 'none_found': 'Find Operator'},
										autonomy={'found': Autonomy.Off, 'none_found': Autonomy.Off},
										remapping={'name': 'person', 'entity_list': 'entity_list', 'number': 'number'})


		# x:703 y:198, x:88 y:199
		_sm_tell_basic_stats_9 = OperatableStateMachine(outcomes=['finished', 'failed'])

		with _sm_tell_basic_stats_9:
			# x:50 y:40
			OperatableStateMachine.add('wait',
										WaitState(wait_time=0),
										transitions={'done': 'GetPeopleStats'},
										autonomy={'done': Autonomy.Off})

			# x:218 y:43
			OperatableStateMachine.add('GetPeopleStats',
										WonderlandGetPersonStat(),
										transitions={'done': 'GenerateSentence', 'none': 'Nobody', 'error': 'failed'},
										autonomy={'done': Autonomy.Off, 'none': Autonomy.Off, 'error': Autonomy.Off},
										remapping={'women': 'women', 'men': 'men', 'others': 'others'})

			# x:466 y:46
			OperatableStateMachine.add('Nobody',
										SaraSay(sentence="There is nobody here !", input_keys=[], emotion=1, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:162 y:243
			OperatableStateMachine.add('GenerateSentence',
										FlexibleCalculationState(calculation=lambda x: "There is " + str(x[0]+x[1]+x[2]) + " persons.", input_keys=['men','women','others']),
										transitions={'done': 'Tell_Stats'},
										autonomy={'done': Autonomy.Off},
										remapping={'men': 'men', 'women': 'women', 'others': 'others', 'output_value': 'sentence'})

			# x:151 y:345
			OperatableStateMachine.add('Generate Sentence 2',
										FlexibleCalculationState(calculation=lambda x: "I recognize " + str(x[1]) + " women and " + str(x[0]) + " men.", input_keys=['men','women','others']),
										transitions={'done': 'Tell_Stats 2'},
										autonomy={'done': Autonomy.Off},
										remapping={'men': 'men', 'women': 'women', 'others': 'others', 'output_value': 'sentence'})

			# x:380 y:172
			OperatableStateMachine.add('Tell_Stats',
										SaraSay(sentence=lambda x: x, input_keys=[], emotion=0, block=True),
										transitions={'done': 'Generate Sentence 2'},
										autonomy={'done': Autonomy.Off})

			# x:409 y:276
			OperatableStateMachine.add('Tell_Stats 2',
										SaraSay(sentence=lambda x: x, input_keys=[], emotion=0, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})



		with _state_machine:
			# x:30 y:40
			OperatableStateMachine.add('continue',
										ContinueButton(),
										transitions={'true': 'Init Scenario', 'false': 'Init Scenario'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off})

			# x:715 y:127
			OperatableStateMachine.add('Tell basic stats',
										_sm_tell_basic_stats_9,
										transitions={'finished': 'Set Find Operator', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:899 y:126
			OperatableStateMachine.add('Find Operator',
										_sm_find_operator_8,
										transitions={'not_found': 'Find Operator', 'done': 'Questions'},
										autonomy={'not_found': Autonomy.Inherit, 'done': Autonomy.Inherit},
										remapping={'person': 'person', 'operator_param': 'operator_param'})

			# x:1120 y:126
			OperatableStateMachine.add('Questions',
										_sm_questions_7,
										transitions={'finished': 'set head', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'person': 'person'})

			# x:343 y:49
			OperatableStateMachine.add('Set Story Waiting',
										Set_a_step(step=2),
										transitions={'done': 'Waiting And Turn'},
										autonomy={'done': Autonomy.Off})

			# x:532 y:48
			OperatableStateMachine.add('Set Analyse',
										Set_a_step(step=3),
										transitions={'done': 'Analyse Crowd'},
										autonomy={'done': Autonomy.Off})

			# x:696 y:47
			OperatableStateMachine.add('Set Begin Game',
										Set_a_step(step=4),
										transitions={'done': 'Tell basic stats'},
										autonomy={'done': Autonomy.Off})

			# x:899 y:49
			OperatableStateMachine.add('Set Find Operator',
										Set_a_step(step=5),
										transitions={'done': 'Find Operator'},
										autonomy={'done': Autonomy.Off})

			# x:332 y:127
			OperatableStateMachine.add('Waiting And Turn',
										_sm_waiting_and_turn_6,
										transitions={'finished': 'Set Analyse', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'half_turn': 'half_turn'})

			# x:1333 y:232
			OperatableStateMachine.add('Set Go Out',
										Set_a_step(step=11),
										transitions={'done': 'Say And Of Game'},
										autonomy={'done': Autonomy.Off})

			# x:1517 y:148
			OperatableStateMachine.add('Leave Arena',
										self.use_behavior(ActionWrapper_MoveSM, 'Leave Arena'),
										transitions={'finished': 'finished', 'failed': 'finished', 'critical_fail': 'finished'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'leave'})

			# x:176 y:42
			OperatableStateMachine.add('Set Join',
										Set_a_step(step=1),
										transitions={'done': 'Set Story Waiting'},
										autonomy={'done': Autonomy.Off})

			# x:177 y:120
			OperatableStateMachine.add('Join Area',
										_sm_join_area_5,
										transitions={'failed': 'failed', 'finished': 'Set Story Waiting'},
										autonomy={'failed': Autonomy.Inherit, 'finished': Autonomy.Inherit},
										remapping={'join': 'join'})

			# x:1302 y:140
			OperatableStateMachine.add('Say And Of Game',
										SaraSay(sentence="The game is finished. I will leave the arena. Thank you for playing with me.", input_keys=[], emotion=1, block=True),
										transitions={'done': 'Leave Arena'},
										autonomy={'done': Autonomy.Off})

			# x:1120 y:237
			OperatableStateMachine.add('set head',
										SaraSetHeadAngle(pitch=-0.2, yaw=0),
										transitions={'done': 'Set Go Out'},
										autonomy={'done': Autonomy.Off})

			# x:34 y:130
			OperatableStateMachine.add('Init Scenario',
										_sm_init_scenario_4,
										transitions={'done': 'Set Join', 'error': 'failed'},
										autonomy={'done': Autonomy.Inherit, 'error': Autonomy.Inherit})

			# x:517 y:124
			OperatableStateMachine.add('Analyse Crowd',
										_sm_analyse_crowd_3,
										transitions={'finished': 'Set Begin Game', 'error': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'error': Autonomy.Inherit})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
