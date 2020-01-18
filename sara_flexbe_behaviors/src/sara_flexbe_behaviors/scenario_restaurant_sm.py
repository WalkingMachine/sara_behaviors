#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_states.sara_say import SaraSay
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.get_robot_pose import Get_Robot_Pose
from sara_flexbe_behaviors.action_findpersonbyquestion_sm import Action_FindPersonByQuestionSM as Action_FindPersonByQuestionSM

from sara_flexbe_states.FilterKey import FilterKey
from sara_flexbe_states.list_entities_by_name import list_entities_by_name
from sara_flexbe_states.sara_set_head_angle import SaraSetHeadAngle
from flexbe_states.wait_state import WaitState
from sara_flexbe_states.sara_move_base import SaraMoveBase
from sara_flexbe_states.pose_gen_euler import GenPoseEuler
from sara_flexbe_states.get_reachable_waypoint import Get_Reacheable_Waypoint
from sara_flexbe_states.GetAttribute import GetAttribute
from sara_flexbe_behaviors.action_move_sm import Action_MoveSM as Action_MoveSM
from sara_flexbe_behaviors.action_ask_sm import Action_AskSM as Action_AskSM

from sara_flexbe_states.KeepLookingAt import KeepLookingAt
from sara_flexbe_states.sara_nlu_restaurant import SaraNLUrestaurant
from sara_flexbe_behaviors.action_findpersonbyid_sm import Action_findPersonByIDSM as Action_findPersonByIDSM
from flexbe_states.check_condition_state import CheckConditionState
from flexbe_states.flexible_check_condition_state import FlexibleCheckConditionState
from sara_flexbe_behaviors.action_find_sm import Action_findSM as Action_findSM
from sara_flexbe_behaviors.action_pick_sm import Action_pickSM as Action_pickSM
from sara_flexbe_states.set_gripper_state import SetGripperState
from flexbe_states.flexible_calculation_state import FlexibleCalculationState
from sara_flexbe_states.run_trajectory import RunTrajectory
from sara_flexbe_states.GetPositionToPlaceOnTable import GetPositionToPlaceOnTable
from sara_flexbe_behaviors.action_place_sm import Action_placeSM as Action_placeSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Tue May 28 2019
@author: Quentin Gaillot
'''
class Scenario_RestaurantSM(Behavior):
	'''
	Scenario restaurant 2019
	'''


	def __init__(self):
		super(Scenario_RestaurantSM, self).__init__()
		self.name = 'Scenario_Restaurant'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(Action_FindPersonByQuestionSM, 'save bar position and initiation/Action_FindPersonByQuestion')
		self.add_behavior(Action_MoveSM, 'move to table and save position/Action_Move')
		self.add_behavior(Action_AskSM, 'ask and save order/ask AND look person/ask/Action_Ask')
		self.add_behavior(Action_MoveSM, 'go to the barman/Action_Move')
		self.add_behavior(Action_findPersonByIDSM, 'go to the barman/Action_findPersonByID')
		self.add_behavior(Action_findSM, 'take objects and bring the order to customer/Action_find')
		self.add_behavior(Action_pickSM, 'take objects and bring the order to customer/Action_pick')
		self.add_behavior(Action_MoveSM, 'take objects and bring the order to customer/Action_Move')
		self.add_behavior(Action_MoveSM, 'take objects and bring the order to customer/Action_Move_2')
		self.add_behavior(Action_findSM, 'take objects and bring the order to customer/find table and place/Action_find_2')
		self.add_behavior(Action_placeSM, 'take objects and bring the order to customer/find table and place/Action_place')
		self.add_behavior(Action_MoveSM, 'Action_Move')


		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:902 y:757, x:882 y:161
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:1232 y:907, x:1267 y:613, x:1271 y:566
		_sm_find_table_and_place_0 = OperatableStateMachine(outcomes=['finished', 'failed', 'no_table'])

		with _sm_find_table_and_place_0:
			# x:877 y:673
			OperatableStateMachine.add('run traj',
										RunTrajectory(file="receive_object", duration=0),
										transitions={'done': 'say release'},
										autonomy={'done': Autonomy.Off})

			# x:532 y:572
			OperatableStateMachine.add('Action_find_2',
										self.use_behavior(Action_findSM, 'take objects and bring the order to customer/find table and place/Action_find_2'),
										transitions={'done': 'get table position', 'failed': 'say do not find table'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'className': 'tableKey', 'entity': 'tableEntity'})

			# x:576 y:514
			OperatableStateMachine.add('set tableKey',
										SetKey(Value="table"),
										transitions={'done': 'Action_find_2'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'tableKey'})

			# x:538 y:638
			OperatableStateMachine.add('get table position',
										CalculationState(calculation=lambda x: x.position),
										transitions={'done': 'Action_place'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'tableEntity', 'output_value': 'pose'})

			# x:736 y:677
			OperatableStateMachine.add('say do not find table',
										SaraSay(sentence="I can not find the table. Please be ready to grab the object.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'run traj'},
										autonomy={'done': Autonomy.Off})

			# x:41 y:231
			OperatableStateMachine.add('find a table and a free spot',
										GetPositionToPlaceOnTable(),
										transitions={'done': 'Action_place', 'not_found': 'look down_left'},
										autonomy={'done': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'distanceFromEdge': 'distanceFromEdge', 'position': 'pose'})

			# x:291 y:805
			OperatableStateMachine.add('Action_place',
										self.use_behavior(Action_placeSM, 'take objects and bring the order to customer/find table and place/Action_place'),
										transitions={'finished': 'finished', 'failed': 'say do not find table'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pos': 'pose'})

			# x:50 y:102
			OperatableStateMachine.add('look down',
										SaraSetHeadAngle(pitch=0, yaw=0.7),
										transitions={'done': 'wait'},
										autonomy={'done': Autonomy.Off})

			# x:214 y:378
			OperatableStateMachine.add('find a table and a free spot_2',
										GetPositionToPlaceOnTable(),
										transitions={'done': 'Action_place', 'not_found': 'look down_right'},
										autonomy={'done': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'distanceFromEdge': 'distanceFromEdge', 'position': 'pose'})

			# x:240 y:232
			OperatableStateMachine.add('look down_left',
										SaraSetHeadAngle(pitch=0.7, yaw=0.6),
										transitions={'done': 'wait_2'},
										autonomy={'done': Autonomy.Off})

			# x:387 y:513
			OperatableStateMachine.add('find a table and a free spot_2_2',
										GetPositionToPlaceOnTable(),
										transitions={'done': 'Action_place', 'not_found': 'set tableKey'},
										autonomy={'done': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'distanceFromEdge': 'distanceFromEdge', 'position': 'pose'})

			# x:402 y:378
			OperatableStateMachine.add('look down_right',
										SaraSetHeadAngle(pitch=-0.7, yaw=0.6),
										transitions={'done': 'wait_3'},
										autonomy={'done': Autonomy.Off})

			# x:66 y:169
			OperatableStateMachine.add('wait',
										WaitState(wait_time=3),
										transitions={'done': 'find a table and a free spot'},
										autonomy={'done': Autonomy.Off})

			# x:242 y:294
			OperatableStateMachine.add('wait_2',
										WaitState(wait_time=3),
										transitions={'done': 'find a table and a free spot_2'},
										autonomy={'done': Autonomy.Off})

			# x:411 y:444
			OperatableStateMachine.add('wait_3',
										WaitState(wait_time=3),
										transitions={'done': 'find a table and a free spot_2_2'},
										autonomy={'done': Autonomy.Off})

			# x:1000 y:670
			OperatableStateMachine.add('say release',
										SaraSay(sentence="Here is your order. I will open my gripper in 3, 2, 1, now.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'open gripper'},
										autonomy={'done': Autonomy.Off})

			# x:1122 y:666
			OperatableStateMachine.add('open gripper',
										SetGripperState(width=0.1, effort=1),
										transitions={'object': 'say good day', 'no_object': 'say good day'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:62 y:29
			OperatableStateMachine.add('set distance',
										SetKey(Value=0.3),
										transitions={'done': 'look down'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'distanceFromEdge'})

			# x:1170 y:771
			OperatableStateMachine.add('say good day',
										SaraSay(sentence="Thank you. Have a good day.", input_keys=[], emotion=6, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		# x:30 y:458, x:130 y:458
		_sm_keep_looking_1 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['personID'])

		with _sm_keep_looking_1:
			# x:30 y:40
			OperatableStateMachine.add('keep',
										KeepLookingAt(),
										transitions={'failed': 'keep'},
										autonomy={'failed': Autonomy.Off},
										remapping={'ID': 'personID'})


		# x:30 y:458, x:130 y:458
		_sm_ask_2 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['question'], output_keys=['answer'])

		with _sm_ask_2:
			# x:30 y:40
			OperatableStateMachine.add('Action_Ask',
										self.use_behavior(Action_AskSM, 'ask and save order/ask AND look person/ask/Action_Ask'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'question': 'question', 'answer': 'answer'})


		# x:30 y:458, x:130 y:458
		_sm_confirm_order_3 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['orderList'])

		with _sm_confirm_order_3:
			# x:114 y:67
			OperatableStateMachine.add('produce question',
										CalculationState(calculation=lambda x: "Did you order :" + str(x[0])),
										transitions={'done': 'Action_Ask'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'orderList', 'output_value': 'question'})

			# x:423 y:171
			OperatableStateMachine.add('Action_Ask',
										self.use_behavior(sara_flexbe_behaviors__Action_AskSM, 'ask and save order/confirm order/Action_Ask'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'question': 'question', 'answer': 'answer'})


		# x:348 y:66, x:351 y:97, x:339 y:159, x:336 y:195, x:518 y:89, x:515 y:175
		_sm_ask_and_look_person_4 = ConcurrencyContainer(outcomes=['finished', 'failed'], input_keys=['personID', 'question'], output_keys=['answer'], conditions=[
										('finished', [('ask', 'finished')]),
										('failed', [('ask', 'failed')]),
										('finished', [('keep looking', 'finished')]),
										('failed', [('keep looking', 'failed')])
										])

		with _sm_ask_and_look_person_4:
			# x:30 y:40
			OperatableStateMachine.add('ask',
										_sm_ask_2,
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'question': 'question', 'answer': 'answer'})

			# x:30 y:138
			OperatableStateMachine.add('keep looking',
										_sm_keep_looking_1,
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'personID': 'personID'})


		# x:30 y:458
		_sm_look_around_2_5 = OperatableStateMachine(outcomes=['finished'])

		with _sm_look_around_2_5:
			# x:215 y:156
			OperatableStateMachine.add('center',
										SaraSetHeadAngle(pitch=0.1, yaw=0),
										transitions={'done': 'w2'},
										autonomy={'done': Autonomy.Off})

			# x:394 y:262
			OperatableStateMachine.add('right',
										SaraSetHeadAngle(pitch=0.1, yaw=-1.5),
										transitions={'done': 'w3'},
										autonomy={'done': Autonomy.Off})

			# x:206 y:372
			OperatableStateMachine.add('center2',
										SaraSetHeadAngle(pitch=0.1, yaw=0),
										transitions={'done': 'w4'},
										autonomy={'done': Autonomy.Off})

			# x:38 y:596
			OperatableStateMachine.add('w1',
										WaitState(wait_time=4),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:413 y:159
			OperatableStateMachine.add('w2',
										WaitState(wait_time=4),
										transitions={'done': 'right'},
										autonomy={'done': Autonomy.Off})

			# x:415 y:370
			OperatableStateMachine.add('w3',
										WaitState(wait_time=4),
										transitions={'done': 'center2'},
										autonomy={'done': Autonomy.Off})

			# x:39 y:371
			OperatableStateMachine.add('w4',
										WaitState(wait_time=4),
										transitions={'done': 'left'},
										autonomy={'done': Autonomy.Off})

			# x:25 y:482
			OperatableStateMachine.add('left',
										SaraSetHeadAngle(pitch=0.1, yaw=1.5),
										transitions={'done': 'w1'},
										autonomy={'done': Autonomy.Off})


		# x:30 y:458
		_sm_look_around_6 = OperatableStateMachine(outcomes=['finished'])

		with _sm_look_around_6:
			# x:215 y:156
			OperatableStateMachine.add('center',
										SaraSetHeadAngle(pitch=0.1, yaw=0),
										transitions={'done': 'w2'},
										autonomy={'done': Autonomy.Off})

			# x:394 y:262
			OperatableStateMachine.add('right',
										SaraSetHeadAngle(pitch=0.1, yaw=-1.5),
										transitions={'done': 'w3'},
										autonomy={'done': Autonomy.Off})

			# x:206 y:372
			OperatableStateMachine.add('center2',
										SaraSetHeadAngle(pitch=0.1, yaw=0),
										transitions={'done': 'w4'},
										autonomy={'done': Autonomy.Off})

			# x:38 y:596
			OperatableStateMachine.add('w1',
										WaitState(wait_time=4),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:413 y:159
			OperatableStateMachine.add('w2',
										WaitState(wait_time=4),
										transitions={'done': 'right'},
										autonomy={'done': Autonomy.Off})

			# x:415 y:370
			OperatableStateMachine.add('w3',
										WaitState(wait_time=4),
										transitions={'done': 'center2'},
										autonomy={'done': Autonomy.Off})

			# x:39 y:371
			OperatableStateMachine.add('w4',
										WaitState(wait_time=4),
										transitions={'done': 'left'},
										autonomy={'done': Autonomy.Off})

			# x:25 y:482
			OperatableStateMachine.add('left',
										SaraSetHeadAngle(pitch=0.1, yaw=1.5),
										transitions={'done': 'w1'},
										autonomy={'done': Autonomy.Off})


		# x:30 y:458, x:130 y:458
		_sm_turn_around_7 = OperatableStateMachine(outcomes=['finished', 'failed'])

		with _sm_turn_around_7:
			# x:80 y:26
			OperatableStateMachine.add('look around',
										_sm_look_around_6,
										transitions={'finished': 'pose with 180 rotation'},
										autonomy={'finished': Autonomy.Inherit})

			# x:66 y:286
			OperatableStateMachine.add('rotation',
										SaraMoveBase(reference="base_link"),
										transitions={'arrived': 'look around_2', 'failed': 'failed'},
										autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'pose'})

			# x:56 y:388
			OperatableStateMachine.add('look around_2',
										_sm_look_around_2_5,
										transitions={'finished': 'finished'},
										autonomy={'finished': Autonomy.Inherit})

			# x:63 y:133
			OperatableStateMachine.add('pose with 180 rotation',
										GenPoseEuler(x=0, y=0, z=0, roll=0, pitch=0, yaw=3.14),
										transitions={'done': 'rotation'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose': 'pose'})


		# x:30 y:458
		_sm_get_waving_people_8 = OperatableStateMachine(outcomes=['finished'], output_keys=['waving_person'])

		with _sm_get_waving_people_8:
			# x:47 y:45
			OperatableStateMachine.add('set name',
										SetKey(Value="person"),
										transitions={'done': 'list people'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'name'})

			# x:40 y:236
			OperatableStateMachine.add('filter waving',
										FilterKey(filter_function=lambda x: x[0].pose.right_arm_up or x[0].pose.left_arm_up, input_keys=["input_list"]),
										transitions={'not_empty': 'get first', 'empty': 'list people'},
										autonomy={'not_empty': Autonomy.Off, 'empty': Autonomy.Off},
										remapping={'input_list': 'entity_list', 'output_list': 'waving_peoples'})

			# x:53 y:326
			OperatableStateMachine.add('get first',
										CalculationState(calculation=lambda x: x[0]),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'waving_peoples', 'output_value': 'waving_person'})

			# x:40 y:133
			OperatableStateMachine.add('list people',
										list_entities_by_name(frontality_level=0.5, distance_max=5),
										transitions={'found': 'filter waving', 'none_found': 'list people'},
										autonomy={'found': Autonomy.Off, 'none_found': Autonomy.Off},
										remapping={'name': 'name', 'entity_list': 'entity_list', 'number': 'number'})


		# x:30 y:458, x:130 y:458, x:230 y:458, x:330 y:458, x:430 y:458
		_sm_look_for_waving_people_9 = ConcurrencyContainer(outcomes=['finished', 'failed'], output_keys=['waving_person'], conditions=[
										('failed', [('turn around', 'failed')]),
										('failed', [('turn around', 'finished')]),
										('finished', [('get waving people', 'finished')])
										])

		with _sm_look_for_waving_people_9:
			# x:268 y:118
			OperatableStateMachine.add('get waving people',
										_sm_get_waving_people_8,
										transitions={'finished': 'finished'},
										autonomy={'finished': Autonomy.Inherit},
										remapping={'waving_person': 'waving_person'})

			# x:60 y:126
			OperatableStateMachine.add('turn around',
										_sm_turn_around_7,
										transitions={'finished': 'failed', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})


		# x:441 y:583, x:93 y:568
		_sm_repeate_if_first_commande_10 = OperatableStateMachine(outcomes=['finished', 'repeate'], input_keys=['commandNumber'], output_keys=['commandNumber'])

		with _sm_repeate_if_first_commande_10:
			# x:242 y:97
			OperatableStateMachine.add('if first command',
										CheckConditionState(predicate=lambda x: x == 1),
										transitions={'true': 'set second command', 'false': 'finished'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'commandNumber'})

			# x:73 y:329
			OperatableStateMachine.add('set second command',
										SetKey(Value=2),
										transitions={'done': 'repeate'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'commandNumber'})


		# x:913 y:749, x:1068 y:149
		_sm_take_objects_and_bring_the_order_to_customer_11 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['barPosition', 'orderList', 'robotPositionToCustomer'])

		with _sm_take_objects_and_bring_the_order_to_customer_11:
			# x:73 y:26
			OperatableStateMachine.add('set indexkey',
										SetKey(Value=0),
										transitions={'done': 'one element by one element from the list'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'indexKey'})

			# x:657 y:111
			OperatableStateMachine.add('increment indexKey',
										CalculationState(calculation=lambda x: x+1),
										transitions={'done': 'one element by one element from the list'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'indexKey', 'output_value': 'indexKey'})

			# x:642 y:728
			OperatableStateMachine.add('check if end of the list',
										FlexibleCheckConditionState(predicate=lambda x: len(x[0]) <= x[1], input_keys=["orderList", "indexKey"]),
										transitions={'true': 'finished', 'false': 'Action_Move_2'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'orderList': 'orderList', 'indexKey': 'indexKey'})

			# x:62 y:258
			OperatableStateMachine.add('Action_find',
										self.use_behavior(Action_findSM, 'take objects and bring the order to customer/Action_find'),
										transitions={'done': 'get entity ID', 'failed': 'say cannot find'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'className': 'item', 'entity': 'entity'})

			# x:76 y:183
			OperatableStateMachine.add('say search and grip',
										SaraSay(sentence=lambda x: "I am now searching the "+x[0]+".", input_keys=["item"], emotion=0, block=True),
										transitions={'done': 'Action_find'},
										autonomy={'done': Autonomy.Off},
										remapping={'item': 'item'})

			# x:258 y:261
			OperatableStateMachine.add('say cannot find',
										SaraSay(sentence="I cannot find the item.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'place arm'},
										autonomy={'done': Autonomy.Off})

			# x:63 y:393
			OperatableStateMachine.add('Action_pick',
										self.use_behavior(Action_pickSM, 'take objects and bring the order to customer/Action_pick'),
										transitions={'success': 'say go to the customer', 'unreachable': 'say cannot pick', 'not found': 'say cannot pick', 'dropped': 'say cannot pick'},
										autonomy={'success': Autonomy.Inherit, 'unreachable': Autonomy.Inherit, 'not found': Autonomy.Inherit, 'dropped': Autonomy.Inherit},
										remapping={'objectID': 'entityID'})

			# x:61 y:548
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(Action_MoveSM, 'take objects and bring the order to customer/Action_Move'),
										transitions={'finished': 'find table and place', 'failed': 'say cant get back to customer'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'robotPositionToCustomer'})

			# x:83 y:326
			OperatableStateMachine.add('get entity ID',
										CalculationState(calculation=lambda x: x.ID),
										transitions={'done': 'Action_pick'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'entity', 'output_value': 'entityID'})

			# x:568 y:407
			OperatableStateMachine.add('say put in the gripper',
										SaraSay(sentence=lambda x: "Please, put the "+x[0]+" in my gripper. I will close it in 3, 2, 1, now.", input_keys=["item"], emotion=0, block=True),
										transitions={'done': 'close gripper'},
										autonomy={'done': Autonomy.Off},
										remapping={'item': 'item'})

			# x:243 y:387
			OperatableStateMachine.add('say cannot pick',
										SaraSay(sentence="I can not pick the item.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'place arm'},
										autonomy={'done': Autonomy.Off})

			# x:388 y:502
			OperatableStateMachine.add('say thank you',
										SaraSay(sentence="Thank you.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'place arm 2'},
										autonomy={'done': Autonomy.Off})

			# x:72 y:465
			OperatableStateMachine.add('say go to the customer',
										SaraSay(sentence="I will serve it to the customer.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Off})

			# x:522 y:505
			OperatableStateMachine.add('close gripper',
										SetGripperState(width=0, effort=1),
										transitions={'object': 'say thank you', 'no_object': 'open gripper'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:357 y:569
			OperatableStateMachine.add('say cant get back to customer',
										SaraSay(sentence="I am not able to go back to the customer.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'check if end of the list'},
										autonomy={'done': Autonomy.Off})

			# x:541 y:317
			OperatableStateMachine.add('open gripper',
										SetGripperState(width=0.10, effort=1),
										transitions={'object': 'say put in the gripper', 'no_object': 'say put in the gripper'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:63 y:110
			OperatableStateMachine.add('one element by one element from the list',
										FlexibleCalculationState(calculation=lambda x: x[0][x[1]].data, input_keys=["orderList", "indexKey"]),
										transitions={'done': 'say search and grip'},
										autonomy={'done': Autonomy.Off},
										remapping={'orderList': 'orderList', 'indexKey': 'indexKey', 'output_value': 'item'})

			# x:376 y:324
			OperatableStateMachine.add('place arm',
										RunTrajectory(file="receive_object", duration=0),
										transitions={'done': 'open gripper'},
										autonomy={'done': Autonomy.Off})

			# x:638 y:184
			OperatableStateMachine.add('Action_Move_2',
										self.use_behavior(Action_MoveSM, 'take objects and bring the order to customer/Action_Move_2'),
										transitions={'finished': 'increment indexKey', 'failed': 'say cannot go back to bar'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'barPosition'})

			# x:817 y:178
			OperatableStateMachine.add('say cannot go back to bar',
										SaraSay(sentence="I am not able to go back to the barman. I will try a new command.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:85 y:740
			OperatableStateMachine.add('find table and place',
										_sm_find_table_and_place_0,
										transitions={'finished': 'retour repos', 'failed': 'retour repos', 'no_table': 'retour repos'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'no_table': Autonomy.Inherit})

			# x:248 y:505
			OperatableStateMachine.add('place arm 2',
										RunTrajectory(file="transport", duration=0),
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Off})

			# x:362 y:679
			OperatableStateMachine.add('retour repos',
										RunTrajectory(file="repos", duration=0),
										transitions={'done': 'check if end of the list'},
										autonomy={'done': Autonomy.Off})


		# x:242 y:352, x:1086 y:243
		_sm_get_the_order_12 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['orderList'])

		with _sm_get_the_order_12:
			# x:68 y:39
			OperatableStateMachine.add('length 1',
										CheckConditionState(predicate=lambda x: len(x) == 1),
										transitions={'true': 'say order', 'false': 'length 2'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'orderList'})

			# x:236 y:41
			OperatableStateMachine.add('length 2',
										CheckConditionState(predicate=lambda x: len(x) ==2),
										transitions={'true': 'say order_2', 'false': 'say order_3'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'orderList'})

			# x:228 y:111
			OperatableStateMachine.add('say order_2',
										SaraSay(sentence=lambda x: "For this order, I would like to have one "+x[0][0].data+" and one "+x[0][1].data+", please.", input_keys=["orderList"], emotion=0, block=True),
										transitions={'done': 'wait 5'},
										autonomy={'done': Autonomy.Off},
										remapping={'orderList': 'orderList'})

			# x:374 y:109
			OperatableStateMachine.add('say order_3',
										SaraSay(sentence=lambda x: "For this order, I would like to have one "+x[0][0].data+", one "+x[0][1].data+" and one "+x[0][2].data+", please.", input_keys=["orderList"], emotion=0, block=True),
										transitions={'done': 'wait 5'},
										autonomy={'done': Autonomy.Off},
										remapping={'orderList': 'orderList'})

			# x:67 y:117
			OperatableStateMachine.add('say order',
										SaraSay(sentence=lambda x: "For this order, I would like to have one "+x[0][0].data+", please.", input_keys=["orderList"], emotion=0, block=True),
										transitions={'done': 'wait 5'},
										autonomy={'done': Autonomy.Off},
										remapping={'orderList': 'orderList'})

			# x:224 y:256
			OperatableStateMachine.add('wait 5',
										WaitState(wait_time=5),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		# x:216 y:528, x:572 y:238
		_sm_go_to_the_barman_13 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['barPosition', 'barmanID'])

		with _sm_go_to_the_barman_13:
			# x:30 y:102
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(Action_MoveSM, 'go to the barman/Action_Move'),
										transitions={'finished': 'if barman id is 0', 'failed': 'say cannot'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'barPosition'})

			# x:365 y:99
			OperatableStateMachine.add('say cannot',
										SaraSay(sentence="I can not reach my destination. I will take another order. If you have one, please raise your hand.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:30 y:320
			OperatableStateMachine.add('Action_findPersonByID',
										self.use_behavior(Action_findPersonByIDSM, 'go to the barman/Action_findPersonByID', default_keys=['className']),
										transitions={'found': 'finished', 'not_found': 'finished'},
										autonomy={'found': Autonomy.Inherit, 'not_found': Autonomy.Inherit},
										remapping={'className': 'className', 'personID': 'barmanID', 'personEntity': 'personEntity'})

			# x:115 y:230
			OperatableStateMachine.add('if barman id is 0',
										CheckConditionState(predicate=lambda x: x == 0),
										transitions={'true': 'finished', 'false': 'Action_findPersonByID'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'barmanID'})


		# x:898 y:561, x:871 y:123
		_sm_ask_and_save_order_14 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['customerID'], output_keys=['orderList'])

		with _sm_ask_and_save_order_14:
			# x:70 y:112
			OperatableStateMachine.add('say ready',
										SaraSay(sentence="Hello.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'set question'},
										autonomy={'done': Autonomy.Off})

			# x:69 y:187
			OperatableStateMachine.add('set question',
										SetKey(Value="What do you want to order?"),
										transitions={'done': 'ask AND look person'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'question'})

			# x:411 y:138
			OperatableStateMachine.add('say cannot',
										SaraSay(sentence="I am not able to understand your order. I will take another order. If you have one, please raise your hand.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:59 y:272
			OperatableStateMachine.add('ask AND look person',
										_sm_ask_and_look_person_4,
										transitions={'finished': 'nlu restaurant', 'failed': 'say cannot'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'personID': 'customerID', 'question': 'question', 'answer': 'answer'})

			# x:411 y:453
			OperatableStateMachine.add('nlu restaurant',
										SaraNLUrestaurant(),
										transitions={'understood': 'confirm order', 'fail': 'say cannot'},
										autonomy={'understood': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'sentence': 'answer', 'orderList': 'orderList'})

			# x:657 y:417
			OperatableStateMachine.add('confirm order',
										_sm_confirm_order_3,
										transitions={'finished': 'finished', 'failed': 'set question'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'orderList': 'orderList'})


		# x:677 y:318, x:735 y:160
		_sm_move_to_table_and_save_position_15 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['customerPosition'], output_keys=['robotPositionToCustomer'])

		with _sm_move_to_table_and_save_position_15:
			# x:69 y:24
			OperatableStateMachine.add('set distance to person',
										SetKey(Value=0.7),
										transitions={'done': 'compute robot pose to customer'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'distanceToPerson'})

			# x:344 y:115
			OperatableStateMachine.add('say cannot',
										SaraSay(sentence="I can not reach my destination. I will take another order. If you have one, please raise your hand.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'save pose to not get flexbe problems'},
										autonomy={'done': Autonomy.Off})

			# x:497 y:129
			OperatableStateMachine.add('save pose to not get flexbe problems',
										Get_Robot_Pose(),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose': 'pose'})

			# x:47 y:98
			OperatableStateMachine.add('compute robot pose to customer',
										Get_Reacheable_Waypoint(),
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose_in': 'customerPosition', 'distance': 'distanceToPerson', 'pose_out': 'robotPositionToCustomer'})

			# x:78 y:199
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(Action_MoveSM, 'move to table and save position/Action_Move'),
										transitions={'finished': 'finished', 'failed': 'say cannot'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'robotPositionToCustomer'})


		# x:112 y:525, x:363 y:46
		_sm_detect_people_waving_16 = OperatableStateMachine(outcomes=['finished', 'failed'], output_keys=['customerPosition', 'customerID'])

		with _sm_detect_people_waving_16:
			# x:84 y:25
			OperatableStateMachine.add('say looking',
										SaraSay(sentence="I am now looking for customers.", input_keys=[], emotion=0, block=False),
										transitions={'done': 'Look for waving people'},
										autonomy={'done': Autonomy.Off})

			# x:73 y:375
			OperatableStateMachine.add('reachable position_2',
										Get_Reacheable_Waypoint(),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose_in': 'customerPosition', 'distance': 'distance', 'pose_out': 'customerPosition'})

			# x:71 y:291
			OperatableStateMachine.add('set distance to customer_2',
										SetKey(Value=1),
										transitions={'done': 'reachable position_2'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'distance'})

			# x:94 y:216
			OperatableStateMachine.add('get attributes',
										GetAttribute(attributes=["ID", "position"]),
										transitions={'done': 'set distance to customer_2'},
										autonomy={'done': Autonomy.Off},
										remapping={'object': 'waving_person', 'ID': 'customerID', 'position': 'customerPosition'})

			# x:63 y:120
			OperatableStateMachine.add('Look for waving people',
										_sm_look_for_waving_people_9,
										transitions={'finished': 'get attributes', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'waving_person': 'waving_person'})


		# x:874 y:499, x:747 y:100
		_sm_save_bar_position_and_initiation_17 = OperatableStateMachine(outcomes=['finished', 'failed'], output_keys=['barPosition', 'commandNumber', 'barmanID'])

		with _sm_save_bar_position_and_initiation_17:
			# x:66 y:96
			OperatableStateMachine.add('set question barman',
										SetKey(Value="Are you the bartender?"),
										transitions={'done': 'Action_FindPersonByQuestion'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'questionBarman'})

			# x:488 y:85
			OperatableStateMachine.add('say failed to find the barman',
										SaraSay(sentence="I am not able to find the barman. I will get the order and come back here to get the items.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'barman ID to 0'},
										autonomy={'done': Autonomy.Off})

			# x:83 y:406
			OperatableStateMachine.add('save barman ID',
										CalculationState(calculation=lambda x: x.ID),
										transitions={'done': 'get current pose'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'personFound', 'output_value': 'barmanID'})

			# x:512 y:183
			OperatableStateMachine.add('barman ID to 0',
										SetKey(Value=0),
										transitions={'done': 'get current pose'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'barmanID'})

			# x:488 y:391
			OperatableStateMachine.add('get current pose',
										Get_Robot_Pose(),
										transitions={'done': 'set first command'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose': 'barPosition'})

			# x:55 y:214
			OperatableStateMachine.add('Action_FindPersonByQuestion',
										self.use_behavior(Action_FindPersonByQuestionSM, 'save bar position and initiation/Action_FindPersonByQuestion'),
										transitions={'found': 'save barman ID', 'failed': 'say failed to find the barman', 'not_found': 'say failed to find the barman'},
										autonomy={'found': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'not_found': Autonomy.Inherit},
										remapping={'question': 'questionBarman', 'entityFound': 'personFound'})

			# x:489 y:478
			OperatableStateMachine.add('set first command',
										SetKey(Value=1),
										transitions={'done': 'say instructions'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'commandNumber'})

			# x:689 y:477
			OperatableStateMachine.add('say instructions',
										SaraSay(sentence="Please, Barman, do not use any basket. Put the objects directly on the table in front of you when I will come back with an order. I will take them one by one to the customer. Thank you!", input_keys=[], emotion=0, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})



		with _state_machine:
			# x:30 y:40
			OperatableStateMachine.add('save bar position and initiation',
										_sm_save_bar_position_and_initiation_17,
										transitions={'finished': 'detect people waving', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'barPosition': 'barPosition', 'commandNumber': 'commandNumber', 'barmanID': 'barmanID'})

			# x:131 y:141
			OperatableStateMachine.add('detect people waving',
										_sm_detect_people_waving_16,
										transitions={'finished': 'move to table and save position', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'customerPosition': 'customerPosition', 'customerID': 'customerID'})

			# x:233 y:250
			OperatableStateMachine.add('move to table and save position',
										_sm_move_to_table_and_save_position_15,
										transitions={'finished': 'ask and save order', 'failed': 'detect people waving'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'customerPosition': 'customerPosition', 'robotPositionToCustomer': 'robotPositionToCustomer'})

			# x:286 y:337
			OperatableStateMachine.add('ask and save order',
										_sm_ask_and_save_order_14,
										transitions={'finished': 'go to the barman', 'failed': 'detect people waving'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'customerID': 'customerID', 'orderList': 'orderList'})

			# x:264 y:434
			OperatableStateMachine.add('go to the barman',
										_sm_go_to_the_barman_13,
										transitions={'finished': 'get the order', 'failed': 'detect people waving'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'barPosition': 'barPosition', 'barmanID': 'barmanID'})

			# x:278 y:526
			OperatableStateMachine.add('get the order',
										_sm_get_the_order_12,
										transitions={'finished': 'take objects and bring the order to customer', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'orderList': 'orderList'})

			# x:260 y:626
			OperatableStateMachine.add('take objects and bring the order to customer',
										_sm_take_objects_and_bring_the_order_to_customer_11,
										transitions={'finished': 'repeate if first commande', 'failed': 'repeate if first commande'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'barPosition': 'barPosition', 'orderList': 'orderList', 'robotPositionToCustomer': 'robotPositionToCustomer'})

			# x:118 y:735
			OperatableStateMachine.add('repeate if first commande',
										_sm_repeate_if_first_commande_10,
										transitions={'finished': 'say finish', 'repeate': 'detect people waving'},
										autonomy={'finished': Autonomy.Inherit, 'repeate': Autonomy.Inherit},
										remapping={'commandNumber': 'commandNumber'})

			# x:431 y:743
			OperatableStateMachine.add('say finish',
										SaraSay(sentence="I reach the end of my scenario. I will go back to the bar.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Off})

			# x:616 y:735
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(Action_MoveSM, 'Action_Move'),
										transitions={'finished': 'finished', 'failed': 'finished'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'barPosition'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
