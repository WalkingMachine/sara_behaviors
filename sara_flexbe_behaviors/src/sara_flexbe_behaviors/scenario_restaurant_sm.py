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
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_behaviors.action_move_sm import Action_MoveSM as sara_flexbe_behaviors__Action_MoveSM
from sara_flexbe_behaviors.action_ask_sm import Action_AskSM as sara_flexbe_behaviors__Action_AskSM
from flexbe_states.check_condition_state import CheckConditionState
from flexbe_states.wait_state import WaitState
from flexbe_states.flexible_calculation_state import FlexibleCalculationState
from flexbe_states.calculation_state import CalculationState
from flexbe_states.flexible_check_condition_state import FlexibleCheckConditionState
from sara_flexbe_behaviors.action_find_sm import Action_findSM as sara_flexbe_behaviors__Action_findSM
from sara_flexbe_behaviors.action_pick_sm import Action_pickSM as sara_flexbe_behaviors__Action_pickSM
from sara_flexbe_states.set_gripper_state import SetGripperState
from sara_flexbe_behaviors.action_place_sm import Action_placeSM as sara_flexbe_behaviors__Action_placeSM
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
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'move to table and save position/Action_Move')
		self.add_behavior(sara_flexbe_behaviors__Action_AskSM, 'ask and save order/Action_Ask')
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'go to the bar/Action_Move')
		self.add_behavior(sara_flexbe_behaviors__Action_findSM, 'bring the order to person/Action_find')
		self.add_behavior(sara_flexbe_behaviors__Action_pickSM, 'bring the order to person/Action_pick')
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'bring the order to person/Action_Move')
		self.add_behavior(sara_flexbe_behaviors__Action_placeSM, 'bring the order to person/Action_place')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:

		# O 176 261 /move to table and save position
		# avoir une meilleure position pour la table?

		# ! 65 53 /ask and save order
		# REGARDER LA PERSONNE QUI LEVE LA MAIN/WAVE|n

		# O 85 406 /ask and save order
		# restaurant NLU



	def create(self):
		# x:902 y:757, x:882 y:161
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:441 y:583, x:93 y:568
		_sm_repeate_if_first_commande_0 = OperatableStateMachine(outcomes=['finished', 'repeate'], input_keys=['commandNumber'], output_keys=['commandNumber'])

		with _sm_repeate_if_first_commande_0:
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


		# x:913 y:749, x:908 y:161
		_sm_bring_the_order_to_person_1 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['barPosition', 'customerPosition', 'orderList'])

		with _sm_bring_the_order_to_person_1:
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
										transitions={'true': 'finished', 'false': 'increment indexKey'},
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
										transitions={'done': 'say put in the gripper'},
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
										transitions={'finished': 'Action_place', 'failed': 'say cant get back to customer'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'customerPosition'})

			# x:83 y:326
			OperatableStateMachine.add('get entity ID',
										CalculationState(calculation=lambda x: x.ID),
										transitions={'done': 'Action_pick'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'entity', 'output_value': 'entityID'})

			# x:379 y:373
			OperatableStateMachine.add('say put in the gripper',
										SaraSay(sentence="Please, put the "+x[0]+" in my gripper.", input_keys=["item"], emotion=0, block=True),
										transitions={'done': 'open gripper'},
										autonomy={'done': Autonomy.Off},
										remapping={'item': 'item'})

			# x:243 y:387
			OperatableStateMachine.add('say cannot pick',
										SaraSay(sentence="I can not pick the item.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'say put in the gripper'},
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

			# x:525 y:380
			OperatableStateMachine.add('open gripper',
										SetGripperState(width=0.14, effort=1),
										transitions={'object': 'wait object 10', 'no_object': 'wait object 10'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:56 y:638
			OperatableStateMachine.add('Action_place',
										self.use_behavior(sara_flexbe_behaviors__Action_placeSM, 'bring the order to person/Action_place'),
										transitions={'finished': 'check if end of the list', 'failed': 'check if end of the list'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pos': 'customerPosition'})

			# x:63 y:110
			OperatableStateMachine.add('one element by one element from the list',
										FlexibleCalculationState(calculation=lambda x: x[0][x[1]], input_keys=["orderList", "indexKey"]),
										transitions={'done': 'say search and grip'},
										autonomy={'done': Autonomy.Off},
										remapping={'orderList': 'orderList', 'indexKey': 'indexKey', 'output_value': 'item'})


		# x:218 y:650, x:1086 y:243
		_sm_get_the_order_2 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['orderList'])

		with _sm_get_the_order_2:
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


		# x:30 y:458, x:462 y:314
		_sm_go_to_the_bar_3 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['barPosition'])

		with _sm_go_to_the_bar_3:
			# x:30 y:102
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'go to the bar/Action_Move'),
										transitions={'finished': 'finished', 'failed': 'say cannot'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'barPosition'})

			# x:365 y:99
			OperatableStateMachine.add('say cannot',
										SaraSay(sentence="I can not reach my destination. I will take another order. If you have one, please raise your hand.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})


		# x:898 y:561, x:871 y:123
		_sm_ask_and_save_order_4 = OperatableStateMachine(outcomes=['finished', 'failed'], output_keys=['orderList'])

		with _sm_ask_and_save_order_4:
			# x:70 y:112
			OperatableStateMachine.add('say ready',
										SaraSay(sentence="I am ready to get your order.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'set question'},
										autonomy={'done': Autonomy.Off})

			# x:69 y:187
			OperatableStateMachine.add('set question',
										SetKey(Value="What do you want to order?"),
										transitions={'done': 'Action_Ask'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'question'})

			# x:53 y:263
			OperatableStateMachine.add('Action_Ask',
										self.use_behavior(sara_flexbe_behaviors__Action_AskSM, 'ask and save order/Action_Ask'),
										transitions={'finished': 'finished', 'failed': 'say cannot'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'question': 'question', 'answer': 'answer'})

			# x:411 y:138
			OperatableStateMachine.add('say cannot',
										SaraSay(sentence="I am not able to understand your order. I will take another order. If you have one, please raise your hand.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})


		# x:704 y:488, x:735 y:160
		_sm_move_to_table_and_save_position_5 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['customerPosition'], output_keys=['tablePosition'])

		with _sm_move_to_table_and_save_position_5:
			# x:80 y:74
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'move to table and save position/Action_Move'),
										transitions={'finished': 'get table pose', 'failed': 'say cannot'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'customerPosition'})

			# x:118 y:438
			OperatableStateMachine.add('get table pose',
										Get_Robot_Pose(),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose': 'tablePosition'})

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


		# x:851 y:631, x:851 y:167
		_sm_detect_people_waving_6 = OperatableStateMachine(outcomes=['finished', 'failed'], output_keys=['customerPosition'])

		with _sm_detect_people_waving_6:
			# x:50 y:32
			OperatableStateMachine.add('say to wave',
										SaraSay(sentence="Hello everyone. If you want to place an order, please raise your hand.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		# x:670 y:531, x:677 y:133
		_sm_save_bar_position_and_initiation_7 = OperatableStateMachine(outcomes=['finished', 'failed'], output_keys=['barPosition', 'commandNumber'])

		with _sm_save_bar_position_and_initiation_7:
			# x:30 y:40
			OperatableStateMachine.add('get current pose',
										Get_Robot_Pose(),
										transitions={'done': 'set first command'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose': 'barPosition'})

			# x:30 y:117
			OperatableStateMachine.add('set first command',
										SetKey(Value=1),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'commandNumber'})



		with _state_machine:
			# x:30 y:40
			OperatableStateMachine.add('save bar position and initiation',
										_sm_save_bar_position_and_initiation_7,
										transitions={'finished': 'detect people waving', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'barPosition': 'barPosition', 'commandNumber': 'commandNumber'})

			# x:131 y:141
			OperatableStateMachine.add('detect people waving',
										_sm_detect_people_waving_6,
										transitions={'finished': 'move to table and save position', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'customerPosition': 'customerPosition'})

			# x:233 y:250
			OperatableStateMachine.add('move to table and save position',
										_sm_move_to_table_and_save_position_5,
										transitions={'finished': 'ask and save order', 'failed': 'detect people waving'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'customerPosition': 'customerPosition', 'tablePosition': 'tablePosition'})

			# x:273 y:338
			OperatableStateMachine.add('ask and save order',
										_sm_ask_and_save_order_4,
										transitions={'finished': 'go to the bar', 'failed': 'detect people waving'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'orderList': 'orderList'})

			# x:264 y:434
			OperatableStateMachine.add('go to the bar',
										_sm_go_to_the_bar_3,
										transitions={'finished': 'get the order', 'failed': 'detect people waving'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'barPosition': 'barPosition'})

			# x:278 y:526
			OperatableStateMachine.add('get the order',
										_sm_get_the_order_2,
										transitions={'finished': 'bring the order to person', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'orderList': 'orderList'})

			# x:260 y:626
			OperatableStateMachine.add('bring the order to person',
										_sm_bring_the_order_to_person_1,
										transitions={'finished': 'repeate if first commande', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'barPosition': 'barPosition', 'customerPosition': 'tablePosition', 'orderList': 'orderList'})

			# x:118 y:735
			OperatableStateMachine.add('repeate if first commande',
										_sm_repeate_if_first_commande_0,
										transitions={'finished': 'finished', 'repeate': 'detect people waving'},
										autonomy={'finished': Autonomy.Inherit, 'repeate': Autonomy.Inherit},
										remapping={'commandNumber': 'commandNumber'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
