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
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_states.list_entities_by_name import list_entities_by_name
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.SetRosParam import SetRosParam
from sara_flexbe_behaviors.action_follow_sm import Action_followSM as sara_flexbe_behaviors__Action_followSM
from sara_flexbe_states.get_speech import GetSpeech
from sara_flexbe_states.regex_tester import RegexTester
from sara_flexbe_behaviors.action_give_back_bag_sm import Action_Give_Back_BagSM as sara_flexbe_behaviors__Action_Give_Back_BagSM
from flexbe_navigation_states.move_base_state import MoveBaseState
from sara_flexbe_behaviors.init_sequence_sm import Init_SequenceSM as sara_flexbe_behaviors__Init_SequenceSM
from sara_flexbe_behaviors.action_receive_bag_sm import Action_Receive_BagSM as sara_flexbe_behaviors__Action_Receive_BagSM
from sara_flexbe_behaviors.lookatclosest_sm import LookAtClosestSM as sara_flexbe_behaviors__LookAtClosestSM
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
		self.add_behavior(sara_flexbe_behaviors__Action_followSM, 'Follow and listen/Action_follow')
		self.add_behavior(sara_flexbe_behaviors__Action_Give_Back_BagSM, 'Action_Give_Back_Bag')
		self.add_behavior(sara_flexbe_behaviors__Init_SequenceSM, 'Init_Sequence')
		self.add_behavior(sara_flexbe_behaviors__Action_Receive_BagSM, 'Recevoir sac/Receive bag/Action_Receive_Bag')
		self.add_behavior(sara_flexbe_behaviors__LookAtClosestSM, 'Recevoir sac/Look at/LookAtClosest')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:

		# O 309 285 
		# Manque OpenPose, pour trouver la direction du bras pour savoir quelle sac prendre



	def create(self):
		# x:1126 y:529, x:377 y:114
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.Pose_Init = "IdlePose"
		_state_machine.userdata.Closed_Gripper_Width = 1
		_state_machine.userdata.Open_Gripper_Width = 255
		_state_machine.userdata.ID = 0
		_state_machine.userdata.PoseStart = "PoseStart"

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:30 y:365
		_sm_look_at_0 = OperatableStateMachine(outcomes=['failed'])

		with _sm_look_at_0:
			# x:105 y:160
			OperatableStateMachine.add('LookAtClosest',
										self.use_behavior(sara_flexbe_behaviors__LookAtClosestSM, 'Recevoir sac/Look at/LookAtClosest'),
										transitions={'failed': 'failed'},
										autonomy={'failed': Autonomy.Inherit})


		# x:231 y:306, x:90 y:369
		_sm_receive_bag_1 = OperatableStateMachine(outcomes=['failed', 'done'], input_keys=['Closed_Gripper_Width', 'Open_Gripper_Width'])

		with _sm_receive_bag_1:
			# x:70 y:52
			OperatableStateMachine.add('PutBAg',
										SaraSay(sentence="Please put the grocery bag in my hand", input_keys=[], emotion=1, block=False),
										transitions={'done': 'Action_Receive_Bag'},
										autonomy={'done': Autonomy.Off})

			# x:35 y:201
			OperatableStateMachine.add('Action_Receive_Bag',
										self.use_behavior(sara_flexbe_behaviors__Action_Receive_BagSM, 'Recevoir sac/Receive bag/Action_Receive_Bag'),
										transitions={'finished': 'done', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'Closed_Gripper_Width': 'Closed_Gripper_Width', 'Open_Gripper_Width': 'Open_Gripper_Width', 'Closed_Gripper_Width': 'Closed_Gripper_Width'})


		# x:30 y:365
		_sm_listen_2 = OperatableStateMachine(outcomes=['done'])

		with _sm_listen_2:
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


		# x:30 y:365, x:130 y:365, x:230 y:365, x:330 y:365, x:430 y:365
		_sm_recevoir_sac_3 = ConcurrencyContainer(outcomes=['failed', 'done'], input_keys=['Closed_Gripper_Width', 'Open_Gripper_Width'], conditions=[
										('failed', [('Receive bag', 'failed')]),
										('done', [('Receive bag', 'done')]),
										('failed', [('Look at', 'failed')])
										])

		with _sm_recevoir_sac_3:
			# x:84 y:156
			OperatableStateMachine.add('Receive bag',
										_sm_receive_bag_1,
										transitions={'failed': 'failed', 'done': 'done'},
										autonomy={'failed': Autonomy.Inherit, 'done': Autonomy.Inherit},
										remapping={'Closed_Gripper_Width': 'Closed_Gripper_Width', 'Open_Gripper_Width': 'Open_Gripper_Width'})

			# x:262 y:154
			OperatableStateMachine.add('Look at',
										_sm_look_at_0,
										transitions={'failed': 'failed'},
										autonomy={'failed': Autonomy.Inherit})


		# x:390 y:296, x:111 y:269, x:230 y:365, x:330 y:365
		_sm_follow_and_listen_4 = ConcurrencyContainer(outcomes=['done', 'failed'], input_keys=['ID'], conditions=[
										('failed', [('Action_follow', 'failed')]),
										('done', [('Listen', 'done')])
										])

		with _sm_follow_and_listen_4:
			# x:132 y:90
			OperatableStateMachine.add('Action_follow',
										self.use_behavior(sara_flexbe_behaviors__Action_followSM, 'Follow and listen/Action_follow'),
										transitions={'failed': 'failed'},
										autonomy={'failed': Autonomy.Inherit},
										remapping={'ID': 'ID'})

			# x:356 y:105
			OperatableStateMachine.add('Listen',
										_sm_listen_2,
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Inherit})


		# x:76 y:535
		_sm_getidope_5 = OperatableStateMachine(outcomes=['done'], output_keys=['ID'])

		with _sm_getidope_5:
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
			# x:46 y:41
			OperatableStateMachine.add('GEtPose',
										Get_Robot_Pose(),
										transitions={'done': 'Init_Sequence'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose': 'Origin'})

			# x:36 y:236
			OperatableStateMachine.add('ImHere',
										SaraSay(sentence="I am ready to carry your luggages!", input_keys=[], emotion=1, block=True),
										transitions={'done': 'GetIDOpe'},
										autonomy={'done': Autonomy.Off})

			# x:49 y:439
			OperatableStateMachine.add('GetBag',
										SaraSay(sentence="Can you give me the bag, please.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'Recevoir sac'},
										autonomy={'done': Autonomy.Off})

			# x:35 y:326
			OperatableStateMachine.add('GetIDOpe',
										_sm_getidope_5,
										transitions={'done': 'GetBag'},
										autonomy={'done': Autonomy.Inherit},
										remapping={'ID': 'ID'})

			# x:241 y:536
			OperatableStateMachine.add('Follow and listen',
										_sm_follow_and_listen_4,
										transitions={'done': 'Action_Give_Back_Bag', 'failed': 'Follow and listen'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'ID': 'ID'})

			# x:446 y:525
			OperatableStateMachine.add('Action_Give_Back_Bag',
										self.use_behavior(sara_flexbe_behaviors__Action_Give_Back_BagSM, 'Action_Give_Back_Bag'),
										transitions={'finished': 'GoBackHome', 'failed': 'Action_Give_Back_Bag'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:870 y:515
			OperatableStateMachine.add('GoBack',
										MoveBaseState(),
										transitions={'arrived': 'finished', 'failed': 'finished'},
										autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'waypoint': 'Origin'})

			# x:22 y:150
			OperatableStateMachine.add('Init_Sequence',
										self.use_behavior(sara_flexbe_behaviors__Init_SequenceSM, 'Init_Sequence'),
										transitions={'finished': 'ImHere', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:54 y:546
			OperatableStateMachine.add('Recevoir sac',
										_sm_recevoir_sac_3,
										transitions={'failed': 'failed', 'done': 'Follow and listen'},
										autonomy={'failed': Autonomy.Inherit, 'done': Autonomy.Inherit},
										remapping={'Closed_Gripper_Width': 'Closed_Gripper_Width', 'Open_Gripper_Width': 'Open_Gripper_Width'})

			# x:682 y:515
			OperatableStateMachine.add('GoBackHome',
										SaraSay(sentence="I will go back home now, bye", input_keys=[], emotion=0, block=True),
										transitions={'done': 'GoBack'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
