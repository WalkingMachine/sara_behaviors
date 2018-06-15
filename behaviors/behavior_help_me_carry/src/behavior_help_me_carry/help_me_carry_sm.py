#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_help_me_carry')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.get_robot_pose import Get_Robot_Pose
from sara_flexbe_states.moveit_move import MoveitMove
from sara_flexbe_states.sara_set_head_angle import SaraSetHeadAngle
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.regex_tester import RegexTester
from behavior_action_guiding_person.action_guiding_person_sm import Action_Guiding_PersonSM
from sara_flexbe_states.get_speech import GetSpeech
from behavior_action_receive_bag.action_receive_bag_sm import Action_Receive_BagSM
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_states.get_reachable_waypoint import Get_Reacheable_Waypoint
from behavior_action_move.action_move_sm import Action_MoveSM
from sara_flexbe_states.set_gripper_state import SetGripperState
from flexbe_states.wait_state import WaitState
from behavior_action_follow.action_follow_sm import Action_followSM
from sara_flexbe_states.SetRosParam import SetRosParam
from sara_flexbe_states.list_entities_by_name import list_entities_by_name
from flexbe_states.calculation_state import CalculationState
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
		self.add_behavior(Action_Guiding_PersonSM, 'GetNewPerson/Action_Guiding_Person')
		self.add_behavior(Action_Receive_BagSM, 'Recevoir sac/Action_Receive_Bag')
		self.add_behavior(Action_MoveSM, 'Retour maison/Action_Move')
		self.add_behavior(Action_followSM, 'Getting ID Operator and follow /Follow/Action_follow')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:

		# O 512 503 
		# Une fois que le robot arrive a destination, il informe quil laissera le sac sur le sol.

		# O 222 46 
		# retourne a la position initiale

		# O 391 134 
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


		# x:320 y:111, x:217 y:274
		_sm_get_operator_id_1 = OperatableStateMachine(outcomes=['not_found', 'done'], output_keys=['ID'])

		with _sm_get_operator_id_1:
			# x:42 y:30
			OperatableStateMachine.add('nom',
										SetKey(Value="person"),
										transitions={'done': 'FindId'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'name'})

			# x:34 y:274
			OperatableStateMachine.add('setID',
										SetRosParam(ParamName="OperatorID"),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off},
										remapping={'Value': 'ID'})

			# x:30 y:112
			OperatableStateMachine.add('FindId',
										list_entities_by_name(frontality_level=0.5),
										transitions={'found': 'GetID', 'not_found': 'not_found'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'name': 'name', 'entity_list': 'Entities_list', 'number': 'number'})

			# x:30 y:186
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
										self.use_behavior(Action_followSM, 'Getting ID Operator and follow /Follow/Action_follow'),
										transitions={'failed': 'not_found'},
										autonomy={'failed': Autonomy.Inherit},
										remapping={'ID': 'ID'})

			# x:294 y:146
			OperatableStateMachine.add('Ecoute_getPose',
										_sm_ecoute_getpose_0,
										transitions={'arrete': 'done', 'fail': 'failed'},
										autonomy={'arrete': Autonomy.Inherit, 'fail': Autonomy.Inherit})


		# x:57 y:371, x:360 y:132
		_sm_waiting_for_operator_3 = OperatableStateMachine(outcomes=['done', 'failed'])

		with _sm_waiting_for_operator_3:
			# x:57 y:67
			OperatableStateMachine.add('getSpeech',
										GetSpeech(watchdog=5),
										transitions={'done': 'UnderstandingOpe', 'nothing': 'getSpeech', 'fail': 'failed'},
										autonomy={'done': Autonomy.Off, 'nothing': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'words': 'words'})

			# x:53 y:249
			OperatableStateMachine.add('start',
										SaraSay(sentence="I will follow you ", emotion=1, block=True),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off})

			# x:39 y:162
			OperatableStateMachine.add('UnderstandingOpe',
										RegexTester(regex=".*follow.*"),
										transitions={'true': 'start', 'false': 'failed'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'text': 'words', 'result': 'result'})


		# x:372 y:428, x:389 y:477
		_sm_getting_id_operator_and_follow__4 = OperatableStateMachine(outcomes=['failed', 'done'], output_keys=['Position'])

		with _sm_getting_id_operator_and_follow__4:
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
		_sm_drop_le_sac_5 = OperatableStateMachine(outcomes=['failed', 'no_object', 'done'], input_keys=['Idle', 'dropPose'])

		with _sm_drop_le_sac_5:
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
										WaitState(wait_time=5),
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
		_sm_retour_maison_6 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['PoseOrigin', 'Relative'])

		with _sm_retour_maison_6:
			# x:54 y:63
			OperatableStateMachine.add('keydistance',
										SetKey(Value=0),
										transitions={'done': 'adapt the end pose'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'distance'})

			# x:258 y:51
			OperatableStateMachine.add('Arrived',
										SaraSay(sentence="I have food, people. I will drop the bags on the floor.", emotion=1, block=True),
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
										self.use_behavior(Action_MoveSM, 'Retour maison/Action_Move'),
										transitions={'finished': 'Arrived', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'pose_out', 'relative': 'Relative'})


		# x:305 y:329, x:335 y:117, x:311 y:458
		_sm_recevoir_sac_7 = OperatableStateMachine(outcomes=['failed', 'fail', 'done'], input_keys=['Closed_Gripper_Width', 'Open_Gripper_Width'])

		with _sm_recevoir_sac_7:
			# x:77 y:40
			OperatableStateMachine.add('sac',
										SaraSay(sentence="Tell me, when you are ready", emotion=1, block=True),
										transitions={'done': 'getspeech2'},
										autonomy={'done': Autonomy.Off})

			# x:30 y:342
			OperatableStateMachine.add('Action_Receive_Bag',
										self.use_behavior(Action_Receive_BagSM, 'Recevoir sac/Action_Receive_Bag'),
										transitions={'finished': 'bringit', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'Closed_Gripper_Width': 'Closed_Gripper_Width', 'Open_Gripper_Width': 'Open_Gripper_Width', 'Closed_Gripper_Width': 'Closed_Gripper_Width'})

			# x:57 y:103
			OperatableStateMachine.add('getspeech2',
										GetSpeech(watchdog=5),
										transitions={'done': 'takebag', 'nothing': 'getspeech2', 'fail': 'fail'},
										autonomy={'done': Autonomy.Off, 'nothing': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'words': 'words'})

			# x:55 y:179
			OperatableStateMachine.add('takebag',
										RegexTester(regex=".*((take)|(bag)|(ready)).*"),
										transitions={'true': 'PutBAg', 'false': 'getspeech2'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'text': 'words', 'result': 'result'})

			# x:53 y:445
			OperatableStateMachine.add('bringit',
										SaraSay(sentence="I will bring it inside", emotion=1, block=True),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off})

			# x:63 y:247
			OperatableStateMachine.add('PutBAg',
										SaraSay(sentence="Could you put the bag in my hand?, please", emotion=1, block=False),
										transitions={'done': 'Action_Receive_Bag'},
										autonomy={'done': Autonomy.Off})


		# x:364 y:229, x:380 y:73
		_sm_getnewperson_8 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['Position'])

		with _sm_getnewperson_8:
			# x:88 y:40
			OperatableStateMachine.add('Say Joke',
										SaraSay(sentence="Can someone come help me, I only have one arm.", emotion=1, block=True),
										transitions={'done': 'ecouteNewPerson'},
										autonomy={'done': Autonomy.Off})

			# x:42 y:221
			OperatableStateMachine.add('listen',
										RegexTester(regex=".*((i)|(come)|(help)).*"),
										transitions={'true': 'Action_Guiding_Person', 'false': 'ecouteNewPerson'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'text': 'words', 'result': 'result'})

			# x:28 y:315
			OperatableStateMachine.add('Action_Guiding_Person',
										self.use_behavior(Action_Guiding_PersonSM, 'GetNewPerson/Action_Guiding_Person'),
										transitions={'finished': 'done', 'not found': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'not found': Autonomy.Inherit},
										remapping={'Position': 'Position'})

			# x:44 y:106
			OperatableStateMachine.add('ecouteNewPerson',
										GetSpeech(watchdog=5),
										transitions={'done': 'listen', 'nothing': 'ecouteNewPerson', 'fail': 'ecouteNewPerson'},
										autonomy={'done': Autonomy.Off, 'nothing': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'words': 'words'})


		# x:30 y:365, x:130 y:365
		_sm_init_sara_9 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['Pose_Init'], output_keys=['Origin'])

		with _sm_init_sara_9:
			# x:30 y:40
			OperatableStateMachine.add('get_pose',
										Get_Robot_Pose(),
										transitions={'done': 'follow'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose': 'Origin'})

			# x:89 y:247
			OperatableStateMachine.add('Init Arm',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'done', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'Pose_Init'})

			# x:91 y:148
			OperatableStateMachine.add('SETHEAD',
										SaraSetHeadAngle(pitch=0, yaw=0),
										transitions={'done': 'Init Arm'},
										autonomy={'done': Autonomy.Off})

			# x:35 y:93
			OperatableStateMachine.add('follow',
										SaraSay(sentence="Hi, i will help you carry some bags. LEt me know when you need me", emotion=1, block=False),
										transitions={'done': 'SETHEAD'},
										autonomy={'done': Autonomy.Off})



		with _state_machine:
			# x:53 y:79
			OperatableStateMachine.add('INIT SARA',
										_sm_init_sara_9,
										transitions={'done': 'Getting ID Operator and follow ', 'failed': 'failed'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'Pose_Init': 'Pose_Init', 'Origin': 'Origin'})

			# x:827 y:439
			OperatableStateMachine.add('finish',
										SaraSay(sentence="I am done for the day", emotion=2, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:610 y:431
			OperatableStateMachine.add('GetNewPerson',
										_sm_getnewperson_8,
										transitions={'done': 'finish', 'failed': 'failed'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'Position': 'Position'})

			# x:45 y:360
			OperatableStateMachine.add('Recevoir sac',
										_sm_recevoir_sac_7,
										transitions={'failed': 'failed', 'fail': 'Retour maison', 'done': 'Retour maison'},
										autonomy={'failed': Autonomy.Inherit, 'fail': Autonomy.Inherit, 'done': Autonomy.Inherit},
										remapping={'Closed_Gripper_Width': 'Closed_Gripper_Width', 'Open_Gripper_Width': 'Open_Gripper_Width'})

			# x:40 y:463
			OperatableStateMachine.add('Retour maison',
										_sm_retour_maison_6,
										transitions={'done': 'drop le sac', 'failed': 'failed'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'PoseOrigin': 'Origin', 'Relative': 'Relative'})

			# x:413 y:423
			OperatableStateMachine.add('drop le sac',
										_sm_drop_le_sac_5,
										transitions={'failed': 'failed', 'no_object': 'failed', 'done': 'GetNewPerson'},
										autonomy={'failed': Autonomy.Inherit, 'no_object': Autonomy.Inherit, 'done': Autonomy.Inherit},
										remapping={'Idle': 'Pose_Init', 'dropPose': 'dropPose'})

			# x:36 y:172
			OperatableStateMachine.add('Getting ID Operator and follow ',
										_sm_getting_id_operator_and_follow__4,
										transitions={'failed': 'failed', 'done': 'Recevoir sac'},
										autonomy={'failed': Autonomy.Inherit, 'done': Autonomy.Inherit},
										remapping={'Position': 'Position'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
