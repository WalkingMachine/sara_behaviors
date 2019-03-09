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
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_behaviors.action_receive_bag_sm import Action_Receive_BagSM as sara_flexbe_behaviors__Action_Receive_BagSM
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_states.list_entities_by_name import list_entities_by_name
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.SetRosParam import SetRosParam
from sara_flexbe_behaviors.action_follow_sm import Action_followSM as sara_flexbe_behaviors__Action_followSM
from sara_flexbe_states.get_speech import GetSpeech
from sara_flexbe_states.regex_tester import RegexTester
from sara_flexbe_behaviors.action_give_back_bag_sm import Action_Give_Back_BagSM as sara_flexbe_behaviors__Action_Give_Back_BagSM
from sara_flexbe_behaviors.actionwrapper_move_sm import ActionWrapper_MoveSM as sara_flexbe_behaviors__ActionWrapper_MoveSM
from sara_flexbe_states.moveit_move import MoveitMove
from sara_flexbe_states.sara_set_head_angle import SaraSetHeadAngle
from flexbe_navigation_states.move_base_state import MoveBaseState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sat Mar 09 2019
@author: Huynh-Anh Le
'''
class CarrymyluggageSM(Behavior):
	'''
	Sara helps someone carry a bag to his car
	'''


	def __init__(self):
		super(CarrymyluggageSM, self).__init__()
		self.name = 'Carry my luggage'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(sara_flexbe_behaviors__Action_Receive_BagSM, 'Action_Receive_Bag')
		self.add_behavior(sara_flexbe_behaviors__Action_followSM, 'Follow and listen/Action_follow')
		self.add_behavior(sara_flexbe_behaviors__Action_Give_Back_BagSM, 'Action_Give_Back_Bag')
		self.add_behavior(sara_flexbe_behaviors__ActionWrapper_MoveSM, 'InitSara/ActionWrapper_Move')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:

		# O 208 229 
		# Manque OpenPose, pour trouver la direction du bras pour savoir quelle sac prendre



	def create(self):
		# x:1003 y:492, x:630 y:19
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.ActionStart = ["move","PoseStart"]
		_state_machine.userdata.Pose_Init = "IdlePose"
		_state_machine.userdata.Closed_Gripper_Width = 1
		_state_machine.userdata.Open_Gripper_Width = 255
		_state_machine.userdata.ID = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:30 y:365
		_sm_listen_0 = OperatableStateMachine(outcomes=['done'])

		with _sm_listen_0:
			# x:59 y:80
			OperatableStateMachine.add('SayFollow',
										SaraSay(sentence="I will follow you to the car now", input_keys=[], emotion=0, block=True),
										transitions={'done': 'LIsten'},
										autonomy={'done': Autonomy.Off})

			# x:161 y:148
			OperatableStateMachine.add('LIsten',
										GetSpeech(watchdog=5),
										transitions={'done': 'Listen2', 'nothing': 'LIsten', 'fail': 'LIsten'},
										autonomy={'done': Autonomy.Off, 'nothing': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'words': 'words'})

			# x:201 y:256
			OperatableStateMachine.add('Listen2',
										RegexTester(regex=".*((arrived)|(car)|(stop))*."),
										transitions={'true': 'done', 'false': 'LIsten'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'text': 'words', 'result': 'result'})


		# x:30 y:365, x:247 y:594
		_sm_initsara_1 = OperatableStateMachine(outcomes=['failed', 'done'], input_keys=['Pose_Init', 'ActionStart'], output_keys=['failed', 'done'])

		with _sm_initsara_1:
			# x:48 y:49
			OperatableStateMachine.add('ActionWrapper_Move',
										self.use_behavior(sara_flexbe_behaviors__ActionWrapper_MoveSM, 'InitSara/ActionWrapper_Move'),
										transitions={'finished': 'SetHead', 'failed': 'failed', 'critical_fail': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'ActionStart'})

			# x:164 y:267
			OperatableStateMachine.add('SetArm',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'done', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'Pose_Init'})

			# x:191 y:166
			OperatableStateMachine.add('SetHead',
										SaraSetHeadAngle(pitch=0, yaw=0),
										transitions={'done': 'SetArm'},
										autonomy={'done': Autonomy.Off})


		# x:390 y:296, x:111 y:269, x:230 y:365, x:330 y:365
		_sm_follow_and_listen_2 = ConcurrencyContainer(outcomes=['done', 'failed'], input_keys=['ID'], conditions=[
										('failed', [('Action_follow', 'failed')]),
										('done', [('Listen', 'done')])
										])

		with _sm_follow_and_listen_2:
			# x:132 y:90
			OperatableStateMachine.add('Action_follow',
										self.use_behavior(sara_flexbe_behaviors__Action_followSM, 'Follow and listen/Action_follow'),
										transitions={'failed': 'failed'},
										autonomy={'failed': Autonomy.Inherit},
										remapping={'ID': 'ID'})

			# x:356 y:105
			OperatableStateMachine.add('Listen',
										_sm_listen_0,
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Inherit})


		# x:56 y:536
		_sm_getidope_3 = OperatableStateMachine(outcomes=['done'])

		with _sm_getidope_3:
			# x:55 y:63
			OperatableStateMachine.add('Person',
										SetKey(Value="person"),
										transitions={'done': 'GEtId'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'name'})

			# x:43 y:180
			OperatableStateMachine.add('GEtId',
										list_entities_by_name(frontality_level=0.5, distance_max=10),
										transitions={'found': 'ID', 'none_found': 'GEtId'},
										autonomy={'found': Autonomy.Off, 'none_found': Autonomy.Off},
										remapping={'name': 'name', 'entity_list': 'Entities_list', 'number': 'number'})

			# x:52 y:290
			OperatableStateMachine.add('ID',
										CalculationState(calculation=lambda x:x[0].ID),
										transitions={'done': 'setID'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Entities_list', 'output_value': 'ID'})

			# x:37 y:399
			OperatableStateMachine.add('setID',
										SetRosParam(ParamName="behavior/Operator/Id"),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off},
										remapping={'Value': 'ID'})



		with _state_machine:
			# x:86 y:59
			OperatableStateMachine.add('GEtPose',
										Get_Robot_Pose(),
										transitions={'done': 'InitSara'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose': 'Origin'})

			# x:24 y:269
			OperatableStateMachine.add('ImHere',
										SaraSay(sentence="I am here and ready!", input_keys=[], emotion=1, block=True),
										transitions={'done': 'GetIDOpe'},
										autonomy={'done': Autonomy.Off})

			# x:27 y:456
			OperatableStateMachine.add('GetBag',
										SaraSay(sentence="Can you give me the bag, please.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'Action_Receive_Bag'},
										autonomy={'done': Autonomy.Off})

			# x:56 y:529
			OperatableStateMachine.add('Action_Receive_Bag',
										self.use_behavior(sara_flexbe_behaviors__Action_Receive_BagSM, 'Action_Receive_Bag'),
										transitions={'finished': 'Follow and listen', 'failed': 'GetBag'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'Closed_Gripper_Width': 'Closed_Gripper_Width', 'Open_Gripper_Width': 'Open_Gripper_Width', 'Closed_Gripper_Width': 'Closed_Gripper_Width'})

			# x:24 y:358
			OperatableStateMachine.add('GetIDOpe',
										_sm_getidope_3,
										transitions={'done': 'GetBag'},
										autonomy={'done': Autonomy.Inherit})

			# x:286 y:536
			OperatableStateMachine.add('Follow and listen',
										_sm_follow_and_listen_2,
										transitions={'done': 'Action_Give_Back_Bag', 'failed': 'Follow and listen'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'ID': 'ID'})

			# x:508 y:523
			OperatableStateMachine.add('Action_Give_Back_Bag',
										self.use_behavior(sara_flexbe_behaviors__Action_Give_Back_BagSM, 'Action_Give_Back_Bag'),
										transitions={'finished': 'GoBack', 'failed': 'Action_Give_Back_Bag'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:42 y:161
			OperatableStateMachine.add('InitSara',
										_sm_initsara_1,
										transitions={'failed': 'failed', 'done': 'ImHere'},
										autonomy={'failed': Autonomy.Inherit, 'done': Autonomy.Inherit},
										remapping={'Pose_Init': 'Pose_Init', 'ActionStart': 'ActionStart', 'failed': 'failed', 'done': 'done'})

			# x:769 y:501
			OperatableStateMachine.add('GoBack',
										MoveBaseState(),
										transitions={'arrived': 'finished', 'failed': 'finished'},
										autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'waypoint': 'Origin'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
