#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_scenario_mvp_storing_groceries')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.WonderlandGetEntityVerbal import WonderlandGetEntityVerbal
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.get_reachable_waypoint import Get_Reacheable_Waypoint
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_states.list_entities_by_name import list_entities_by_name
from behavior_action_turn.action_turn_sm import action_turnSM
from flexbe_states.check_condition_state import CheckConditionState
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.for_loop import ForLoop
from sara_flexbe_states.pose_gen_euler_key import GenPoseEulerKey
from behavior_action_pick.action_pick_sm import Action_pickSM
from sara_flexbe_states.sara_say_key import SaraSayKey
from sara_flexbe_states.binary_calculation_state import BinaryCalculationState
from behavior_action_place.action_place_sm import Action_placeSM
from sara_flexbe_states.sara_move_base import SaraMoveBase
from flexbe_states.wait_state import WaitState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sun Jun 17 2018
@author: Raphael Duchaine
'''
class scenario_MVP_storing_groceriesSM(Behavior):
	'''
	Will search for each category of objects and put them together
	'''


	def __init__(self):
		super(scenario_MVP_storing_groceriesSM, self).__init__()
		self.name = 'scenario_MVP_storing_groceries'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(action_turnSM, 'Look for Table s objects/searchTable/action_turn')
		self.add_behavior(Action_pickSM, 'Pick and place all objects/Pick and react to errors/Action_pick')
		self.add_behavior(Action_placeSM, 'Pick and place all objects/place near same name or cat /Action_place')
		self.add_behavior(action_turnSM, 'Pick and place all objects/FaceCupboard')
		self.add_behavior(action_turnSM, 'Pick and place all objects/FaceCupboard2')
		self.add_behavior(action_turnSM, 'Pick and place all objects/ForEachEntity/storingGroceries_tryFacingTable/FaceTable')
		self.add_behavior(action_turnSM, 'FaceCupboard')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:

		# O 216 14 
		# Still need the |ntableRelativePos by|nlooking for multiple|n same y objects

		# O 657 119 
		# Add offset |nfor each category|nplaceXpos=i*offset+cbPos|nif side == x



	def create(self):
		lengthCategories = 5
		# x:594 y:649, x:604 y:88
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['nomArmoire'])
		_state_machine.userdata.nomTable = "table"
		_state_machine.userdata.empty = ""
		_state_machine.userdata.categories = ["drinks","snacks","fruits","cleaning stuff","food"]
		_state_machine.userdata.nomArmoire = "cupboard"
		_state_machine.userdata.zero = 0
		_state_machine.userdata.hauteur3rdShelfFromFloor = 64
		_state_machine.userdata.placeZoffset = 0.05
		_state_machine.userdata.cbXpos = 1
		_state_machine.userdata.cbYpos = 1

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:400 y:54, x:521 y:307
		_sm_storinggroceries_tryfacingtable_0 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['rotToTable'])

		with _sm_storinggroceries_tryfacingtable_0:
			# x:120 y:57
			OperatableStateMachine.add('FaceTable',
										self.use_behavior(action_turnSM, 'Pick and place all objects/ForEachEntity/storingGroceries_tryFacingTable/FaceTable'),
										transitions={'finished': 'finished', 'failed': 'Have problem turning'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'rotation': 'rotToTable'})

			# x:68 y:406
			OperatableStateMachine.add('Have problem turning',
										SaraSay(sentence="I just desoriented myself. I'll try to rectify.", emotion=3, block=True),
										transitions={'done': 'faceCupboard'},
										autonomy={'done': Autonomy.Off})

			# x:434 y:161
			OperatableStateMachine.add('faceCupboard',
										SaraMoveBase(),
										transitions={'arrived': 'FaceTable', 'failed': 'Cant rectify'},
										autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'rotToTable'})

			# x:402 y:392
			OperatableStateMachine.add('Cant rectify',
										SaraSay(sentence="I'm sorry, I failed", emotion=3, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})


		# x:30 y:293
		_sm_i_really_wanted_to_get_this_object_1 = OperatableStateMachine(outcomes=['finished'], input_keys=['entity_list', 'j'])

		with _sm_i_really_wanted_to_get_this_object_1:
			# x:96 y:37
			OperatableStateMachine.add('getEntityName',
										BinaryCalculationState(calculation=lambda x: x[0][x[1]].name),
										transitions={'done': 'I really wanted to get this'},
										autonomy={'done': Autonomy.Off},
										remapping={'X': 'entity_list', 'Y': 'j', 'Z': 'name'})

			# x:309 y:42
			OperatableStateMachine.add('I really wanted to get this',
										SaraSayKey(Format="I really wanted to get this {}.", emotion=3, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'name'})


		# x:409 y:296, x:340 y:196, x:801 y:287, x:43 y:204
		_sm_foreachentity_2 = OperatableStateMachine(outcomes=['end', 'not_found', 'done', 'failed'], input_keys=['categories', 'i', 'rotToTable'], output_keys=['entity_list', 'j', 'category', 'entityID', 'name', 'category'])

		with _sm_foreachentity_2:
			# x:24 y:48
			OperatableStateMachine.add('storingGroceries_tryFacingTable',
										_sm_storinggroceries_tryfacingtable_0,
										transitions={'finished': 'getCategory', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'rotToTable': 'rotToTable'})

			# x:445 y:121
			OperatableStateMachine.add('ForEverySimilarItems',
										ForLoop(repeat=5),
										transitions={'do': 'getEntityId', 'end': 'end'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'j'})

			# x:502 y:227
			OperatableStateMachine.add('getEntityId',
										BinaryCalculationState(calculation="X[Y].ID"),
										transitions={'done': 'getEntityName'},
										autonomy={'done': Autonomy.Off},
										remapping={'X': 'entity_list', 'Y': 'j', 'Z': 'entityID'})

			# x:696 y:152
			OperatableStateMachine.add('getEntityName',
										BinaryCalculationState(calculation="X[Y].name"),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off},
										remapping={'X': 'entity_list', 'Y': 'j', 'Z': 'name'})

			# x:155 y:168
			OperatableStateMachine.add('list_entities_by_name',
										list_entities_by_name(frontality_level=0.5, distance_max=10),
										transitions={'found': 'ForEverySimilarItems', 'none_found': 'not_found'},
										autonomy={'found': Autonomy.Off, 'none_found': Autonomy.Off},
										remapping={'name': 'category', 'entity_list': 'entity_list', 'number': 'nbrEntities'})

			# x:326 y:47
			OperatableStateMachine.add('getCategory',
										BinaryCalculationState(calculation=lambda x: x[0][x[1]]),
										transitions={'done': 'list_entities_by_name'},
										autonomy={'done': Autonomy.Off},
										remapping={'X': 'categories', 'Y': 'i', 'Z': 'category'})


		# x:30 y:293, x:130 y:293
		_sm_place_near_same_name_or_cat__3 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['shelfPos', 'name', 'zero', 'placeZoffset', 'category'])

		with _sm_place_near_same_name_or_cat__3:
			# x:224 y:112
			OperatableStateMachine.add('list_entities_by_name',
										list_entities_by_name(frontality_level=0.5, distance_max=4),
										transitions={'found': 'getPos', 'none_found': 'list_entities_by_category'},
										autonomy={'found': Autonomy.Off, 'none_found': Autonomy.Off},
										remapping={'name': 'name', 'entity_list': 'cp_entity_list', 'number': 'cp_entity_number'})

			# x:440 y:93
			OperatableStateMachine.add('getPos',
										CalculationState(calculation=lambda x: x[0].position),
										transitions={'done': 'addZOffset'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'cp_entity_list', 'output_value': 'posSimilar'})

			# x:371 y:279
			OperatableStateMachine.add('list_entities_by_category',
										list_entities_by_name(frontality_level=0.5, distance_max=10),
										transitions={'found': 'getPos', 'none_found': 'Action_place'},
										autonomy={'found': Autonomy.Off, 'none_found': Autonomy.Off},
										remapping={'name': 'category', 'entity_list': 'cp_entity_list', 'number': 'cp_entity_number'})

			# x:482 y:422
			OperatableStateMachine.add('Action_place',
										self.use_behavior(Action_placeSM, 'Pick and place all objects/place near same name or cat /Action_place'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pos': 'shelfPos'})

			# x:741 y:309
			OperatableStateMachine.add('Addoffset',
										GenPoseEulerKey(),
										transitions={'done': 'Action_place'},
										autonomy={'done': Autonomy.Off},
										remapping={'xpos': 'xpos', 'ypos': 'ypos', 'zpos': 'zpos', 'yaw': 'zero', 'pitch': 'zero', 'roll': 'zero', 'pose': 'pose'})

			# x:629 y:33
			OperatableStateMachine.add('addZOffset',
										BinaryCalculationState(calculation="X.z-Y"),
										transitions={'done': 'get_ypos'},
										autonomy={'done': Autonomy.Off},
										remapping={'X': 'posSimilar', 'Y': 'placeZoffset', 'Z': 'zpos'})

			# x:588 y:156
			OperatableStateMachine.add('get_ypos',
										CalculationState(calculation=lambda x: x.y),
										transitions={'done': 'get_xpos'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'posSimilar', 'output_value': 'ypos'})

			# x:659 y:233
			OperatableStateMachine.add('get_xpos',
										CalculationState(calculation=lambda x: x.x),
										transitions={'done': 'Addoffset'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'posSimilar', 'output_value': 'xpos'})


		# x:30 y:307, x:130 y:307
		_sm_pick_and_react_to_errors_4 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['name', 'category', 'entity_list', 'j', 'entityID', 'rotToTable'])

		with _sm_pick_and_react_to_errors_4:
			# x:30 y:240
			OperatableStateMachine.add('Action_pick',
										self.use_behavior(Action_pickSM, 'Pick and place all objects/Pick and react to errors/Action_pick'),
										transitions={'success': 'say name', 'unreachable': 'I really wanted to get this object', 'not found': 'Cannot find', 'dropped': 'Oops'},
										autonomy={'success': Autonomy.Inherit, 'unreachable': Autonomy.Inherit, 'not found': Autonomy.Inherit, 'dropped': Autonomy.Inherit},
										remapping={'objectID': 'entityID'})

			# x:354 y:198
			OperatableStateMachine.add('Cannot find',
										SaraSay(sentence="Looks like I can no longer find it!", emotion=3, block=True),
										transitions={'done': 'I really wanted to get this object'},
										autonomy={'done': Autonomy.Off})

			# x:341 y:273
			OperatableStateMachine.add('say name',
										SaraSayKey(Format="This {}", emotion=1, block=True),
										transitions={'done': 'say cat'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'name'})

			# x:344 y:356
			OperatableStateMachine.add('say cat',
										SaraSayKey(Format="is a type of {}", emotion=1, block=True),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'category'})

			# x:233 y:40
			OperatableStateMachine.add('I really wanted to get this object',
										_sm_i_really_wanted_to_get_this_object_1,
										transitions={'finished': 'failed'},
										autonomy={'finished': Autonomy.Inherit},
										remapping={'entity_list': 'entity_list', 'j': 'j'})

			# x:220 y:161
			OperatableStateMachine.add('Oops',
										SaraSay(sentence="Oops! I dropped it.", emotion=3, block=True),
										transitions={'done': 'I really wanted to get this object'},
										autonomy={'done': Autonomy.Off})


		# x:826 y:181, x:130 y:293
		_sm_searchtable_5 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['empty'], output_keys=['nbrQuartTour'])

		with _sm_searchtable_5:
			# x:38 y:43
			OperatableStateMachine.add('setRotation',
										SetKey(Value=90),
										transitions={'done': 'nbrQuartTour'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'rotation'})

			# x:492 y:50
			OperatableStateMachine.add('list_entities_by_name',
										list_entities_by_name(frontality_level=0.5, distance_max=10),
										transitions={'found': 'getApproxTablePos', 'none_found': 'Three turns done?'},
										autonomy={'found': Autonomy.Off, 'none_found': Autonomy.Off},
										remapping={'name': 'empty', 'entity_list': 'entity_list', 'number': 'number'})

			# x:666 y:74
			OperatableStateMachine.add('getApproxTablePos',
										CalculationState(calculation=lambda x: x[0].position),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'entity_list', 'output_value': 'approxTablePos'})

			# x:186 y:40
			OperatableStateMachine.add('action_turn',
										self.use_behavior(action_turnSM, 'Look for Table s objects/searchTable/action_turn'),
										transitions={'finished': 'incrementNbrQuartTour', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'rotation': 'rotation'})

			# x:30 y:149
			OperatableStateMachine.add('nbrQuartTour',
										SetKey(Value=0),
										transitions={'done': 'action_turn'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'nbrQuartTour'})

			# x:332 y:25
			OperatableStateMachine.add('incrementNbrQuartTour',
										CalculationState(calculation=lambda x: x+1),
										transitions={'done': 'list_entities_by_name'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'nbrQuartTour', 'output_value': 'nbrQuartTour'})

			# x:341 y:161
			OperatableStateMachine.add('Three turns done?',
										CheckConditionState(predicate=lambda x : x >= 3),
										transitions={'true': 'failed', 'false': 'action_turn'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'nbrQuartTour'})


		# x:30 y:293, x:130 y:293
		_sm_try_to_open_the_door_6 = OperatableStateMachine(outcomes=['finished', 'failed'])

		with _sm_try_to_open_the_door_6:
			# x:52 y:85
			OperatableStateMachine.add('PLACEHOLDER',
										WaitState(wait_time=0),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})


		# x:30 y:293
		_sm_pick_and_place_all_objects_7 = OperatableStateMachine(outcomes=['end'], input_keys=['categories', 'cbXpos', 'hauteur3rdShelfFromFloor', 'zero', 'rotToTable', 'rotToCupboard', 'cbYpos', 'placeZoffset'])

		with _sm_pick_and_place_all_objects_7:
			# x:30 y:36
			OperatableStateMachine.add('To be sure that all objects were picked',
										ForLoop(repeat=2),
										transitions={'do': 'ForEachCategory', 'end': 'end'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'tryIndex'})

			# x:172 y:166
			OperatableStateMachine.add('shelfPos',
										GenPoseEulerKey(),
										transitions={'done': 'ForEachEntity'},
										autonomy={'done': Autonomy.Off},
										remapping={'xpos': 'cbXpos', 'ypos': 'cbYpos', 'zpos': 'hauteur3rdShelfFromFloor', 'yaw': 'zero', 'pitch': 'zero', 'roll': 'zero', 'pose': 'shelfPos'})

			# x:585 y:262
			OperatableStateMachine.add('Pick and react to errors',
										_sm_pick_and_react_to_errors_4,
										transitions={'done': 'FaceCupboard', 'failed': 'FaceCupboard2'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'name': 'name', 'category': 'category', 'entity_list': 'entity_list', 'j': 'j', 'entityID': 'entityID', 'rotToTable': 'rotToTable'})

			# x:612 y:40
			OperatableStateMachine.add('failed to place',
										SaraSayKey(Format="Oops. Looks like I failed to place this {}. Maybe I'm not flexible enough", emotion=3, block=True),
										transitions={'done': 'ForEachEntity'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'name'})

			# x:827 y:109
			OperatableStateMachine.add('place near same name or cat ',
										_sm_place_near_same_name_or_cat__3,
										transitions={'finished': 'ForEachEntity', 'failed': 'failed to place'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'shelfPos': 'shelfPos', 'name': 'name', 'zero': 'zero', 'placeZoffset': 'placeZoffset', 'category': 'category'})

			# x:295 y:84
			OperatableStateMachine.add('ForEachCategory',
										ForLoop(repeat=lengthCategories),
										transitions={'do': 'shelfPos', 'end': 'To be sure that all objects were picked'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'i'})

			# x:804 y:201
			OperatableStateMachine.add('FaceCupboard',
										self.use_behavior(action_turnSM, 'Pick and place all objects/FaceCupboard'),
										transitions={'finished': 'place near same name or cat ', 'failed': 'FaceCupboard'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'rotation': 'rotToCupboard'})

			# x:418 y:16
			OperatableStateMachine.add('FaceCupboard2',
										self.use_behavior(action_turnSM, 'Pick and place all objects/FaceCupboard2'),
										transitions={'finished': 'ForEachCategory', 'failed': 'FaceCupboard2'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'rotation': 'rotToCupboard'})

			# x:335 y:268
			OperatableStateMachine.add('ForEachEntity',
										_sm_foreachentity_2,
										transitions={'end': 'ForEachCategory', 'not_found': 'ForEachCategory', 'done': 'Pick and react to errors', 'failed': 'end'},
										autonomy={'end': Autonomy.Inherit, 'not_found': Autonomy.Inherit, 'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'categories': 'categories', 'i': 'i', 'rotToTable': 'rotToTable', 'entity_list': 'entity_list', 'j': 'j', 'category': 'category', 'entityID': 'entityID', 'name': 'name', 'category': 'category'})


		# x:768 y:153, x:229 y:313
		_sm_look_for_table_s_objects_8 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['empty'], output_keys=['rotToCupboard', 'rotToTable'])

		with _sm_look_for_table_s_objects_8:
			# x:25 y:0
			OperatableStateMachine.add('searchTable',
										_sm_searchtable_5,
										transitions={'done': 'setRotToTable', 'failed': 'failed'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'empty': 'empty', 'nbrQuartTour': 'nbrQuartTour'})

			# x:321 y:37
			OperatableStateMachine.add('setRotToTable',
										CalculationState(calculation=lambda x: x*90),
										transitions={'done': 'setRotToCupboard'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'nbrQuartTour', 'output_value': 'rotToTable'})

			# x:495 y:78
			OperatableStateMachine.add('setRotToCupboard',
										CalculationState(calculation=lambda x: -x),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'rotToTable', 'output_value': 'rotToCupboard'})


		# x:30 y:296, x:130 y:296, x:619 y:302
		_sm_get_cupboardpos_9 = OperatableStateMachine(outcomes=['none', 'error', 'done'], input_keys=['empty', 'nomArmoire'], output_keys=['distance', 'cbXpos', 'cbZpos', 'cupboardPos'])

		with _sm_get_cupboardpos_9:
			# x:30 y:136
			OperatableStateMachine.add('GetListeofCupboard',
										WonderlandGetEntityVerbal(),
										transitions={'one': 'getCupboardPos', 'multiple': 'getCupboardPos', 'none': 'none', 'error': 'error'},
										autonomy={'one': Autonomy.Off, 'multiple': Autonomy.Off, 'none': Autonomy.Off, 'error': Autonomy.Off},
										remapping={'name': 'nomArmoire', 'containers': 'empty', 'entities': 'cupboards'})

			# x:253 y:45
			OperatableStateMachine.add('getCupboardPos',
										CalculationState(calculation=lambda x: x[0].position),
										transitions={'done': 'setDistance'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'cupboards', 'output_value': 'cupboardPos'})

			# x:557 y:33
			OperatableStateMachine.add('getApproachCupboard',
										Get_Reacheable_Waypoint(),
										transitions={'done': 'cbXpos'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose_in': 'cupboardPos', 'distance': 'distance', 'pose_out': 'approachCupboard'})

			# x:416 y:42
			OperatableStateMachine.add('setDistance',
										SetKey(Value=1.0),
										transitions={'done': 'getApproachCupboard'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'distance'})

			# x:436 y:137
			OperatableStateMachine.add('cbXpos',
										CalculationState(calculation=lambda x: x.position.x),
										transitions={'done': 'cbZpos'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'cupboardPos', 'output_value': 'cbXpos'})

			# x:409 y:231
			OperatableStateMachine.add('cbZpos',
										CalculationState(calculation=lambda x: x.position.y),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'cupboardPos', 'output_value': 'cbYpos'})



		with _state_machine:
			# x:43 y:204
			OperatableStateMachine.add('Look for Table s objects',
										_sm_look_for_table_s_objects_8,
										transitions={'finished': 'FaceCupboard', 'failed': 'Cannot find table'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'empty': 'empty', 'rotToCupboard': 'rotToCupboard', 'rotToTable': 'rotToTable'})

			# x:309 y:124
			OperatableStateMachine.add('Cannot find table',
										SaraSay(sentence="I did not find the table, let me try again.", emotion=3, block=True),
										transitions={'done': 'Get CupBoardPos'},
										autonomy={'done': Autonomy.Off})

			# x:267 y:630
			OperatableStateMachine.add('Pick and place all objects',
										_sm_pick_and_place_all_objects_7,
										transitions={'end': 'finished'},
										autonomy={'end': Autonomy.Inherit},
										remapping={'categories': 'categories', 'cbXpos': 'cbXpos', 'hauteur3rdShelfFromFloor': 'hauteur3rdShelfFromFloor', 'zero': 'zero', 'rotToTable': 'rotToTable', 'rotToCupboard': 'rotToCupboard', 'cbYpos': 'cbYpos', 'placeZoffset': 'placeZoffset'})

			# x:28 y:403
			OperatableStateMachine.add('Try to open the door',
										_sm_try_to_open_the_door_6,
										transitions={'finished': 'Pick and place all objects', 'failed': 'Can you open it for me?'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:34 y:496
			OperatableStateMachine.add('Can you open it for me?',
										SaraSay(sentence="I'm not able to open the door. Can someone do it for me please?", emotion=1, block=True),
										transitions={'done': 'wait for open door'},
										autonomy={'done': Autonomy.Off})

			# x:42 y:568
			OperatableStateMachine.add('wait for open door',
										WaitState(wait_time=6),
										transitions={'done': 'Thanks'},
										autonomy={'done': Autonomy.Off})

			# x:67 y:638
			OperatableStateMachine.add('Thanks',
										SaraSay(sentence="Thank you.", emotion=1, block=True),
										transitions={'done': 'Pick and place all objects'},
										autonomy={'done': Autonomy.Off})

			# x:44 y:300
			OperatableStateMachine.add('FaceCupboard',
										self.use_behavior(action_turnSM, 'FaceCupboard'),
										transitions={'finished': 'Try to open the door', 'failed': 'FaceCupboard'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'rotation': 'rotToCupboard'})

			# x:26 y:77
			OperatableStateMachine.add('Get CupBoardPos',
										_sm_get_cupboardpos_9,
										transitions={'none': 'failed', 'error': 'failed', 'done': 'Look for Table s objects'},
										autonomy={'none': Autonomy.Inherit, 'error': Autonomy.Inherit, 'done': Autonomy.Inherit},
										remapping={'empty': 'empty', 'nomArmoire': 'nomArmoire', 'distance': 'distance', 'cbXpos': 'cbXpos', 'cbZpos': 'cbYpos', 'cupboardPos': 'cupboardPos'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
