#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.get_robot_pose import Get_Robot_Pose
from sara_flexbe_behaviors.action_move_sm import Action_MoveSM as sara_flexbe_behaviors__Action_MoveSM
from sara_flexbe_states.get_reachable_waypoint import Get_Reacheable_Waypoint
from sara_flexbe_states.GetAttribute import GetAttribute
from sara_flexbe_states.sara_set_head_angle import SaraSetHeadAngle
from flexbe_states.wait_state import WaitState
from flexbe_states.log_key_state import LogKeyState
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.list_entities_by_name import list_entities_by_name
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_behaviors.action_turn_sm import action_turnSM as sara_flexbe_behaviors__action_turnSM
from flexbe_states.check_condition_state import CheckConditionState
from sara_flexbe_states.Filter import Filter
from sara_flexbe_states.KeepLookingAt import KeepLookingAt
from sara_flexbe_states.SetRosParam import SetRosParam
from sara_flexbe_states.regex_tester import RegexTester
from sara_flexbe_states.get_speech import GetSpeech
from sara_flexbe_behaviors.lookatclosest_sm import LookAtClosestSM as sara_flexbe_behaviors__LookAtClosestSM
from sara_flexbe_behaviors.init_sequence_sm import Init_SequenceSM as sara_flexbe_behaviors__Init_SequenceSM
from sara_flexbe_states.sara_follow import SaraFollow
from sara_flexbe_behaviors.action_pass_door_sm import Action_Pass_DoorSM as sara_flexbe_behaviors__Action_Pass_DoorSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Mar 18 2019
@author: Huynh-Anh Le
'''
class FarewellSM(Behavior):
	'''
	Some guests are tired, so they call the robot to retrieve their coat.  It’s raining outside and thereis only one umbrella, so the robot takes the guests one by one to their cab and returns with theumbrella
	'''


	def __init__(self):
		super(FarewellSM, self).__init__()
		self.name = 'Farewell'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'GetTaxi/Action_Move_to taxi')
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'GetTaxi/Action_Move')
		self.add_behavior(sara_flexbe_behaviors__action_turnSM, 'GetTaxi/Find umbrella/gettaxihuman/Rotation/action_turn')
		self.add_behavior(sara_flexbe_behaviors__LookAtClosestSM, 'confirm/LookAtClosest')
		self.add_behavior(sara_flexbe_behaviors__Init_SequenceSM, 'Init_Sequence')
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'nevermind/Action_Move')
		self.add_behavior(sara_flexbe_behaviors__Action_Pass_DoorSM, 'Action_Pass_Door')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:

		# O 832 253 
		# Retrieve coats

		# O 250 215 
		# On filtre les gens qui wavent et les femmes

		# O 224 438 
		# ON confirme que la personne veut partir

		# O 242 543 
		# on sapproche du taxi

		# O 821 211 
		# Il reste a prendre les manteaux|net ramener la deuxieme personne



	def create(self):
		# x:712 y:612, x:820 y:97
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.name = "person"
		_state_machine.userdata.distance = 1.05
		_state_machine.userdata.taxi = "taxi"
		_state_machine.userdata.umbrella = "umbrella"
		_state_machine.userdata.DoorName = "door_2_exit"

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:30 y:365, x:130 y:365, x:230 y:365
		_sm_get_closer_0 = ConcurrencyContainer(outcomes=['finished'], input_keys=['ID'], conditions=[
										('finished', [('follow', 'failed')]),
										('finished', [('wait 3', 'done')])
										])

		with _sm_get_closer_0:
			# x:46 y:131
			OperatableStateMachine.add('follow',
										SaraFollow(distance=1.15, ReplanPeriod=0.5),
										transitions={'failed': 'finished'},
										autonomy={'failed': Autonomy.Off},
										remapping={'ID': 'ID'})

			# x:223 y:134
			OperatableStateMachine.add('wait 3',
										WaitState(wait_time=12),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		# x:571 y:592
		_sm_scan_1 = OperatableStateMachine(outcomes=['finished'])

		with _sm_scan_1:
			# x:42 y:66
			OperatableStateMachine.add('Looking',
										SaraSay(sentence="I am trying to find who wants to leave. Please raise your hand.", input_keys=[], emotion=0, block=False),
										transitions={'done': 'center'},
										autonomy={'done': Autonomy.Off})

			# x:394 y:262
			OperatableStateMachine.add('right',
										SaraSetHeadAngle(pitch=0.1, yaw=-0.3),
										transitions={'done': 'w3'},
										autonomy={'done': Autonomy.Off})

			# x:206 y:372
			OperatableStateMachine.add('center2',
										SaraSetHeadAngle(pitch=0.1, yaw=0),
										transitions={'done': 'w4'},
										autonomy={'done': Autonomy.Off})

			# x:34 y:589
			OperatableStateMachine.add('w1',
										WaitState(wait_time=3),
										transitions={'done': 'center3'},
										autonomy={'done': Autonomy.Off})

			# x:413 y:159
			OperatableStateMachine.add('w2',
										WaitState(wait_time=3),
										transitions={'done': 'right'},
										autonomy={'done': Autonomy.Off})

			# x:415 y:370
			OperatableStateMachine.add('w3',
										WaitState(wait_time=3),
										transitions={'done': 'center2'},
										autonomy={'done': Autonomy.Off})

			# x:39 y:371
			OperatableStateMachine.add('w4',
										WaitState(wait_time=3),
										transitions={'done': 'left'},
										autonomy={'done': Autonomy.Off})

			# x:16 y:475
			OperatableStateMachine.add('left',
										SaraSetHeadAngle(pitch=0.1, yaw=0.3),
										transitions={'done': 'w1'},
										autonomy={'done': Autonomy.Off})

			# x:215 y:156
			OperatableStateMachine.add('center',
										SaraSetHeadAngle(pitch=0.1, yaw=0),
										transitions={'done': 'w2'},
										autonomy={'done': Autonomy.Off})

			# x:213 y:579
			OperatableStateMachine.add('center3',
										SaraSetHeadAngle(pitch=0.1, yaw=0),
										transitions={'done': 'wait'},
										autonomy={'done': Autonomy.Off})

			# x:393 y:576
			OperatableStateMachine.add('wait',
										WaitState(wait_time=4),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		# x:32 y:494, x:627 y:411
		_sm_filtregender_2 = OperatableStateMachine(outcomes=['none_found', 'found person'], input_keys=['name'], output_keys=['pronoun', 'person'])

		with _sm_filtregender_2:
			# x:109 y:51
			OperatableStateMachine.add('List',
										list_entities_by_name(frontality_level=0.5, distance_max=10),
										transitions={'found': 'FiltreWave', 'none_found': 'none_found'},
										autonomy={'found': Autonomy.Off, 'none_found': Autonomy.Off},
										remapping={'name': 'name', 'entity_list': 'entity_list', 'number': 'number'})

			# x:180 y:301
			OperatableStateMachine.add('FiltreExitingwomen',
										Filter(filter=lambda x: x.face.gender == "female"),
										transitions={'done': 'no female?'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_list': 'persons', 'output_list': 'female'})

			# x:174 y:386
			OperatableStateMachine.add('no female?',
										CheckConditionState(predicate=lambda x: len(x)>0),
										transitions={'true': 'set pronoun female', 'false': 'set pronoun male'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'female'})

			# x:374 y:312
			OperatableStateMachine.add('set pronoun female',
										SetKey(Value="miss"),
										transitions={'done': 'get first female'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'pronoun'})

			# x:181 y:476
			OperatableStateMachine.add('set pronoun male',
										SetKey(Value=""),
										transitions={'done': 'get first male'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'pronoun'})

			# x:599 y:290
			OperatableStateMachine.add('get first female',
										CalculationState(calculation=lambda x: x[0]),
										transitions={'done': 'found person'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'female', 'output_value': 'person'})

			# x:381 y:408
			OperatableStateMachine.add('get first male',
										CalculationState(calculation=lambda x: x[0]),
										transitions={'done': 'found person'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'persons', 'output_value': 'person'})

			# x:151 y:135
			OperatableStateMachine.add('FiltreWave',
										Filter(filter=lambda x: x.pose.right_arm_up or x.pose.left_arm_up),
										transitions={'done': 'if more than 0'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_list': 'entity_list', 'output_list': 'persons'})

			# x:157 y:217
			OperatableStateMachine.add('if more than 0',
										CheckConditionState(predicate=lambda x: len(x)>0),
										transitions={'true': 'FiltreExitingwomen', 'false': 'none_found'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'persons'})


		# x:772 y:208, x:360 y:516
		_sm_confirm_3 = OperatableStateMachine(outcomes=['false', 'done'], input_keys=['Person', 'pronoun'])

		with _sm_confirm_3:
			# x:66 y:83
			OperatableStateMachine.add('Confirm',
										SaraSay(sentence=lambda x: "would you like to leave, " + x[0] + "?", input_keys=["pronoun"], emotion=0, block=True),
										transitions={'done': 'GetSpeech'},
										autonomy={'done': Autonomy.Off},
										remapping={'pronoun': 'pronoun'})

			# x:82 y:504
			OperatableStateMachine.add('GetID',
										SetRosParam(ParamName="OpeID"),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off},
										remapping={'Value': 'ID'})

			# x:67 y:298
			OperatableStateMachine.add('if yes',
										RegexTester(regex=".*((yes)|(I do)|(yeah)|(sure)|(all right)|(verry well)|(of course)|(by all mean)|(certainly)|(absolutely)|(indeed)|(to)|(want)).*"),
										transitions={'true': 'get id', 'false': 'test no'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'text': 'text', 'result': 'result'})

			# x:84 y:409
			OperatableStateMachine.add('get id',
										GetAttribute(attributes=["ID"]),
										transitions={'done': 'GetID'},
										autonomy={'done': Autonomy.Off},
										remapping={'object': 'Person', 'ID': 'ID'})

			# x:87 y:188
			OperatableStateMachine.add('GetSpeech',
										GetSpeech(watchdog=10),
										transitions={'done': 'if yes', 'nothing': 'sayno', 'fail': 'if yes'},
										autonomy={'done': Autonomy.Off, 'nothing': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'words': 'text'})

			# x:259 y:193
			OperatableStateMachine.add('sayno',
										SaraSay(sentence="Sorry, did you say that you want to leave?", input_keys=[], emotion=0, block=True),
										transitions={'done': 'getno'},
										autonomy={'done': Autonomy.Off})

			# x:461 y:192
			OperatableStateMachine.add('getno',
										GetSpeech(watchdog=10),
										transitions={'done': 'getNO', 'nothing': 'get id', 'fail': 'get id'},
										autonomy={'done': Autonomy.Off, 'nothing': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'words': 'text'})

			# x:603 y:337
			OperatableStateMachine.add('getNO',
										RegexTester(regex=".*((yes)|(I do)|(yeah)|(sure)|(all right)|(verry well)|(of course)|(by all mean)|(certainly)|(absolutely)|(indeed)|(to)|(want)).*"),
										transitions={'true': 'get id', 'false': 'false'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'text': 'text', 'result': 'result'})

			# x:246 y:298
			OperatableStateMachine.add('test no',
										RegexTester(regex=".*((no)|(not)|(nope)|(negative)|(wrong)|(bad)).*"),
										transitions={'true': 'false', 'false': 'sayno'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'text': 'text', 'result': 'result'})


		# x:30 y:365
		_sm_look_at_4 = OperatableStateMachine(outcomes=['failed'], input_keys=['umbrella'])

		with _sm_look_at_4:
			# x:181 y:86
			OperatableStateMachine.add('get ID',
										GetAttribute(attributes=["ID"]),
										transitions={'done': 'look'},
										autonomy={'done': Autonomy.Off},
										remapping={'object': 'umbrella', 'ID': 'ID'})

			# x:193 y:193
			OperatableStateMachine.add('look',
										KeepLookingAt(),
										transitions={'failed': 'failed'},
										autonomy={'failed': Autonomy.Off},
										remapping={'ID': 'ID'})


		# x:228 y:419
		_sm_find_raising_arm_5 = OperatableStateMachine(outcomes=['finished'], output_keys=['umbrella'])

		with _sm_find_raising_arm_5:
			# x:33 y:48
			OperatableStateMachine.add('setperson',
										SetKey(Value="person"),
										transitions={'done': 'gettaxiperson'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'person'})

			# x:183 y:120
			OperatableStateMachine.add('gettaxiperson',
										list_entities_by_name(frontality_level=0.5, distance_max=10),
										transitions={'found': 'taxi', 'none_found': 'gettaxiperson'},
										autonomy={'found': Autonomy.Off, 'none_found': Autonomy.Off},
										remapping={'name': 'person', 'entity_list': 'entity_list', 'number': 'number'})

			# x:408 y:270
			OperatableStateMachine.add('if',
										CheckConditionState(predicate=lambda x: len(x)>0),
										transitions={'true': 'get first', 'false': 'gettaxiperson'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'output_list'})

			# x:344 y:184
			OperatableStateMachine.add('taxi',
										Filter(filter=lambda x: x.pose.right_arm_up or x.pose.left_arm_up),
										transitions={'done': 'if'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_list': 'entity_list', 'output_list': 'output_list'})

			# x:405 y:359
			OperatableStateMachine.add('get first',
										CalculationState(calculation=lambda x: x[0]),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'output_list', 'output_value': 'umbrella'})


		# x:30 y:365
		_sm_rotation_6 = OperatableStateMachine(outcomes=['end'])

		with _sm_rotation_6:
			# x:51 y:38
			OperatableStateMachine.add('Set 180 degres',
										SetKey(Value=3.1416),
										transitions={'done': 'Look Center'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'rotation'})

			# x:613 y:470
			OperatableStateMachine.add('action_turn',
										self.use_behavior(sara_flexbe_behaviors__action_turnSM, 'GetTaxi/Find umbrella/gettaxihuman/Rotation/action_turn'),
										transitions={'finished': 'Look Right', 'failed': 'Look Right'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'rotation': 'rotation'})

			# x:421 y:54
			OperatableStateMachine.add('Look Right',
										SaraSetHeadAngle(pitch=0, yaw=-1.5),
										transitions={'done': 'w2'},
										autonomy={'done': Autonomy.Off})

			# x:265 y:56
			OperatableStateMachine.add('w1',
										WaitState(wait_time=4),
										transitions={'done': 'Look Right'},
										autonomy={'done': Autonomy.Off})

			# x:630 y:56
			OperatableStateMachine.add('w2',
										WaitState(wait_time=4),
										transitions={'done': 'center'},
										autonomy={'done': Autonomy.Off})

			# x:250 y:177
			OperatableStateMachine.add('Look Center',
										SaraSetHeadAngle(pitch=0, yaw=0),
										transitions={'done': 'w1'},
										autonomy={'done': Autonomy.Off})

			# x:618 y:304
			OperatableStateMachine.add('Look Left 2',
										SaraSetHeadAngle(pitch=0, yaw=1.5),
										transitions={'done': 'w4'},
										autonomy={'done': Autonomy.Off})

			# x:612 y:138
			OperatableStateMachine.add('center',
										SaraSetHeadAngle(pitch=0, yaw=0),
										transitions={'done': 'w3'},
										autonomy={'done': Autonomy.Off})

			# x:635 y:214
			OperatableStateMachine.add('w3',
										WaitState(wait_time=4),
										transitions={'done': 'Look Left 2'},
										autonomy={'done': Autonomy.Off})

			# x:636 y:394
			OperatableStateMachine.add('w4',
										WaitState(wait_time=4),
										transitions={'done': 'action_turn'},
										autonomy={'done': Autonomy.Off})


		# x:30 y:365
		_sm_find_entity_7 = OperatableStateMachine(outcomes=['found'], input_keys=['className'], output_keys=['entity'])

		with _sm_find_entity_7:
			# x:181 y:178
			OperatableStateMachine.add('find_entity',
										list_entities_by_name(frontality_level=0.5, distance_max=4),
										transitions={'found': 'Get Entity', 'none_found': 'find_entity'},
										autonomy={'found': Autonomy.Off, 'none_found': Autonomy.Off},
										remapping={'name': 'className', 'entity_list': 'entity_list', 'number': 'number'})

			# x:454 y:178
			OperatableStateMachine.add('Get Entity',
										CalculationState(calculation=lambda x: x[0]),
										transitions={'done': 'found'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'entity_list', 'output_value': 'entity'})

			# x:194 y:40
			OperatableStateMachine.add('WaitState',
										WaitState(wait_time=1),
										transitions={'done': 'find_entity'},
										autonomy={'done': Autonomy.Off})


		# x:30 y:365, x:130 y:365, x:230 y:365
		_sm_look_at_taxi_for_1_sec_8 = ConcurrencyContainer(outcomes=['done'], input_keys=['umbrella'], conditions=[
										('done', [('WaitState', 'done')]),
										('done', [('look at', 'failed')])
										])

		with _sm_look_at_taxi_for_1_sec_8:
			# x:30 y:40
			OperatableStateMachine.add('WaitState',
										WaitState(wait_time=1),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off})

			# x:250 y:120
			OperatableStateMachine.add('look at',
										_sm_look_at_4,
										transitions={'failed': 'done'},
										autonomy={'failed': Autonomy.Inherit},
										remapping={'umbrella': 'umbrella'})


		# x:34 y:496, x:130 y:365, x:475 y:291, x:330 y:365, x:430 y:365
		_sm_gettaxihuman_9 = ConcurrencyContainer(outcomes=['found', 'not_found'], input_keys=['umbrella'], output_keys=['umbrella'], conditions=[
										('not_found', [('Rotation', 'end')]),
										('found', [('Find Entity', 'found')]),
										('found', [('FInd raising arm', 'finished')])
										])

		with _sm_gettaxihuman_9:
			# x:127 y:67
			OperatableStateMachine.add('Find Entity',
										_sm_find_entity_7,
										transitions={'found': 'found'},
										autonomy={'found': Autonomy.Inherit},
										remapping={'className': 'umbrella', 'entity': 'umbrella'})

			# x:129 y:180
			OperatableStateMachine.add('Rotation',
										_sm_rotation_6,
										transitions={'end': 'not_found'},
										autonomy={'end': Autonomy.Inherit})

			# x:377 y:127
			OperatableStateMachine.add('FInd raising arm',
										_sm_find_raising_arm_5,
										transitions={'finished': 'found'},
										autonomy={'finished': Autonomy.Inherit},
										remapping={'umbrella': 'umbrella'})


		# x:73 y:441, x:586 y:51
		_sm_find_umbrella_10 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['umbrella'], output_keys=['umbrella'])

		with _sm_find_umbrella_10:
			# x:67 y:42
			OperatableStateMachine.add('Look Center',
										SaraSetHeadAngle(pitch=0.1, yaw=0),
										transitions={'done': 'saytaxi'},
										autonomy={'done': Autonomy.Off})

			# x:278 y:138
			OperatableStateMachine.add('Look Center Not Found',
										SaraSetHeadAngle(pitch=0.1, yaw=0),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:58 y:326
			OperatableStateMachine.add('Log Entity',
										LogKeyState(text="Found entity: {}", severity=Logger.REPORT_HINT),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'umbrella'})

			# x:62 y:169
			OperatableStateMachine.add('gettaxihuman',
										_sm_gettaxihuman_9,
										transitions={'found': 'look at taxi for 1 sec', 'not_found': 'Look Center Not Found'},
										autonomy={'found': Autonomy.Inherit, 'not_found': Autonomy.Inherit},
										remapping={'umbrella': 'umbrella'})

			# x:61 y:244
			OperatableStateMachine.add('look at taxi for 1 sec',
										_sm_look_at_taxi_for_1_sec_8,
										transitions={'done': 'Log Entity'},
										autonomy={'done': Autonomy.Inherit},
										remapping={'umbrella': 'umbrella'})

			# x:63 y:108
			OperatableStateMachine.add('saytaxi',
										SaraSay(sentence="Taxi driver, please raise your umbrella, so i can see you.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'gettaxihuman'},
										autonomy={'done': Autonomy.Off})


		# x:83 y:284
		_sm_lift_head_11 = OperatableStateMachine(outcomes=['finished'])

		with _sm_lift_head_11:
			# x:53 y:42
			OperatableStateMachine.add('lift head',
										SaraSetHeadAngle(pitch=0, yaw=0),
										transitions={'done': 'wait 2'},
										autonomy={'done': Autonomy.Off})

			# x:57 y:152
			OperatableStateMachine.add('wait 2',
										WaitState(wait_time=3),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		# x:30 y:365
		_sm_get_closer_12 = OperatableStateMachine(outcomes=['finished'], input_keys=['person'])

		with _sm_get_closer_12:
			# x:151 y:63
			OperatableStateMachine.add('get ID',
										GetAttribute(attributes=["ID"]),
										transitions={'done': 'Get closer'},
										autonomy={'done': Autonomy.Off},
										remapping={'object': 'person', 'ID': 'ID'})

			# x:135 y:194
			OperatableStateMachine.add('Get closer',
										_sm_get_closer_0,
										transitions={'finished': 'finished'},
										autonomy={'finished': Autonomy.Inherit},
										remapping={'ID': 'ID'})


		# x:607 y:98, x:558 y:330
		_sm_get_gender_13 = OperatableStateMachine(outcomes=['none_found', 'done'], input_keys=['name', 'distance'], output_keys=['person', 'pronoun'])

		with _sm_get_gender_13:
			# x:30 y:40
			OperatableStateMachine.add('set head',
										SaraSetHeadAngle(pitch=0, yaw=0),
										transitions={'done': 'Scan'},
										autonomy={'done': Autonomy.Off})

			# x:441 y:109
			OperatableStateMachine.add('FiltreGender',
										_sm_filtregender_2,
										transitions={'none_found': 'none_found', 'found person': 'done'},
										autonomy={'none_found': Autonomy.Inherit, 'found person': Autonomy.Inherit},
										remapping={'name': 'name', 'pronoun': 'pronoun', 'person': 'person'})

			# x:211 y:93
			OperatableStateMachine.add('Scan',
										_sm_scan_1,
										transitions={'finished': 'FiltreGender'},
										autonomy={'finished': Autonomy.Inherit})


		# x:30 y:373, x:130 y:373
		_sm_nevermind_14 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['poseOrigin'])

		with _sm_nevermind_14:
			# x:30 y:40
			OperatableStateMachine.add('say ok',
										SaraSay(sentence="I will try again", input_keys=[], emotion=0, block=False),
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Off})

			# x:26 y:192
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'nevermind/Action_Move'),
										transitions={'finished': 'done', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'poseOrigin'})


		# x:30 y:458, x:130 y:458, x:230 y:458, x:330 y:458, x:430 y:458
		_sm_confirm_15 = ConcurrencyContainer(outcomes=['false', 'done'], input_keys=['person', 'pronoun'], conditions=[
										('false', [('Confirm', 'false')]),
										('done', [('Confirm', 'done')]),
										('false', [('LookAtClosest', 'failed')])
										])

		with _sm_confirm_15:
			# x:95 y:163
			OperatableStateMachine.add('Confirm',
										_sm_confirm_3,
										transitions={'false': 'false', 'done': 'done'},
										autonomy={'false': Autonomy.Inherit, 'done': Autonomy.Inherit},
										remapping={'Person': 'person', 'pronoun': 'pronoun'})

			# x:309 y:162
			OperatableStateMachine.add('LookAtClosest',
										self.use_behavior(sara_flexbe_behaviors__LookAtClosestSM, 'confirm/LookAtClosest'),
										transitions={'failed': 'false'},
										autonomy={'failed': Autonomy.Inherit})


		# x:65 y:581, x:688 y:449
		_sm_gettaxi_16 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['distance', 'taxi', 'umbrella'])

		with _sm_gettaxi_16:
			# x:103 y:28
			OperatableStateMachine.add('Action_Move_to taxi',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'GetTaxi/Action_Move_to taxi'),
										transitions={'finished': 'Lift head', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'taxi'})

			# x:220 y:546
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'GetTaxi/Action_Move'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'pose_out'})

			# x:80 y:475
			OperatableStateMachine.add('NotTooClose',
										Get_Reacheable_Waypoint(),
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose_in': 'position', 'distance': 'distance', 'pose_out': 'pose_out'})

			# x:81 y:400
			OperatableStateMachine.add('GEtUmbrellaPosition',
										GetAttribute(attributes=["position"]),
										transitions={'done': 'NotTooClose'},
										autonomy={'done': Autonomy.Off},
										remapping={'object': 'umbrella', 'position': 'position'})

			# x:108 y:131
			OperatableStateMachine.add('Lift head',
										_sm_lift_head_11,
										transitions={'finished': 'Find umbrella'},
										autonomy={'finished': Autonomy.Inherit})

			# x:150 y:315
			OperatableStateMachine.add('log',
										LogKeyState(text="found umbrella: {}", severity=Logger.REPORT_HINT),
										transitions={'done': 'GEtUmbrellaPosition'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'umbrella'})

			# x:267 y:312
			OperatableStateMachine.add('say see taxy',
										SaraSay(sentence="I see the taxi. Over there. The person with the umbrella.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'log'},
										autonomy={'done': Autonomy.Off})

			# x:111 y:204
			OperatableStateMachine.add('Find umbrella',
										_sm_find_umbrella_10,
										transitions={'finished': 'say see taxy', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'umbrella': 'umbrella'})



		with _state_machine:
			# x:46 y:16
			OperatableStateMachine.add('GetOrigin',
										Get_Robot_Pose(),
										transitions={'done': 'Init_Sequence'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose': 'poseOrigin'})

			# x:63 y:627
			OperatableStateMachine.add('GetTaxi',
										_sm_gettaxi_16,
										transitions={'finished': 'say succeed', 'failed': 'say fail'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'distance': 'distance', 'taxi': 'taxi', 'umbrella': 'umbrella'})

			# x:103 y:369
			OperatableStateMachine.add('confirm',
										_sm_confirm_15,
										transitions={'false': 'nevermind', 'done': 'say taxi'},
										autonomy={'false': Autonomy.Inherit, 'done': Autonomy.Inherit},
										remapping={'person': 'person', 'pronoun': 'pronoun'})

			# x:289 y:142
			OperatableStateMachine.add('say nobody',
										SaraSay(sentence="I don't see any raised hand.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'Get Gender'},
										autonomy={'done': Autonomy.Off})

			# x:571 y:104
			OperatableStateMachine.add('say fail',
										SaraSay(sentence="I failed this scenario. Sorry.", input_keys=[], emotion=3, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:245 y:595
			OperatableStateMachine.add('say succeed',
										SaraSay(sentence="here is the taxy driver.", input_keys=[], emotion=5, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:96 y:452
			OperatableStateMachine.add('say taxi',
										SaraSay(sentence="Ok, follow me to the taxi then and please retrieve your own coat.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'Action_Pass_Door'},
										autonomy={'done': Autonomy.Off})

			# x:49 y:101
			OperatableStateMachine.add('Init_Sequence',
										self.use_behavior(sara_flexbe_behaviors__Init_SequenceSM, 'Init_Sequence'),
										transitions={'finished': 'Get Gender', 'failed': 'say fail'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:17 y:288
			OperatableStateMachine.add('nevermind',
										_sm_nevermind_14,
										transitions={'done': 'Get Gender', 'failed': 'say fail'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'poseOrigin': 'poseOrigin'})

			# x:30 y:192
			OperatableStateMachine.add('Get Gender',
										_sm_get_gender_13,
										transitions={'none_found': 'say nobody', 'done': 'get closer'},
										autonomy={'none_found': Autonomy.Inherit, 'done': Autonomy.Inherit},
										remapping={'name': 'name', 'distance': 'distance', 'person': 'person', 'pronoun': 'pronoun'})

			# x:259 y:310
			OperatableStateMachine.add('get closer',
										_sm_get_closer_12,
										transitions={'finished': 'confirm'},
										autonomy={'finished': Autonomy.Inherit},
										remapping={'person': 'person'})

			# x:43 y:533
			OperatableStateMachine.add('Action_Pass_Door',
										self.use_behavior(sara_flexbe_behaviors__Action_Pass_DoorSM, 'Action_Pass_Door'),
										transitions={'Done': 'GetTaxi', 'Fail': 'GetTaxi'},
										autonomy={'Done': Autonomy.Inherit, 'Fail': Autonomy.Inherit},
										remapping={'DoorName': 'DoorName'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
