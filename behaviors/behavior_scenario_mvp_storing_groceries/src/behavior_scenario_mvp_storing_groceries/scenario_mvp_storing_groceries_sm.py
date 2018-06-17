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
from behavior_action_pick.action_pick_sm import Action_pickSM
from sara_flexbe_states.binary_calculation_state import BinaryCalculationState
from sara_flexbe_states.for_loop import ForLoop
from sara_flexbe_states.list_entities_by_name import list_entities_by_name
from sara_flexbe_states.sara_say_key import SaraSayKey
from sara_flexbe_states.sara_say import SaraSay
from behavior_action_place.action_place_sm import Action_placeSM
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.get_reachable_waypoint import Get_Reacheable_Waypoint
from sara_flexbe_states.SetKey import SetKey
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
		self.add_behavior(Action_pickSM, 'Action_pick')
		self.add_behavior(Action_placeSM, 'Action_place')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		lengthCategories = 5
		# x:72 y:406, x:163 y:457
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['categories'])
		_state_machine.userdata.nomTable = "table"
		_state_machine.userdata.empty = ""
		_state_machine.userdata.categories = ["drinks","snacks","fruits","cleaning stuff","food"]

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:508 y:61
		_sm_i_really_wanted_to_get_this_$object_0 = OperatableStateMachine(outcomes=['done'], input_keys=['entity_list', 'j'])

		with _sm_i_really_wanted_to_get_this_$object_0:
			# x:30 y:95
			OperatableStateMachine.add('getEntityName',
										BinaryCalculationState(calculation=lambda x: x[y].name),
										transitions={'done': 'this $object'},
										autonomy={'done': Autonomy.Off},
										remapping={'X': 'entity_list', 'Y': 'j', 'Z': 'name'})

			# x:261 y:51
			OperatableStateMachine.add('this $object',
										SaraSayKey(Format=I really wanted to get this {}., emotion=3, block=True),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'name'})


		# x:208 y:217, x:19 y:210, x:753 y:219
		_sm_foreachentity_1 = OperatableStateMachine(outcomes=['end', 'not_found', 'done'], input_keys=['categories', 'i'], output_keys=['entity_list', 'j', 'category', 'entityID', 'name'])

		with _sm_foreachentity_1:
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
										transitions={'found': 'ForEverySimilarItems', 'not_found': 'not_found'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'name': 'category', 'entity_list': 'entity_list', 'number': 'nbrEntities'})



		with _state_machine:
			# x:34 y:23
			OperatableStateMachine.add('GetListeofTable',
										WonderlandGetEntityVerbal(),
										transitions={'one': 'getTablePosition', 'multiple': 'getTablePosition', 'none': 'failed', 'error': 'failed'},
										autonomy={'one': Autonomy.Off, 'multiple': Autonomy.Off, 'none': Autonomy.Off, 'error': Autonomy.Off},
										remapping={'name': 'nomTable', 'containers': 'empty', 'entities': 'tables'})

			# x:569 y:277
			OperatableStateMachine.add('Action_pick',
										self.use_behavior(Action_pickSM, 'Action_pick'),
										transitions={'success': 'say name', 'unreachable': 'I really wanted to get this $object', 'not found': 'Can't find', 'dropped': 'Oops'},
										autonomy={'success': Autonomy.Inherit, 'unreachable': Autonomy.Inherit, 'not found': Autonomy.Inherit, 'dropped': Autonomy.Inherit},
										remapping={'objectID': 'entityID'})

			# x:356 y:351
			OperatableStateMachine.add('ForEachEntity',
										_sm_foreachentity_1,
										transitions={'end': 'ForEachCategory', 'not_found': 'ForEachCategory', 'done': 'Action_pick'},
										autonomy={'end': Autonomy.Inherit, 'not_found': Autonomy.Inherit, 'done': Autonomy.Inherit},
										remapping={'categories': 'categories', 'i': 'i', 'entity_list': 'entity_list', 'j': 'j', 'category': 'category', 'entityID': 'entityID', 'name': 'name'})

			# x:743 y:93
			OperatableStateMachine.add('I really wanted to get this $object',
										_sm_i_really_wanted_to_get_this_$object_0,
										transitions={'done': 'ForEachCategory'},
										autonomy={'done': Autonomy.Inherit},
										remapping={'entity_list': 'entity_list', 'j': 'j'})

			# x:818 y:193
			OperatableStateMachine.add('Oops',
										SaraSay(sentence=Oops! I dropped it., emotion=3, block=True),
										transitions={'done': 'I really wanted to get this $object'},
										autonomy={'done': Autonomy.Off})

			# x:904 y:247
			OperatableStateMachine.add('Can't find',
										SaraSay(sentence=Looks like I can no longer find it!, emotion=3, block=True),
										transitions={'done': 'I really wanted to get this $object'},
										autonomy={'done': Autonomy.Off})

			# x:851 y:363
			OperatableStateMachine.add('say name',
										SaraSayKey(Format=This {}, emotion=1, block=True),
										transitions={'done': 'say cat'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'name'})

			# x:768 y:455
			OperatableStateMachine.add('say cat',
										SaraSayKey(Format=is a type of {}, emotion=1, block=True),
										transitions={'done': 'Action_place'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'category'})

			# x:572 y:443
			OperatableStateMachine.add('Action_place',
										self.use_behavior(Action_placeSM, 'Action_place'),
										transitions={'finished': 'ForEachCategory', 'failed': 'Oops'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pos': 'tablePos'})

			# x:257 y:13
			OperatableStateMachine.add('getTablePosition',
										CalculationState(calculation=lambda x: x[0].position),
										transitions={'done': 'setDistance'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'tables', 'output_value': 'tablePos'})

			# x:558 y:8
			OperatableStateMachine.add('getApproach',
										Get_Reacheable_Waypoint(),
										transitions={'done': 'ForEachCategory'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose_in': 'tablePos', 'distance': 'distance', 'pose_out': 'approachTable'})

			# x:420 y:10
			OperatableStateMachine.add('setDistance',
										SetKey(Value=1.0),
										transitions={'done': 'getApproach'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'distance'})

			# x:446 y:205
			OperatableStateMachine.add('ForEachCategory',
										ForLoop(repeat=lengthCategories),
										transitions={'do': 'ForEachEntity', 'end': 'finished'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'i'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
