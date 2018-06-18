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
from sara_flexbe_states.binary_calculation_state import BinaryCalculationState
from sara_flexbe_states.for_loop import ForLoop
from sara_flexbe_states.list_entities_by_name import list_entities_by_name
from sara_flexbe_states.pose_gen_euler_key import GenPoseEulerKey
from behavior_action_pick.action_pick_sm import Action_pickSM
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.sara_say_key import SaraSayKey
from behavior_action_turn.action_turn_sm import action_turnSM
from behavior_action_place.action_place_sm import Action_placeSM
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
		self.add_behavior(Action_pickSM, 'Pick & react to errors/Action_pick')
		self.add_behavior(action_turnSM, 'LookAt cupboard/action_turn')
		self.add_behavior(Action_placeSM, 'place near same name or cat /Action_place')
		self.add_behavior(action_turnSM, 'Look for Table's objects/action_turn')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:

		# O 216 14 
		# Still need the |ntableRelativePos by|nlooking for multiple|n same y objects

		# O 274 417 
		# Add offset |nfor each category|nplaceXpos=i*offset+cbPos|nif side == x



	def create(self):
		lengthCategories = 5
		# x:113 y:483, x:22 y:219
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['nomArmoire'])
		_state_machine.userdata.nomTable = "table"
		_state_machine.userdata.empty = ""
		_state_machine.userdata.categories = ["drinks","snacks","fruits","cleaning stuff","food"]
		_state_machine.userdata.nomArmoire = "cupboard"
		_state_machine.userdata.zero = 0
		_state_machine.userdata.hauteur3rdShelfFromFloor = 64
		_state_machine.userdata.placeYoffset = 0.05

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:30 y:293
		_sm_i_really_wanted_to_get_this_object_0 = OperatableStateMachine(outcomes=['finished'], input_keys=['entity_list', 'j'])

		with _sm_i_really_wanted_to_get_this_object_0:
			# x:96 y:37
			OperatableStateMachine.add('getEntityName',
										BinaryCalculationState(calculation=lambda x: x[y].name),
										transitions={'done': 'I really wanted to get this'},
										autonomy={'done': Autonomy.Off},
										remapping={'X': 'entity_list', 'Y': 'j', 'Z': 'name'})

			# x:309 y:42
			OperatableStateMachine.add('I really wanted to get this',
										SaraSayKey(Format=I really wanted to get this {}., emotion=3, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'name'})


		# x:762 y:247, x:130 y:293
		_sm_look_for_table's_objects_1 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['empty'], output_keys=['nbrQuartTour'])

		with _sm_look_for_table's_objects_1:
			# x:43 y:30
			OperatableStateMachine.add('setRotation',
										SetKey(Value=90),
										transitions={'done': 'action_turn'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'rotation'})

			# x:414 y:35
			OperatableStateMachine.add('list_entities_by_name',
										list_entities_by_name(frontality_level=0.5, distance_max=10),
										transitions={'found': 'getApproxTablePos', 'none_found': 'action_turn'},
										autonomy={'found': Autonomy.Off, 'none_found': Autonomy.Off},
										remapping={'name': 'empty', 'entity_list': 'entity_list', 'number': 'number'})

			# x:628 y:94
			OperatableStateMachine.add('getApproxTablePos',
										CalculationState(calculation=lambda x: x[0].position),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'entity_list', 'output_value': 'approxTablePos'})

			# x:223 y:43
			OperatableStateMachine.add('action_turn',
										self.use_behavior(action_turnSM, 'Look for Table's objects/action_turn'),
										transitions={'finished': 'list_entities_by_name', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'rotation': 'rotation'})


		# x:741 y:442, x:712 y:520
		_sm_place_near_same_name_or_cat__2 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['shelfPos', 'placeYoffset', 'category', 'name', 'zero'])

		with _sm_place_near_same_name_or_cat__2:
			# x:224 y:112
			OperatableStateMachine.add('list_entities_by_name',
										list_entities_by_name(frontality_level=0.5, distance_max=4),
										transitions={'found': 'getPos', 'none_found': 'list_entities_by_category'},
										autonomy={'found': Autonomy.Off, 'none_found': Autonomy.Off},
										remapping={'name': 'name', 'entity_list': 'cp_entity_list', 'number': 'cp_entity_number'})

			# x:440 y:93
			OperatableStateMachine.add('getPos',
										CalculationState(calculation=lambda x: x[0].position),
										transitions={'done': 'addYOffset'},
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
										self.use_behavior(Action_placeSM, 'place near same name or cat /Action_place'),
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
			OperatableStateMachine.add('addYOffset',
										BinaryCalculationState(calculation=lambda x: x.y-y),
										transitions={'done': 'get_zpos'},
										autonomy={'done': Autonomy.Off},
										remapping={'X': 'posSimilar', 'Y': 'placeYoffset', 'Z': 'ypos'})

			# x:588 y:156
			OperatableStateMachine.add('get_zpos',
										CalculationState(calculation=lambda x: x.z),
										transitions={'done': 'get_xpos'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'posSimilar', 'output_value': 'zpos'})

			# x:659 y:233
			OperatableStateMachine.add('get_xpos',
										CalculationState(calculation=lambda x: x.x),
										transitions={'done': 'Addoffset'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'posSimilar', 'output_value': 'xpos'})


		# x:140 y:296, x:406 y:297
		_sm_lookat_cupboard_3 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['nbrQuartTour'])

		with _sm_lookat_cupboard_3:
			# x:30 y:40
			OperatableStateMachine.add('get rotation',
										CalculationState(calculation=lambda x: -(x*90)),
										transitions={'done': 'action_turn'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'nbrQuartTour', 'output_value': 'rotation'})

			# x:215 y:31
			OperatableStateMachine.add('action_turn',
										self.use_behavior(action_turnSM, 'LookAt cupboard/action_turn'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'rotation': 'rotation'})


		# x:301 y:468, x:73 y:99
		_sm_pick_&_react_to_errors_4 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['name', 'category', 'entity_list', 'j', 'entityID'])

		with _sm_pick_&_react_to_errors_4:
			# x:30 y:240
			OperatableStateMachine.add('Action_pick',
										self.use_behavior(Action_pickSM, 'Pick & react to errors/Action_pick'),
										transitions={'success': 'say name', 'unreachable': 'I really wanted to get this object', 'not found': 'Cannot find', 'dropped': 'Oops'},
										autonomy={'success': Autonomy.Inherit, 'unreachable': Autonomy.Inherit, 'not found': Autonomy.Inherit, 'dropped': Autonomy.Inherit},
										remapping={'objectID': 'entityID'})

			# x:354 y:198
			OperatableStateMachine.add('Cannot find',
										SaraSay(sentence=Looks like I can no longer find it!, emotion=3, block=True),
										transitions={'done': 'I really wanted to get this object'},
										autonomy={'done': Autonomy.Off})

			# x:341 y:273
			OperatableStateMachine.add('say name',
										SaraSayKey(Format=This {}, emotion=1, block=True),
										transitions={'done': 'say cat'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'name'})

			# x:344 y:356
			OperatableStateMachine.add('say cat',
										SaraSayKey(Format=is a type of {}, emotion=1, block=True),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'category'})

			# x:233 y:40
			OperatableStateMachine.add('I really wanted to get this object',
										_sm_i_really_wanted_to_get_this_object_0,
										transitions={'finished': 'failed'},
										autonomy={'finished': Autonomy.Inherit},
										remapping={'entity_list': 'entity_list', 'j': 'j'})

			# x:220 y:161
			OperatableStateMachine.add('Oops',
										SaraSay(sentence=Oops! I dropped it., emotion=3, block=True),
										transitions={'done': 'I really wanted to get this object'},
										autonomy={'done': Autonomy.Off})


		# x:208 y:217, x:19 y:210, x:753 y:219
		_sm_foreachentity_5 = OperatableStateMachine(outcomes=['end', 'not_found', 'done'], input_keys=['categories', 'i'], output_keys=['entity_list', 'j', 'category', 'entityID', 'name'])

		with _sm_foreachentity_5:
			# x:30 y:40
			OperatableStateMachine.add('getCategory',
										BinaryCalculationState(calculation=lambda x: x[y]),
										transitions={'done': 'list_entities_by_name'},
										autonomy={'done': Autonomy.Off},
										remapping={'X': 'categories', 'Y': 'i', 'Z': 'category'})

			# x:259 y:122
			OperatableStateMachine.add('ForEverySimilarItems',
										ForLoop(repeat=nbrEntities),
										transitions={'do': 'getEntityId', 'end': 'end'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'j'})

			# x:363 y:189
			OperatableStateMachine.add('getEntityId',
										BinaryCalculationState(calculation=lambda x: x[j].id),
										transitions={'done': 'getEntityName'},
										autonomy={'done': Autonomy.Off},
										remapping={'X': 'entity_list', 'Y': 'j', 'Z': 'entityID'})

			# x:565 y:155
			OperatableStateMachine.add('getEntityName',
										BinaryCalculationState(calculation=lambda x: x[j].name),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off},
										remapping={'X': 'entity_list', 'Y': 'j', 'Z': 'name'})

			# x:33 y:116
			OperatableStateMachine.add('list_entities_by_name',
										list_entities_by_name(frontality_level=0.5, distance_max=10),
										transitions={'found': 'ForEverySimilarItems', 'none_found': 'not_found'},
										autonomy={'found': Autonomy.Off, 'none_found': Autonomy.Off},
										remapping={'name': 'category', 'entity_list': 'entity_list', 'number': 'nbrEntities'})


		# x:30 y:296, x:130 y:296, x:619 y:302
		_sm_get_cupboardpos_6 = OperatableStateMachine(outcomes=['none', 'error', 'done'], input_keys=['empty', 'nomArmoire'], output_keys=['tablePos', 'distance', 'cbXpos', 'cbZpos'])

		with _sm_get_cupboardpos_6:
			# x:30 y:55
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
										CalculationState(calculation=lambda x: x.position.z),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'cupboardPos', 'output_value': 'cbZpos'})



		with _state_machine:
			# x:43 y:27
			OperatableStateMachine.add('Get CupBoardPos',
										_sm_get_cupboardpos_6,
										transitions={'none': 'failed', 'error': 'failed', 'done': 'Look for Table's objects'},
										autonomy={'none': Autonomy.Inherit, 'error': Autonomy.Inherit, 'done': Autonomy.Inherit},
										remapping={'empty': 'empty', 'nomArmoire': 'nomArmoire', 'tablePos': 'cupboardPos', 'distance': 'distance', 'cbXpos': 'cbXpos', 'cbZpos': 'cbZpos'})

			# x:484 y:404
			OperatableStateMachine.add('ForEachEntity',
										_sm_foreachentity_5,
										transitions={'end': 'ForEachCategory', 'not_found': 'ForEachCategory', 'done': 'Pick & react to errors'},
										autonomy={'end': Autonomy.Inherit, 'not_found': Autonomy.Inherit, 'done': Autonomy.Inherit},
										remapping={'categories': 'categories', 'i': 'i', 'entity_list': 'entity_list', 'j': 'j', 'category': 'category', 'entityID': 'entityID', 'name': 'name'})

			# x:346 y:349
			OperatableStateMachine.add('GenPoseEulerKey',
										GenPoseEulerKey(),
										transitions={'done': 'ForEachEntity'},
										autonomy={'done': Autonomy.Off},
										remapping={'xpos': 'cbXpos', 'ypos': 'hauteur3rdShelfFromFloor', 'zpos': 'cbZpos', 'yaw': 'zero', 'pitch': 'zero', 'roll': 'zero', 'pose': 'shelfPos'})

			# x:766 y:421
			OperatableStateMachine.add('Pick & react to errors',
										_sm_pick_&_react_to_errors_4,
										transitions={'done': 'LookAt cupboard', 'failed': 'ForEachCategory'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'name': 'name', 'category': 'category', 'entity_list': 'entity_list', 'j': 'j', 'entityID': 'entityID'})

			# x:764 y:77
			OperatableStateMachine.add('failed to place',
										SaraSayKey(Format="Oops. Looks like I failed to place this {}. Maybe I'm not flexible enough", emotion=3, block=True),
										transitions={'done': 'ForEachEntity'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'name'})

			# x:1011 y:306
			OperatableStateMachine.add('LookAt cupboard',
										_sm_lookat_cupboard_3,
										transitions={'finished': 'place near same name or cat ', 'failed': 'LookAt cupboard'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'nbrQuartTour': 'nbrQuartTour'})

			# x:974 y:54
			OperatableStateMachine.add('place near same name or cat ',
										_sm_place_near_same_name_or_cat__2,
										transitions={'finished': 'ForEachEntity', 'failed': 'failed to place'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'shelfPos': 'shelfPos', 'placeYoffset': 'placeYoffset', 'category': 'category', 'name': 'name', 'zero': 'zero'})

			# x:449 y:249
			OperatableStateMachine.add('ForEachCategory',
										ForLoop(repeat=lengthCategories),
										transitions={'do': 'GenPoseEulerKey', 'end': 'To be sure that all objects were picked'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'i'})

			# x:184 y:249
			OperatableStateMachine.add('To be sure that all objects were picked',
										ForLoop(repeat=2),
										transitions={'do': 'ForEachCategory', 'end': 'finished'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'tryIndex'})

			# x:215 y:94
			OperatableStateMachine.add('Look for Table's objects',
										_sm_look_for_table's_objects_1,
										transitions={'finished': 'To be sure that all objects were picked', 'failed': 'Cannot find table'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'empty': 'empty', 'nbrQuartTour': 'nbrQuartTour'})

			# x:456 y:43
			OperatableStateMachine.add('Cannot find table',
										SaraSay(sentence="I didn't find the table, let me try again.", emotion=3, block=True),
										transitions={'done': 'Get CupBoardPos'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
