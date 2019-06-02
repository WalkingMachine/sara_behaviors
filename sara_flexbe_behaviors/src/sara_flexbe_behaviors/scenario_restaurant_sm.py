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
from sara_flexbe_behaviors.action_findpersonbyquestion_sm import Action_FindPersonByQuestionSM as sara_flexbe_behaviors__Action_FindPersonByQuestionSM
from sara_flexbe_states.get_reachable_waypoint import Get_Reacheable_Waypoint
from sara_flexbe_behaviors.action_move_sm import Action_MoveSM as sara_flexbe_behaviors__Action_MoveSM
from sara_flexbe_behaviors.action_ask_sm import Action_AskSM as sara_flexbe_behaviors__Action_AskSM
from sara_flexbe_states.KeepLookingAt import KeepLookingAt
from sara_flexbe_behaviors.action_findpersonbyid_sm import Action_findPersonByIDSM as sara_flexbe_behaviors__Action_findPersonByIDSM
from flexbe_states.check_condition_state import CheckConditionState
from flexbe_states.wait_state import WaitState
from flexbe_states.flexible_check_condition_state import FlexibleCheckConditionState
from sara_flexbe_behaviors.action_find_sm import Action_findSM as sara_flexbe_behaviors__Action_findSM
from sara_flexbe_behaviors.action_pick_sm import Action_pickSM as sara_flexbe_behaviors__Action_pickSM
from sara_flexbe_states.set_gripper_state import SetGripperState
from sara_flexbe_behaviors.action_place_sm import Action_placeSM as sara_flexbe_behaviors__Action_placeSM
from flexbe_states.flexible_calculation_state import FlexibleCalculationState
from sara_flexbe_states.run_trajectory import RunTrajectory
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
		self.add_behavior(sara_flexbe_behaviors__Action_FindPersonByQuestionSM, 'save bar position and initiation/Action_FindPersonByQuestion')
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'move to table and save position/Action_Move')
		self.add_behavior(sara_flexbe_behaviors__Action_AskSM, 'ask and save order/ask AND look person/ask/Action_Ask')
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'go to the barman/Action_Move')
		self.add_behavior(sara_flexbe_behaviors__Action_findPersonByIDSM, 'go to the barman/Action_findPersonByID')
		self.add_behavior(sara_flexbe_behaviors__Action_findSM, 'bring the order to person/Action_find')
		self.add_behavior(sara_flexbe_behaviors__Action_pickSM, 'bring the order to person/Action_pick')
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'bring the order to person/Action_Move')
		self.add_behavior(sara_flexbe_behaviors__Action_placeSM, 'bring the order to person/Action_place')
		self.add_behavior(sara_flexbe_behaviors__Action_findSM, 'bring the order to person/Action_find_2')
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'bring the order to person/Action_Move_2')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:

		# O 176 261 /move to table and save position
		# avoir une meilleure position pour la table?

		# O 85 406 /ask and save order
		# restaurant NLU



	def create(self):
		# x:902 y:757, x:882 y:161
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:30 y:458, x:130 y:458
		_sm_keep_looking_0 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['personID'])

		with _sm_keep_looking_0:
			# x:30 y:40
			OperatableStateMachine.add('keep',
										KeepLookingAt(),
										transitions={'failed': 'keep'},
										autonomy={'failed': Autonomy.Off},
										remapping={'ID': 'personID'})


		# x:30 y:458, x:130 y:458
		_sm_ask_1 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['question'], output_keys=['answer'])

		with _sm_ask_1:
			# x:30 y:40
			OperatableStateMachine.add('Action_Ask',
										self.use_behavior(sara_flexbe_behaviors__Action_AskSM, 'ask and save order/ask AND look person/ask/Action_Ask'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'question': 'question', 'answer': 'answer'})


		# x:348 y:66, x:351 y:97, x:339 y:159, x:336 y:195, x:518 y:89, x:515 y:175
		_sm_ask_and_look_person_2 = ConcurrencyContainer(outcomes=['finished', 'failed'], input_keys=['personID', 'question'], output_keys=['answer'], conditions=[
										('finished', [('ask', 'finished')]),
										('failed', [('ask', 'failed')]),
										('finished', [('keep looking', 'finished')]),
										('failed', [('keep looking', 'failed')])
										])

		with _sm_ask_and_look_person_2:
			# x:30 y:40
			OperatableStateMachine.add('ask',
										_sm_ask_1,
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'question': 'question', 'answer': 'answer'})

			# x:30 y:138
			OperatableStateMachine.add('keep looking',
										_sm_keep_looking_0,
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'personID': 'personID'})


		# x:441 y:583, x:93 y:568
		_sm_repeate_if_first_commande_3 = OperatableStateMachine(outcomes=['finished', 'repeate'], input_keys=['commandNumber'], output_keys=['commandNumber'])

		with _sm_repeate_if_first_commande_3:
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
		_sm_bring_the_order_to_person_4 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['barPosition', 'orderList', 'robotPositionToCustomer'])

		with _sm_bring_the_order_to_person_4:
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
										self.use_behavior(sara_flexbe_behaviors__Action_findSM, 'bring the order to person/Action_find'),
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
										self.use_behavior(sara_flexbe_behaviors__Action_pickSM, 'bring the order to person/Action_pick'),
										transitions={'success': 'say go to the customer', 'unreachable': 'say cannot pick', 'not found': 'say cannot pick', 'dropped': 'say cannot pick'},
										autonomy={'success': Autonomy.Inherit, 'unreachable': Autonomy.Inherit, 'not found': Autonomy.Inherit, 'dropped': Autonomy.Inherit},
										remapping={'objectID': 'entityID', 'Entity': 'entity'})

			# x:61 y:548
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'bring the order to person/Action_Move'),
										transitions={'finished': 'set tableKey', 'failed': 'say cant get back to customer'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'robotPositionToCustomer'})

			# x:83 y:326
			OperatableStateMachine.add('get entity ID',
										CalculationState(calculation=lambda x: x.ID),
										transitions={'done': 'Action_pick'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'entity', 'output_value': 'entityID'})

			# x:508 y:321
			OperatableStateMachine.add('say put in the gripper',
										SaraSay(sentence="Please, put the "+x[0]+" in my gripper.", input_keys=["item"], emotion=0, block=True),
										transitions={'done': 'open gripper'},
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
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Off})

			# x:72 y:465
			OperatableStateMachine.add('say go to the customer',
										SaraSay(sentence="I will serve it to the customer", input_keys=[], emotion=0, block=True),
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Off})

			# x:522 y:505
			OperatableStateMachine.add('close gripper',
										SetGripperState(width=0, effort=1),
										transitions={'object': 'say thank you', 'no_object': 'say thank you'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:536 y:444
			OperatableStateMachine.add('wait object 10',
										WaitState(wait_time=10),
										transitions={'done': 'close gripper'},
										autonomy={'done': Autonomy.Off})

			# x:357 y:569
			OperatableStateMachine.add('say cant get back to customer',
										SaraSay(sentence="I am not able to go back to the customer.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'check if end of the list'},
										autonomy={'done': Autonomy.Off})

			# x:526 y:382
			OperatableStateMachine.add('open gripper',
										SetGripperState(width=0.10, effort=1),
										transitions={'object': 'wait object 10', 'no_object': 'wait object 10'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:58 y:824
			OperatableStateMachine.add('Action_place',
										self.use_behavior(sara_flexbe_behaviors__Action_placeSM, 'bring the order to person/Action_place'),
										transitions={'finished': 'check if end of the list', 'failed': 'check if end of the list'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pos': 'tablePosition'})

			# x:63 y:110
			OperatableStateMachine.add('one element by one element from the list',
										FlexibleCalculationState(calculation=lambda x: x[0][x[1]], input_keys=["orderList", "indexKey"]),
										transitions={'done': 'say search and grip'},
										autonomy={'done': Autonomy.Off},
										remapping={'orderList': 'orderList', 'indexKey': 'indexKey', 'output_value': 'item'})

			# x:376 y:324
			OperatableStateMachine.add('place arm',
										RunTrajectory(file="receive_object", duration=0),
										transitions={'done': 'say put in the gripper'},
										autonomy={'done': Autonomy.Off})

			# x:58 y:680
			OperatableStateMachine.add('Action_find_2',
										self.use_behavior(sara_flexbe_behaviors__Action_findSM, 'bring the order to person/Action_find_2'),
										transitions={'done': 'get table position', 'failed': 'say do not find table'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'className': 'tableKey', 'entity': 'tableEntity'})

			# x:76 y:617
			OperatableStateMachine.add('set tableKey',
										SetKey(Value="table"),
										transitions={'done': 'Action_find_2'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'tableKey'})

			# x:80 y:763
			OperatableStateMachine.add('get table position',
										CalculationState(calculation=lambda x: x.position),
										transitions={'done': 'Action_place'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'tableEntity', 'output_value': 'tablePosition'})

			# x:272 y:671
			OperatableStateMachine.add('say do not find table',
										SaraSay(sentence="I can not find the table.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'check if end of the list'},
										autonomy={'done': Autonomy.Off})

			# x:638 y:184
			OperatableStateMachine.add('Action_Move_2',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'bring the order to person/Action_Move_2'),
										transitions={'finished': 'increment indexKey', 'failed': 'say cannot go back to bar'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'barPosition'})

			# x:817 y:178
			OperatableStateMachine.add('say cannot go back to bar',
										SaraSay(sentence="I am not able to go back to the barman. I will try a new command.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})


		# x:218 y:650, x:1086 y:243
		_sm_get_the_order_5 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['orderList'])

		with _sm_get_the_order_5:
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
										SaraSay(sentence=lambda x: "For this order, I would like to have one "+x[0][0]+" and one "+x[0][1]+", please.", input_keys=["orderList"], emotion=0, block=True),
										transitions={'done': 'wait 5'},
										autonomy={'done': Autonomy.Off},
										remapping={'orderList': 'orderList'})

			# x:374 y:109
			OperatableStateMachine.add('say order_3',
										SaraSay(sentence=lambda x: "For this order, I would like to have one "+x[0][0]+", one "+x[0][1]+" and one "+x[0][2]+", please.", input_keys=["orderList"], emotion=0, block=True),
										transitions={'done': 'wait 5'},
										autonomy={'done': Autonomy.Off},
										remapping={'orderList': 'orderList'})

			# x:67 y:117
			OperatableStateMachine.add('say order',
										SaraSay(sentence=lambda x: "For this order, I would like to have one "+x[0][0]+", please.", input_keys=["orderList"], emotion=0, block=True),
										transitions={'done': 'wait 5'},
										autonomy={'done': Autonomy.Off},
										remapping={'orderList': 'orderList'})

			# x:199 y:457
			OperatableStateMachine.add('wait 5',
										WaitState(wait_time=5),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		# x:86 y:559, x:572 y:238
		_sm_go_to_the_barman_6 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['barPosition', 'barmanID'])

		with _sm_go_to_the_barman_6:
			# x:30 y:102
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'go to the barman/Action_Move'),
										transitions={'finished': 'Action_findPersonByID', 'failed': 'say cannot'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'barPosition'})

			# x:365 y:99
			OperatableStateMachine.add('say cannot',
										SaraSay(sentence="I can not reach my destination. I will take another order. If you have one, please raise your hand.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:29 y:225
			OperatableStateMachine.add('Action_findPersonByID',
										self.use_behavior(sara_flexbe_behaviors__Action_findPersonByIDSM, 'go to the barman/Action_findPersonByID', default_keys=['className']),
										transitions={'found': 'finished', 'not_found': 'finished'},
										autonomy={'found': Autonomy.Inherit, 'not_found': Autonomy.Inherit},
										remapping={'className': 'className', 'personID': 'barmanID', 'personEntity': 'personEntity'})


		# x:898 y:561, x:871 y:123
		_sm_ask_and_save_order_7 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['customerID'], output_keys=['orderList'])

		with _sm_ask_and_save_order_7:
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
										_sm_ask_and_look_person_2,
										transitions={'finished': 'le temps de faire un NLU resaurant', 'failed': 'say cannot'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'personID': 'customerID', 'question': 'question', 'answer': 'answer'})

			# x:415 y:508
			OperatableStateMachine.add('le temps de faire un NLU resaurant',
										SetKey(Value=["orange", "pringles"]),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Key'})


		# x:704 y:488, x:735 y:160
		_sm_move_to_table_and_save_position_8 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['customerPosition'], output_keys=['robotPositionToCustomer'])

		with _sm_move_to_table_and_save_position_8:
			# x:69 y:24
			OperatableStateMachine.add('set distance to person',
										SetKey(Value=0.7),
										transitions={'done': 'compute robot pose to customer'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'distanceToPerson'})

			# x:365 y:99
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
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'move to table and save position/Action_Move'),
										transitions={'finished': 'finished', 'failed': 'say cannot'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'robotPositionToCustomer'})


		# x:851 y:631, x:851 y:167
		_sm_detect_people_waving_9 = OperatableStateMachine(outcomes=['finished', 'failed'], output_keys=['customerPosition', 'customerID'])

		with _sm_detect_people_waving_9:
			# x:50 y:32
			OperatableStateMachine.add('say to wave',
										SaraSay(sentence="Hello everyone. If you want to place an order, please raise your hand.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		# x:790 y:769, x:747 y:100
		_sm_save_bar_position_and_initiation_10 = OperatableStateMachine(outcomes=['finished', 'failed'], output_keys=['barPosition', 'commandNumber', 'barmanID'])

		with _sm_save_bar_position_and_initiation_10:
			# x:66 y:96
			OperatableStateMachine.add('set question barman',
										SetKey(Value="Are you the barman?"),
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
										CalculationState(calculation=x.ID),
										transitions={'done': 'get current pose'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'personFound', 'output_value': 'barmanID'})

			# x:512 y:183
			OperatableStateMachine.add('barman ID to 0',
										SetKey(Value=0),
										transitions={'done': 'get current pose'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'barmanID'})

			# x:509 y:674
			OperatableStateMachine.add('get current pose',
										Get_Robot_Pose(),
										transitions={'done': 'set first command'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose': 'barPosition'})

			# x:51 y:182
			OperatableStateMachine.add('Action_FindPersonByQuestion',
										self.use_behavior(sara_flexbe_behaviors__Action_FindPersonByQuestionSM, 'save bar position and initiation/Action_FindPersonByQuestion'),
										transitions={'found': 'save barman ID', 'failed': 'say failed to find the barman', 'not_found': 'say failed to find the barman'},
										autonomy={'found': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'not_found': Autonomy.Inherit},
										remapping={'question': 'questionBarman', 'entityFound': 'personFound'})

			# x:505 y:756
			OperatableStateMachine.add('set first command',
										SetKey(Value=1),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'commandNumber'})



		with _state_machine:
			# x:30 y:40
			OperatableStateMachine.add('save bar position and initiation',
										_sm_save_bar_position_and_initiation_10,
										transitions={'finished': 'detect people waving', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'barPosition': 'barPosition', 'commandNumber': 'commandNumber', 'barmanID': 'barmanID'})

			# x:131 y:141
			OperatableStateMachine.add('detect people waving',
										_sm_detect_people_waving_9,
										transitions={'finished': 'move to table and save position', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'customerPosition': 'customerPosition', 'customerID': 'customerID'})

			# x:233 y:250
			OperatableStateMachine.add('move to table and save position',
										_sm_move_to_table_and_save_position_8,
										transitions={'finished': 'ask and save order', 'failed': 'detect people waving'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'customerPosition': 'customerPosition', 'robotPositionToCustomer': 'robotPositionToCustomer'})

			# x:273 y:338
			OperatableStateMachine.add('ask and save order',
										_sm_ask_and_save_order_7,
										transitions={'finished': 'go to the barman', 'failed': 'detect people waving'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'customerID': 'customerID', 'orderList': 'orderList'})

			# x:264 y:434
			OperatableStateMachine.add('go to the barman',
										_sm_go_to_the_barman_6,
										transitions={'finished': 'get the order', 'failed': 'detect people waving'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'barPosition': 'barPosition', 'barmanID': 'barmanID'})

			# x:278 y:526
			OperatableStateMachine.add('get the order',
										_sm_get_the_order_5,
										transitions={'finished': 'bring the order to person', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'orderList': 'orderList'})

			# x:260 y:626
			OperatableStateMachine.add('bring the order to person',
										_sm_bring_the_order_to_person_4,
										transitions={'finished': 'repeate if first commande', 'failed': 'repeate if first commande'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'barPosition': 'barPosition', 'orderList': 'orderList', 'robotPositionToCustomer': 'robotPositionToCustomer'})

			# x:118 y:735
			OperatableStateMachine.add('repeate if first commande',
										_sm_repeate_if_first_commande_3,
										transitions={'finished': 'finished', 'repeate': 'detect people waving'},
										autonomy={'finished': Autonomy.Inherit, 'repeate': Autonomy.Inherit},
										remapping={'commandNumber': 'commandNumber'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
