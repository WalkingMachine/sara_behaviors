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
from sara_flexbe_behaviors.init_sequence_sm import Init_SequenceSM as sara_flexbe_behaviors__Init_SequenceSM
from sara_flexbe_behaviors.action_move_sm import Action_MoveSM as sara_flexbe_behaviors__Action_MoveSM
from sara_flexbe_states.sara_set_head_angle import SaraSetHeadAngle
from sara_flexbe_states.GetPointedPositionOnPlane import GetPointedPositionOnPlane
from sara_flexbe_states.get_reachable_waypoint import Get_Reacheable_Waypoint
from sara_flexbe_states.sara_move_base import SaraMoveBase
from sara_flexbe_behaviors.action_point_at_sm import Action_point_atSM as sara_flexbe_behaviors__Action_point_atSM
from sara_flexbe_states.LookAtPos import LookAtPos
from sara_flexbe_behaviors.action_receive_bag_sm import Action_Receive_BagSM as sara_flexbe_behaviors__Action_Receive_BagSM
from flexbe_states.wait_state import WaitState
from sara_flexbe_states.set_gripper_state import SetGripperState
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
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'Action_Move')
		self.add_behavior(sara_flexbe_behaviors__Action_point_atSM, 'recevoir sac/Recevoir sac/look at bag/designate bag/point at it/Action_point_at')
		self.add_behavior(sara_flexbe_behaviors__Action_Receive_BagSM, 'recevoir sac/Recevoir sac/receive it/Action_Receive_Bag')
		self.add_behavior(sara_flexbe_behaviors__LookAtClosestSM, 'recevoir sac/LookAtClosest')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:

		# O 287 357 
		# Manque OpenPose, pour trouver la direction du bras pour savoir quelle sac prendre



	def create(self):
		# x:1103 y:529, x:321 y:227
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
		_sm_look_in_the_eyes_0 = OperatableStateMachine(outcomes=['finished'])

		with _sm_look_in_the_eyes_0:
			# x:189 y:48
			OperatableStateMachine.add('wait 3',
										WaitState(wait_time=3),
										transitions={'done': 'say ready'},
										autonomy={'done': Autonomy.Off})

			# x:171 y:288
			OperatableStateMachine.add('reset head',
										SaraSetHeadAngle(pitch=0.1, yaw=0),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:164 y:163
			OperatableStateMachine.add('say ready',
										SaraSay(sentence="Good, I see you want this bag. But, could you hand it to me please?", input_keys=[], emotion=0, block=True),
										transitions={'done': 'reset head'},
										autonomy={'done': Autonomy.Off})


		# x:30 y:365
		_sm_look_at_it_1 = OperatableStateMachine(outcomes=['fail'], input_keys=['position'])

		with _sm_look_at_it_1:
			# x:126 y:99
			OperatableStateMachine.add('look',
										LookAtPos(),
										transitions={'failed': 'look', 'done': 'look'},
										autonomy={'failed': Autonomy.Off, 'done': Autonomy.Off},
										remapping={'pos': 'position'})


		# x:30 y:365
		_sm_point_at_it_2 = OperatableStateMachine(outcomes=['finished'], input_keys=['position'])

		with _sm_point_at_it_2:
			# x:112 y:202
			OperatableStateMachine.add('Action_point_at',
										self.use_behavior(sara_flexbe_behaviors__Action_point_atSM, 'recevoir sac/Recevoir sac/look at bag/designate bag/point at it/Action_point_at'),
										transitions={'finished': 'Action_point_at', 'failed': 'Action_point_at'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'targetPoint': 'position'})


		# x:30 y:365
		_sm_move_to_it_3 = OperatableStateMachine(outcomes=['arrived'], input_keys=['position'])

		with _sm_move_to_it_3:
			# x:204 y:52
			OperatableStateMachine.add('set distance',
										SetKey(Value=1),
										transitions={'done': 'get pose'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'distance'})

			# x:211 y:185
			OperatableStateMachine.add('get pose',
										Get_Reacheable_Waypoint(),
										transitions={'done': 'move to bag'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose_in': 'position', 'distance': 'distance', 'pose_out': 'pose'})

			# x:188 y:279
			OperatableStateMachine.add('move to bag',
										SaraMoveBase(reference="map"),
										transitions={'arrived': 'arrived', 'failed': 'arrived'},
										autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'pose'})


		# x:30 y:365, x:130 y:365, x:230 y:365, x:330 y:365
		_sm_designate_bag_4 = ConcurrencyContainer(outcomes=['finished'], input_keys=['position'], conditions=[
										('finished', [('look at it', 'fail')]),
										('finished', [('point at it', 'finished')]),
										('finished', [('move to it', 'arrived')])
										])

		with _sm_designate_bag_4:
			# x:499 y:118
			OperatableStateMachine.add('move to it',
										_sm_move_to_it_3,
										transitions={'arrived': 'finished'},
										autonomy={'arrived': Autonomy.Inherit},
										remapping={'position': 'position'})

			# x:239 y:126
			OperatableStateMachine.add('point at it',
										_sm_point_at_it_2,
										transitions={'finished': 'finished'},
										autonomy={'finished': Autonomy.Inherit},
										remapping={'position': 'position'})

			# x:45 y:121
			OperatableStateMachine.add('look at it',
										_sm_look_at_it_1,
										transitions={'fail': 'finished'},
										autonomy={'fail': Autonomy.Inherit},
										remapping={'position': 'position'})


		# x:30 y:365, x:130 y:365, x:230 y:365, x:330 y:365
		_sm_receive_it_5 = ConcurrencyContainer(outcomes=['finished', 'failed'], input_keys=['Closed_Gripper_Width', 'Open_Gripper_Width'], conditions=[
										('finished', [('Action_Receive_Bag', 'finished'), ('look in the eyes', 'finished')]),
										('failed', [('Action_Receive_Bag', 'failed')])
										])

		with _sm_receive_it_5:
			# x:30 y:149
			OperatableStateMachine.add('Action_Receive_Bag',
										self.use_behavior(sara_flexbe_behaviors__Action_Receive_BagSM, 'recevoir sac/Recevoir sac/receive it/Action_Receive_Bag'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'Closed_Gripper_Width': 'Closed_Gripper_Width', 'Open_Gripper_Width': 'Open_Gripper_Width', 'Closed_Gripper_Width': 'Closed_Gripper_Width'})

			# x:259 y:150
			OperatableStateMachine.add('look in the eyes',
										_sm_look_in_the_eyes_0,
										transitions={'finished': 'finished'},
										autonomy={'finished': Autonomy.Inherit})


		# x:30 y:322
		_sm_look_at_bag_6 = OperatableStateMachine(outcomes=['finished'])

		with _sm_look_at_bag_6:
			# x:35 y:70
			OperatableStateMachine.add('setName',
										SetKey(Value="person"),
										transitions={'done': 'say 1'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'personName'})

			# x:233 y:109
			OperatableStateMachine.add('say 1',
										SaraSay(sentence="Please, point at the bag you want.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'list'},
										autonomy={'done': Autonomy.Off})

			# x:28 y:193
			OperatableStateMachine.add('list',
										list_entities_by_name(frontality_level=0.5, distance_max=10),
										transitions={'found': 'calc', 'none_found': 'list'},
										autonomy={'found': Autonomy.Off, 'none_found': Autonomy.Off},
										remapping={'name': 'personName', 'entity_list': 'entity_list', 'number': 'number'})

			# x:230 y:363
			OperatableStateMachine.add('get bag position from pointing',
										GetPointedPositionOnPlane(planeHeight=0.2),
										transitions={'done': 'designate bag', 'not_pointing': 'say 1', 'pointing_up': 'say 1', 'failed': 'list'},
										autonomy={'done': Autonomy.Off, 'not_pointing': Autonomy.Off, 'pointing_up': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'entity': 'entity', 'position': 'position'})

			# x:34 y:362
			OperatableStateMachine.add('calc',
										CalculationState(calculation=lambda x: x[0]),
										transitions={'done': 'get bag position from pointing'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'entity_list', 'output_value': 'entity'})

			# x:241 y:554
			OperatableStateMachine.add('designate bag',
										_sm_designate_bag_4,
										transitions={'finished': 'finished'},
										autonomy={'finished': Autonomy.Inherit},
										remapping={'position': 'position'})


		# x:30 y:365, x:130 y:365
		_sm_recevoir_sac_7 = OperatableStateMachine(outcomes=['failed', 'done'], input_keys=['Closed_Gripper_Width', 'Open_Gripper_Width'])

		with _sm_recevoir_sac_7:
			# x:66 y:44
			OperatableStateMachine.add('look at bag',
										_sm_look_at_bag_6,
										transitions={'finished': 'close'},
										autonomy={'finished': Autonomy.Inherit})

			# x:41 y:267
			OperatableStateMachine.add('receive it',
										_sm_receive_it_5,
										transitions={'finished': 'done', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'Closed_Gripper_Width': 'Closed_Gripper_Width', 'Open_Gripper_Width': 'Open_Gripper_Width'})

			# x:81 y:157
			OperatableStateMachine.add('close',
										SetGripperState(width=0, effort=0),
										transitions={'object': 'receive it', 'no_object': 'receive it'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})


		# x:30 y:365
		_sm_listen_8 = OperatableStateMachine(outcomes=['done'])

		with _sm_listen_8:
			# x:50 y:76
			OperatableStateMachine.add('SayFollow',
										SaraSay(sentence="I will follow you to the car now. Tell me when we get to the car.", input_keys=[], emotion=0, block=False),
										transitions={'done': 'LIsten'},
										autonomy={'done': Autonomy.Off})

			# x:161 y:148
			OperatableStateMachine.add('LIsten',
										GetSpeech(watchdog=10),
										transitions={'done': 'Listen2', 'nothing': 'LIsten', 'fail': 'LIsten'},
										autonomy={'done': Autonomy.Off, 'nothing': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'words': 'words'})

			# x:201 y:256
			OperatableStateMachine.add('Listen2',
										RegexTester(regex=".*((car)|(here it is)|(now)).*"),
										transitions={'true': 'done', 'false': 'Listen2'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'text': 'words', 'result': 'result'})


		# x:30 y:365, x:130 y:365, x:230 y:365, x:330 y:365, x:430 y:365
		_sm_recevoir_sac_9 = ConcurrencyContainer(outcomes=['failed', 'done'], input_keys=['Closed_Gripper_Width', 'Open_Gripper_Width'], conditions=[
										('failed', [('Recevoir sac', 'failed')]),
										('done', [('Recevoir sac', 'done')]),
										('done', [('LookAtClosest', 'failed')])
										])

		with _sm_recevoir_sac_9:
			# x:30 y:40
			OperatableStateMachine.add('Recevoir sac',
										_sm_recevoir_sac_7,
										transitions={'failed': 'failed', 'done': 'done'},
										autonomy={'failed': Autonomy.Inherit, 'done': Autonomy.Inherit},
										remapping={'Closed_Gripper_Width': 'Closed_Gripper_Width', 'Open_Gripper_Width': 'Open_Gripper_Width'})

			# x:234 y:114
			OperatableStateMachine.add('LookAtClosest',
										self.use_behavior(sara_flexbe_behaviors__LookAtClosestSM, 'recevoir sac/LookAtClosest'),
										transitions={'failed': 'done'},
										autonomy={'failed': Autonomy.Inherit})


		# x:390 y:296, x:111 y:269, x:230 y:365, x:330 y:365
		_sm_follow_and_listen_10 = ConcurrencyContainer(outcomes=['done', 'failed'], input_keys=['ID'], conditions=[
										('failed', [('Action_follow', 'failed')]),
										('done', [('Listen', 'done')])
										])

		with _sm_follow_and_listen_10:
			# x:132 y:90
			OperatableStateMachine.add('Action_follow',
										self.use_behavior(sara_flexbe_behaviors__Action_followSM, 'Follow and listen/Action_follow'),
										transitions={'failed': 'failed'},
										autonomy={'failed': Autonomy.Inherit},
										remapping={'ID': 'ID'})

			# x:356 y:105
			OperatableStateMachine.add('Listen',
										_sm_listen_8,
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Inherit})


		# x:76 y:535
		_sm_getidope_11 = OperatableStateMachine(outcomes=['done'], output_keys=['ID'])

		with _sm_getidope_11:
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

			# x:35 y:321
			OperatableStateMachine.add('ImHere',
										SaraSay(sentence="I am ready to carry your luggage!", input_keys=[], emotion=1, block=True),
										transitions={'done': 'recevoir sac'},
										autonomy={'done': Autonomy.Off})

			# x:28 y:539
			OperatableStateMachine.add('GetIDOpe',
										_sm_getidope_11,
										transitions={'done': 'Follow and listen'},
										autonomy={'done': Autonomy.Inherit},
										remapping={'ID': 'ID'})

			# x:220 y:536
			OperatableStateMachine.add('Follow and listen',
										_sm_follow_and_listen_10,
										transitions={'done': 'Action_Give_Back_Bag', 'failed': 'failed'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'ID': 'ID'})

			# x:411 y:525
			OperatableStateMachine.add('Action_Give_Back_Bag',
										self.use_behavior(sara_flexbe_behaviors__Action_Give_Back_BagSM, 'Action_Give_Back_Bag'),
										transitions={'finished': 'GoBackHome', 'failed': 'Action_Give_Back_Bag'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:24 y:135
			OperatableStateMachine.add('Init_Sequence',
										self.use_behavior(sara_flexbe_behaviors__Init_SequenceSM, 'Init_Sequence'),
										transitions={'finished': 'move head up', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:634 y:522
			OperatableStateMachine.add('GoBackHome',
										SaraSay(sentence="I will go back home now. Have a good day!", input_keys=[], emotion=0, block=True),
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Off})

			# x:827 y:516
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'Action_Move'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'Origin'})

			# x:35 y:230
			OperatableStateMachine.add('move head up',
										SaraSetHeadAngle(pitch=0.1, yaw=0),
										transitions={'done': 'ImHere'},
										autonomy={'done': Autonomy.Off})

			# x:35 y:427
			OperatableStateMachine.add('recevoir sac',
										_sm_recevoir_sac_9,
										transitions={'failed': 'failed', 'done': 'GetIDOpe'},
										autonomy={'failed': Autonomy.Inherit, 'done': Autonomy.Inherit},
										remapping={'Closed_Gripper_Width': 'Closed_Gripper_Width', 'Open_Gripper_Width': 'Open_Gripper_Width'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
