#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.sara_move_base import SaraMoveBase
from sara_flexbe_states.sara_set_head_angle import SaraSetHeadAngle
from sara_flexbe_states.moveit_move import MoveitMove
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_behaviors.action_receive_bag_sm import Action_Receive_BagSM as sara_flexbe_behaviors__Action_Receive_BagSM
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_states.list_entities_by_name import list_entities_by_name
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.SetRosParam import SetRosParam
from sara_flexbe_behaviors.action_follow_sm import Action_followSM as sara_flexbe_behaviors__Action_followSM
from sara_flexbe_states.get_speech import GetSpeech
from sara_flexbe_states.regex_tester import RegexTester
from sara_flexbe_states.set_gripper_state import SetGripperState
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

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:731 y:482, x:630 y:19
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.poseStart = poseStart
		_state_machine.userdata.Pose_Init = "IdlePose"
		_state_machine.userdata.Closed_Gripper_Width = 1
		_state_machine.userdata.Open_Gripper_Width = 255
		_state_machine.userdata.ID = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:123 y:422
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
										RegexTester(regex=".*arrived*."),
										transitions={'true': 'done', 'false': 'Listen2'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'text': 'words', 'result': 'result'})


		# x:390 y:296, x:111 y:269, x:230 y:365, x:330 y:365, x:228 y:281
		_sm_follow_and_listen_1 = ConcurrencyContainer(outcomes=['done', 'failed'], input_keys=['ID'], conditions=[
										('true', [('Listen', 'done')]),
										('failed', [('Action_follow', 'failed')])
										])

		with _sm_follow_and_listen_1:
			# x:132 y:90
			OperatableStateMachine.add('Action_follow',
										self.use_behavior(sara_flexbe_behaviors__Action_followSM, 'Follow and listen/Action_follow'),
										transitions={'failed': 'failed'},
										autonomy={'failed': Autonomy.Inherit},
										remapping={'ID': 'ID'})

			# x:356 y:105
			OperatableStateMachine.add('Listen',
										_sm_listen_0,
										transitions={'done': 'true'},
										autonomy={'done': Autonomy.Inherit})


		# x:56 y:536
		_sm_getidope_2 = OperatableStateMachine(outcomes=['done'])

		with _sm_getidope_2:
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
										SetRosParam(ParamName="OpeID"),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off},
										remapping={'Value': 'ID'})


		# x:30 y:365, x:175 y:448
		_sm_initsara_3 = OperatableStateMachine(outcomes=['failed', 'done'], input_keys=['poseStart', 'Pose_Init'], output_keys=['failed', 'done'])

		with _sm_initsara_3:
			# x:41 y:77
			OperatableStateMachine.add('MoveStart',
										SaraMoveBase(),
										transitions={'arrived': 'SetHead', 'failed': 'failed'},
										autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'poseStart'})

			# x:183 y:155
			OperatableStateMachine.add('SetHead',
										SaraSetHeadAngle(pitch=0, yaw=0),
										transitions={'done': 'SetArm'},
										autonomy={'done': Autonomy.Off})

			# x:164 y:267
			OperatableStateMachine.add('SetArm',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'done', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'Pose_Init'})



		with _state_machine:
			# x:51 y:34
			OperatableStateMachine.add('InitSara',
										_sm_initsara_3,
										transitions={'failed': 'failed', 'done': 'ImHere'},
										autonomy={'failed': Autonomy.Inherit, 'done': Autonomy.Inherit},
										remapping={'poseStart': 'poseStart', 'Pose_Init': 'Pose_Init', 'failed': 'failed', 'done': 'done'})

			# x:45 y:121
			OperatableStateMachine.add('ImHere',
										SaraSay(sentence="I am here and ready", input_keys=[], emotion=0, block=True),
										transitions={'done': 'GetIDOpe'},
										autonomy={'done': Autonomy.Off})

			# x:36 y:276
			OperatableStateMachine.add('GetBag',
										SaraSay(sentence="Can you give me the bag, please", input_keys=[], emotion=0, block=True),
										transitions={'done': 'Action_Receive_Bag'},
										autonomy={'done': Autonomy.Off})

			# x:21 y:354
			OperatableStateMachine.add('Action_Receive_Bag',
										self.use_behavior(sara_flexbe_behaviors__Action_Receive_BagSM, 'Action_Receive_Bag'),
										transitions={'finished': 'Follow and listen', 'failed': 'Action_Receive_Bag'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'Closed_Gripper_Width': 'Closed_Gripper_Width', 'Open_Gripper_Width': 'Open_Gripper_Width', 'Closed_Gripper_Width': 'Closed_Gripper_Width'})

			# x:41 y:196
			OperatableStateMachine.add('GetIDOpe',
										_sm_getidope_2,
										transitions={'done': 'GetBag'},
										autonomy={'done': Autonomy.Inherit})

			# x:38 y:454
			OperatableStateMachine.add('Follow and listen',
										_sm_follow_and_listen_1,
										transitions={'done': 'SAyGiveBAck', 'failed': 'Follow and listen'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'ID': 'ID'})

			# x:390 y:493
			OperatableStateMachine.add('OPen',
										SetGripperState(width=0.1, effort=1),
										transitions={'object': 'finish', 'no_object': 'finish'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:197 y:525
			OperatableStateMachine.add('SAyGiveBAck',
										SaraSay(sentence="Here is the bag", input_keys=[], emotion=0, block=True),
										transitions={'done': 'OPen'},
										autonomy={'done': Autonomy.Off})

			# x:555 y:480
			OperatableStateMachine.add('finish',
										SaraSay(sentence="It was a pleasure to serve you", input_keys=[], emotion=0, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
