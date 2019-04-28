#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.regex_tester import RegexTester
from sara_flexbe_states.get_speech import GetSpeech
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_states.sara_set_head_angle import SaraSetHeadAngle
from sara_flexbe_states.list_entities_by_name import list_entities_by_name
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_behaviors.action_guide2_sm import Action_Guide2SM as sara_flexbe_behaviors__Action_Guide2SM
from sara_flexbe_behaviors.action_receive_bag_sm import Action_Receive_BagSM as sara_flexbe_behaviors__Action_Receive_BagSM
from sara_flexbe_behaviors.lookatclosest_sm import LookAtClosestSM as sara_flexbe_behaviors__LookAtClosestSM
from sara_flexbe_states.get_reachable_waypoint import Get_Reacheable_Waypoint
from sara_flexbe_behaviors.action_move_sm import Action_MoveSM as sara_flexbe_behaviors__Action_MoveSM
from sara_flexbe_states.moveit_move import MoveitMove
from sara_flexbe_states.set_gripper_state import SetGripperState
from flexbe_states.wait_state import WaitState
from sara_flexbe_states.get_robot_pose import Get_Robot_Pose
from sara_flexbe_behaviors.action_follow_sm import Action_followSM as sara_flexbe_behaviors__Action_followSM
from sara_flexbe_states.SetRosParam import SetRosParam
from sara_flexbe_behaviors.action_pass_door_sm import Action_Pass_DoorSM as sara_flexbe_behaviors__Action_Pass_DoorSM
from sara_flexbe_states.continue_button import ContinueButton
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sat May 19 2018
@author: Huynh-Anh Le
'''
class HelpmecarrySM(Behavior):
	'''
	Helps someone carry groceries
	'''


	def __init__(self):
		super(HelpmecarrySM, self).__init__()
		self.name = 'Help me carry'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(sara_flexbe_behaviors__Action_Guide2SM, 'GetNewPerson/Action_Guide2')
		self.add_behavior(sara_flexbe_behaviors__Action_Receive_BagSM, 'Recevoir sac/Receive bag/Action_Receive_Bag')
		self.add_behavior(sara_flexbe_behaviors__LookAtClosestSM, 'Recevoir sac/Look at/LookAtClosest')
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'Retour maison/Action_Move')
		self.add_behavior(sara_flexbe_behaviors__Action_followSM, 'Getting ID Operator and follow /Follow/Action_follow')
		self.add_behavior(sara_flexbe_behaviors__Action_Pass_DoorSM, 'Enter arena/Action_Pass_Door')
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'Enter arena/Action_Move')
		self.add_behavior(sara_flexbe_behaviors__Action_Pass_DoorSM, 'ExitArena/Action_Pass_Door')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:

		# O 678 543 
		# Une fois que le robot arrive a destination, il informe quil laissera le sac sur le sol.

		# ! 364 45 
		# retourne a la position initiale

		# O 525 82 
		# lorsquil arrive a destination, il baisse le bras, ouvre la pince ,attend et ferme sa pince.



	def create(self):
		# x:832 y:260, x:728 y:256
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['ID'])
		_state_machine.userdata.ID = 0
		_state_machine.userdata.Closed_Gripper_Width = 1
		_state_machine.userdata.Open_Gripper_Width = 255
		_state_machine.userdata.Relative = False
		_state_machine.userdata.Pose_Init = "IdlePose"
		_state_machine.userdata.dropPose = "DropBagPose"
		_state_machine.userdata.EntryDoor = "door1/enter"
		_state_machine.userdata.ExitDoor = "door1/exit"

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:700 y:231, x:418 y:463
		_sm_ecoute_getpose_0 = OperatableStateMachine(outcomes=['arrete', 'fail'])

		with _sm_ecoute_getpose_0:
			# x:53 y:35
			OperatableStateMachine.add('Ecoute',
										GetSpeech(watchdog=5),
										transitions={'done': 'stop', 'nothing': 'Ecoute', 'fail': 'fail'},
										autonomy={'done': Autonomy.Off, 'nothing': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'words': 'words'})

			# x:373 y:215
			OperatableStateMachine.add('stop',
										RegexTester(regex=".*stop.*"),
										transitions={'true': 'arrete', 'false': 'Ecoute'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'text': 'words', 'result': 'result'})


		# x:350 y:105, x:261 y:311
		_sm_get_operator_id_1 = OperatableStateMachine(outcomes=['not_found', 'done'], output_keys=['ID'])

		with _sm_get_operator_id_1:
			# x:42 y:30
			OperatableStateMachine.add('nom',
										SetKey(Value="person"),
										transitions={'done': 'FindId'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'name'})

			# x:37 y:347
			OperatableStateMachine.add('setID',
										SetRosParam(ParamName="OperatorID"),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off},
										remapping={'Value': 'ID'})

			# x:30 y:112
			OperatableStateMachine.add('FindId',
										list_entities_by_name(frontality_level=0.5, distance_max=10),
										transitions={'found': 'GetID', 'none_found': 'not_found'},
										autonomy={'found': Autonomy.Off, 'none_found': Autonomy.Off},
										remapping={'name': 'name', 'entity_list': 'Entities_list', 'number': 'number'})

			# x:38 y:238
			OperatableStateMachine.add('GetID',
										CalculationState(calculation=lambda x: x[0].ID),
										transitions={'done': 'setID'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Entities_list', 'output_value': 'ID'})


		# x:346 y:367, x:610 y:472, x:230 y:365, x:628 y:425, x:619 y:318, x:54 y:367
		_sm_follow_2 = ConcurrencyContainer(outcomes=['done', 'failed', 'not_found'], input_keys=['ID', 'distance'], output_keys=['Position'], conditions=[
										('not_found', [('Action_follow', 'failed')]),
										('done', [('Ecoute_getPose', 'arrete')]),
										('failed', [('Ecoute_getPose', 'fail')])
										])

		with _sm_follow_2:
			# x:107 y:103
			OperatableStateMachine.add('Action_follow',
										self.use_behavior(sara_flexbe_behaviors__Action_followSM, 'Getting ID Operator and follow /Follow/Action_follow'),
										transitions={'failed': 'not_found'},
										autonomy={'failed': Autonomy.Inherit},
										remapping={'ID': 'ID'})

			# x:294 y:146
			OperatableStateMachine.add('Ecoute_getPose',
										_sm_ecoute_getpose_0,
										transitions={'arrete': 'done', 'fail': 'failed'},
										autonomy={'arrete': Autonomy.Inherit, 'fail': Autonomy.Inherit})


		# x:57 y:371, x:419 y:55
		_sm_waiting_for_operator_3 = OperatableStateMachine(outcomes=['done', 'failed'])

		with _sm_waiting_for_operator_3:
			# x:57 y:67
			OperatableStateMachine.add('getSpeech',
										GetSpeech(watchdog=15),
										transitions={'done': 'UnderstandingOpe', 'nothing': 'failed', 'fail': 'failed'},
										autonomy={'done': Autonomy.Off, 'nothing': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'words': 'words'})

			# x:53 y:249
			OperatableStateMachine.add('start',
										SaraSay(sentence="I will follow you. Tell me when to stop.", input_keys=[], emotion=1, block=True),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off})

			# x:203 y:180
			OperatableStateMachine.add('UnderstandingOpe',
										RegexTester(regex=".*follow.*"),
										transitions={'true': 'start', 'false': 'failed'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'text': 'words', 'result': 'result'})


		# x:130 y:365
		_sm_look_at_4 = OperatableStateMachine(outcomes=['failed'])

		with _sm_look_at_4:
			# x:105 y:160
			OperatableStateMachine.add('LookAtClosest',
										self.use_behavior(sara_flexbe_behaviors__LookAtClosestSM, 'Recevoir sac/Look at/LookAtClosest'),
										transitions={'failed': 'failed'},
										autonomy={'failed': Autonomy.Inherit})


		# x:280 y:296, x:248 y:549
		_sm_receive_bag_5 = OperatableStateMachine(outcomes=['failed', 'done'], input_keys=['Closed_Gripper_Width', 'Open_Gripper_Width'])

		with _sm_receive_bag_5:
			# x:42 y:326
			OperatableStateMachine.add('PutBAg',
										SaraSay(sentence="Please put the grocery bag in my hand", input_keys=[], emotion=1, block=False),
										transitions={'done': 'Action_Receive_Bag'},
										autonomy={'done': Autonomy.Off})

			# x:18 y:427
			OperatableStateMachine.add('Action_Receive_Bag',
										self.use_behavior(sara_flexbe_behaviors__Action_Receive_BagSM, 'Recevoir sac/Receive bag/Action_Receive_Bag'),
										transitions={'finished': 'bringit', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'Closed_Gripper_Width': 'Closed_Gripper_Width', 'Open_Gripper_Width': 'Open_Gripper_Width', 'Closed_Gripper_Width': 'Closed_Gripper_Width'})

			# x:66 y:125
			OperatableStateMachine.add('getspeech2',
										GetSpeech(watchdog=5),
										transitions={'done': 'takebag', 'nothing': 'getspeech2', 'fail': 'failed'},
										autonomy={'done': Autonomy.Off, 'nothing': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'words': 'words'})

			# x:64 y:218
			OperatableStateMachine.add('takebag',
										RegexTester(regex=".*((take)|(bag)|(ready)).*"),
										transitions={'true': 'PutBAg', 'false': 'getspeech2'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'text': 'words', 'result': 'result'})

			# x:42 y:531
			OperatableStateMachine.add('bringit',
										SaraSay(sentence="I will bring it inside", input_keys=[], emotion=1, block=True),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off})

			# x:77 y:40
			OperatableStateMachine.add('sac',
										SaraSay(sentence="Ok. Tell me, when you are ready", input_keys=[], emotion=1, block=True),
										transitions={'done': 'getspeech2'},
										autonomy={'done': Autonomy.Off})


		# x:147 y:579
		_sm_look_at_closest_6 = OperatableStateMachine(outcomes=['failed'], output_keys=['Entity'])

		with _sm_look_at_closest_6:
			# x:40 y:39
			OperatableStateMachine.add('set person',
										SetKey(Value="person"),
										transitions={'done': 'head angle'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Person'})

			# x:36 y:119
			OperatableStateMachine.add('head angle',
										SaraSetHeadAngle(pitch=-0.3, yaw=0),
										transitions={'done': 'get persons'},
										autonomy={'done': Autonomy.Off})

			# x:271 y:149
			OperatableStateMachine.add('get persons',
										list_entities_by_name(frontality_level=0.5, distance_max=2),
										transitions={'found': 'set person', 'none_found': 'get persons'},
										autonomy={'found': Autonomy.Off, 'none_found': Autonomy.Off},
										remapping={'name': 'Person', 'entity_list': 'entity_list', 'number': 'number'})


		# x:30 y:365
		_sm_get_op_7 = OperatableStateMachine(outcomes=['true'])

		with _sm_get_op_7:
			# x:76 y:40
			OperatableStateMachine.add('Say Joke',
										SaraSay(sentence="Can someone come help me, I only have one arm.", input_keys=[], emotion=1, block=True),
										transitions={'done': 'ecouteNewPerson'},
										autonomy={'done': Autonomy.Off})

			# x:208 y:255
			OperatableStateMachine.add('listen',
										RegexTester(regex=".*((i)|(come)|(help)).*"),
										transitions={'true': 'true', 'false': 'ecouteNewPerson'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'text': 'words', 'result': 'result'})

			# x:32 y:106
			OperatableStateMachine.add('ecouteNewPerson',
										GetSpeech(watchdog=5),
										transitions={'done': 'listen', 'nothing': 'ecouteNewPerson', 'fail': 'ecouteNewPerson'},
										autonomy={'done': Autonomy.Off, 'nothing': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'words': 'words'})


		# x:65 y:357, x:130 y:365, x:230 y:365
		_sm_get_ope_8 = ConcurrencyContainer(outcomes=['true'], output_keys=['Entity'], conditions=[
										('true', [('get op', 'true')]),
										('true', [('look at closest', 'failed')])
										])

		with _sm_get_ope_8:
			# x:37 y:35
			OperatableStateMachine.add('get op',
										_sm_get_op_7,
										transitions={'true': 'true'},
										autonomy={'true': Autonomy.Inherit})

			# x:238 y:109
			OperatableStateMachine.add('look at closest',
										_sm_look_at_closest_6,
										transitions={'failed': 'true'},
										autonomy={'failed': Autonomy.Inherit},
										remapping={'Entity': 'Entity'})


		# x:37 y:417, x:236 y:263
		_sm_init_sara_9 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['Pose_Init'], output_keys=['Origin'])

		with _sm_init_sara_9:
			# x:30 y:40
			OperatableStateMachine.add('get_pose',
										Get_Robot_Pose(),
										transitions={'done': 'SETHEAD'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose': 'Origin'})

			# x:24 y:259
			OperatableStateMachine.add('Init Arm',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'done', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'Pose_Init'})

			# x:23 y:183
			OperatableStateMachine.add('SETHEAD',
										SaraSetHeadAngle(pitch=0, yaw=0),
										transitions={'done': 'Init Arm'},
										autonomy={'done': Autonomy.Off})


		# x:92 y:291, x:242 y:133
		_sm_exitarena_10 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['ExitDoor'])

		with _sm_exitarena_10:
			# x:38 y:119
			OperatableStateMachine.add('Action_Pass_Door',
										self.use_behavior(sara_flexbe_behaviors__Action_Pass_DoorSM, 'ExitArena/Action_Pass_Door'),
										transitions={'Done': 'finished', 'Fail': 'failed'},
										autonomy={'Done': Autonomy.Inherit, 'Fail': Autonomy.Inherit},
										remapping={'DoorName': 'ExitDoor'})


		# x:353 y:529, x:369 y:296
		_sm_enter_arena_11 = OperatableStateMachine(outcomes=['done', 'fail'], input_keys=['EntryDoor'])

		with _sm_enter_arena_11:
			# x:132 y:147
			OperatableStateMachine.add('Action_Pass_Door',
										self.use_behavior(sara_flexbe_behaviors__Action_Pass_DoorSM, 'Enter arena/Action_Pass_Door'),
										transitions={'Done': 'say start', 'Fail': 'fail'},
										autonomy={'Done': Autonomy.Inherit, 'Fail': Autonomy.Inherit},
										remapping={'DoorName': 'EntryDoor'})

			# x:124 y:501
			OperatableStateMachine.add('say help',
										SaraSay(sentence="Hi, i will help you carry some bags. LEt me know when you need me", input_keys=[], emotion=1, block=True),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off})

			# x:146 y:256
			OperatableStateMachine.add('say start',
										SaraSay(sentence="", input_keys=[], emotion=1, block=True),
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Off})

			# x:121 y:375
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'Enter arena/Action_Move'),
										transitions={'finished': 'say help', 'failed': 'fail'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'EntryDoor'})


		# x:372 y:428, x:389 y:477
		_sm_getting_id_operator_and_follow__12 = OperatableStateMachine(outcomes=['failed', 'done'], output_keys=['Position'])

		with _sm_getting_id_operator_and_follow__12:
			# x:70 y:115
			OperatableStateMachine.add('Waiting for operator',
										_sm_waiting_for_operator_3,
										transitions={'done': 'Get operator ID', 'failed': 'Waiting for operator'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:71 y:504
			OperatableStateMachine.add('get pose',
										Get_Robot_Pose(),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose': 'Position'})

			# x:69 y:415
			OperatableStateMachine.add('Follow',
										_sm_follow_2,
										transitions={'done': 'get pose', 'failed': 'failed', 'not_found': 'initial'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'not_found': Autonomy.Inherit},
										remapping={'ID': 'ID', 'distance': 'distance', 'Position': 'Position'})

			# x:60 y:222
			OperatableStateMachine.add('Get operator ID',
										_sm_get_operator_id_1,
										transitions={'not_found': 'Get operator ID', 'done': 'set follow distance'},
										autonomy={'not_found': Autonomy.Inherit, 'done': Autonomy.Inherit},
										remapping={'ID': 'ID'})

			# x:60 y:324
			OperatableStateMachine.add('set follow distance',
										SetKey(Value="0.5"),
										transitions={'done': 'Follow'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'distance'})

			# x:286 y:327
			OperatableStateMachine.add('initial',
										SaraSetHeadAngle(pitch=0, yaw=0),
										transitions={'done': 'Get operator ID'},
										autonomy={'done': Autonomy.Off})


		# x:247 y:123, x:282 y:200, x:230 y:365
		_sm_drop_le_sac_13 = OperatableStateMachine(outcomes=['failed', 'no_object', 'done'], input_keys=['Idle', 'dropPose'])

		with _sm_drop_le_sac_13:
			# x:22 y:114
			OperatableStateMachine.add('dropbag',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'Open', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'dropPose'})

			# x:5 y:344
			OperatableStateMachine.add('close',
										SetGripperState(width=0, effort=1),
										transitions={'object': 'returnIdl', 'no_object': 'returnIdl'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:19 y:268
			OperatableStateMachine.add('wait',
										WaitState(wait_time=2),
										transitions={'done': 'close'},
										autonomy={'done': Autonomy.Off})

			# x:8 y:433
			OperatableStateMachine.add('returnIdl',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'done', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'Idle'})

			# x:10 y:190
			OperatableStateMachine.add('Open',
										SetGripperState(width=0.1, effort=1),
										transitions={'object': 'wait', 'no_object': 'no_object'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})


		# x:555 y:54, x:568 y:190
		_sm_retour_maison_14 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['PoseOrigin', 'Relative'])

		with _sm_retour_maison_14:
			# x:54 y:63
			OperatableStateMachine.add('keydistance',
										SetKey(Value=0),
										transitions={'done': 'adapt the end pose'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'distance'})

			# x:258 y:51
			OperatableStateMachine.add('Arrived',
										SaraSay(sentence="I have food, people. I will drop the bags on the floor.", input_keys=[], emotion=1, block=True),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off})

			# x:43 y:141
			OperatableStateMachine.add('adapt the end pose',
										Get_Reacheable_Waypoint(),
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose_in': 'PoseOrigin', 'distance': 'distance', 'pose_out': 'pose_out'})

			# x:236 y:182
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'Retour maison/Action_Move'),
										transitions={'finished': 'Arrived', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'pose_out'})


		# x:30 y:365, x:130 y:365, x:230 y:365, x:330 y:365, x:430 y:365
		_sm_recevoir_sac_15 = ConcurrencyContainer(outcomes=['failed', 'done'], input_keys=['Closed_Gripper_Width', 'Open_Gripper_Width'], conditions=[
										('failed', [('Receive bag', 'failed')]),
										('done', [('Receive bag', 'done')]),
										('failed', [('Look at', 'failed')])
										])

		with _sm_recevoir_sac_15:
			# x:84 y:156
			OperatableStateMachine.add('Receive bag',
										_sm_receive_bag_5,
										transitions={'failed': 'failed', 'done': 'done'},
										autonomy={'failed': Autonomy.Inherit, 'done': Autonomy.Inherit},
										remapping={'Closed_Gripper_Width': 'Closed_Gripper_Width', 'Open_Gripper_Width': 'Open_Gripper_Width'})

			# x:262 y:154
			OperatableStateMachine.add('Look at',
										_sm_look_at_4,
										transitions={'failed': 'failed'},
										autonomy={'failed': Autonomy.Inherit})


		# x:728 y:533, x:722 y:468
		_sm_getnewperson_16 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['Position'])

		with _sm_getnewperson_16:
			# x:52 y:77
			OperatableStateMachine.add('Get ope',
										_sm_get_ope_8,
										transitions={'true': 'set name'},
										autonomy={'true': Autonomy.Inherit},
										remapping={'Entity': 'Entity'})

			# x:46 y:508
			OperatableStateMachine.add('SET HEAD',
										SaraSetHeadAngle(pitch=-0.2, yaw=0),
										transitions={'done': 'Action_Guide2'},
										autonomy={'done': Autonomy.Off})

			# x:39 y:297
			OperatableStateMachine.add('list',
										list_entities_by_name(frontality_level=0.5, distance_max=2),
										transitions={'found': 'get closest ID', 'none_found': 'list'},
										autonomy={'found': Autonomy.Off, 'none_found': Autonomy.Off},
										remapping={'name': 'name', 'entity_list': 'entity_list', 'number': 'number'})

			# x:70 y:194
			OperatableStateMachine.add('set name',
										SetKey(Value="person"),
										transitions={'done': 'list'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'name'})

			# x:151 y:413
			OperatableStateMachine.add('get closest ID',
										CalculationState(calculation=lambda x: x[0].ID),
										transitions={'done': 'SET HEAD'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'entity_list', 'output_value': 'ID'})

			# x:293 y:534
			OperatableStateMachine.add('Action_Guide2',
										self.use_behavior(sara_flexbe_behaviors__Action_Guide2SM, 'GetNewPerson/Action_Guide2'),
										transitions={'finished': 'done', 'failed': 'failed', 'critical_fail': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Position': 'Position', 'ID': 'ID'})

			# x:57 y:399
			OperatableStateMachine.add('set 0',
										SetKey(Value=0),
										transitions={'done': 'SET HEAD'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'ID'})



		with _state_machine:
			# x:188 y:35
			OperatableStateMachine.add('say ready',
										SaraSay(sentence="I'm ready for the help me carry scenario. I will follow when you ask me.", input_keys=[], emotion=1, block=True),
										transitions={'done': 'INIT SARA'},
										autonomy={'done': Autonomy.Off})

			# x:827 y:439
			OperatableStateMachine.add('finish',
										SaraSay(sentence="I am done for the day", input_keys=[], emotion=2, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:53 y:641
			OperatableStateMachine.add('GetNewPerson',
										_sm_getnewperson_16,
										transitions={'done': 'say leave', 'failed': 'failed'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'Position': 'Position'})

			# x:48 y:349
			OperatableStateMachine.add('Recevoir sac',
										_sm_recevoir_sac_15,
										transitions={'failed': 'failed', 'done': 'Retour maison'},
										autonomy={'failed': Autonomy.Inherit, 'done': Autonomy.Inherit},
										remapping={'Closed_Gripper_Width': 'Closed_Gripper_Width', 'Open_Gripper_Width': 'Open_Gripper_Width'})

			# x:36 y:448
			OperatableStateMachine.add('Retour maison',
										_sm_retour_maison_14,
										transitions={'done': 'drop le sac', 'failed': 'failed'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'PoseOrigin': 'Origin', 'Relative': 'Relative'})

			# x:49 y:556
			OperatableStateMachine.add('drop le sac',
										_sm_drop_le_sac_13,
										transitions={'failed': 'failed', 'no_object': 'failed', 'done': 'GetNewPerson'},
										autonomy={'failed': Autonomy.Inherit, 'no_object': Autonomy.Inherit, 'done': Autonomy.Inherit},
										remapping={'Idle': 'Pose_Init', 'dropPose': 'dropPose'})

			# x:150 y:260
			OperatableStateMachine.add('Getting ID Operator and follow ',
										_sm_getting_id_operator_and_follow__12,
										transitions={'failed': 'failed', 'done': 'Recevoir sac'},
										autonomy={'failed': Autonomy.Inherit, 'done': Autonomy.Inherit},
										remapping={'Position': 'Position'})

			# x:148 y:177
			OperatableStateMachine.add('Enter arena',
										_sm_enter_arena_11,
										transitions={'done': 'Getting ID Operator and follow ', 'fail': 'failed'},
										autonomy={'done': Autonomy.Inherit, 'fail': Autonomy.Inherit},
										remapping={'EntryDoor': 'EntryDoor'})

			# x:498 y:617
			OperatableStateMachine.add('ExitArena',
										_sm_exitarena_10,
										transitions={'finished': 'finish', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'ExitDoor': 'ExitDoor'})

			# x:389 y:14
			OperatableStateMachine.add('ContinueButton',
										ContinueButton(),
										transitions={'true': 'say ready', 'false': 'say ready'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off})

			# x:329 y:645
			OperatableStateMachine.add('say leave',
										SaraSay(sentence="I will leave now. Goodbye", input_keys=[], emotion=1, block=True),
										transitions={'done': 'ExitArena'},
										autonomy={'done': Autonomy.Off})

			# x:319 y:101
			OperatableStateMachine.add('wait1',
										WaitState(wait_time=5),
										transitions={'done': 'say ready'},
										autonomy={'done': Autonomy.Off})

			# x:35 y:78
			OperatableStateMachine.add('INIT SARA',
										_sm_init_sara_9,
										transitions={'done': 'Getting ID Operator and follow ', 'failed': 'failed'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'Pose_Init': 'Pose_Init', 'Origin': 'Origin'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
