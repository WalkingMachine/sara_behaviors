#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_actionwrapper_move')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.story import Set_Story
from sara_flexbe_states.set_a_step import Set_a_step
from sara_flexbe_states.WonderlandGetEntityVerbal import WonderlandGetEntityVerbal
from sara_flexbe_states.SetKey import SetKey
from flexbe_states.calculation_state import CalculationState
from flexbe_states.flexible_check_condition_state import FlexibleCheckConditionState
from flexbe_states.log_key_state import LogKeyState
from flexbe_states.flexible_calculation_state import FlexibleCalculationState
from sara_flexbe_states.WonderlandGetEntityByID import WonderlandGetEntityByID
from flexbe_states.check_condition_state import CheckConditionState
from sara_flexbe_states.sara_say_key import SaraSayKey
from sara_flexbe_states.sara_say import SaraSay
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on 22/05/2018
@author: Lucas Maurice
'''
class ActionWrapper_MoveSM(Behavior):
	'''
	action wrapper pour move
	'''


	def __init__(self):
		super(ActionWrapper_MoveSM, self).__init__()
		self.name = 'ActionWrapper_Move'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
        
        # [/MANUAL_INIT]

		# Behavior comments:

		# O 1262 27 
		# Move|n1- Location|n2- Location Container|n3- Location Container

		# O 1260 94 
		# Story|n0- Decompose Command|n1- Find Area|n2- Join Area|n3- END



	def create(self):
		# x:470 y:280, x:618 y:290
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['Action'])
		_state_machine.userdata.Action = ["Move", "table"]
		_state_machine.userdata.relative = False

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

		# x:128 y:568
		_sm_get_area_containers_0 = OperatableStateMachine(outcomes=['done'], input_keys=['command'], output_keys=['containers'])

		with _sm_get_area_containers_0:
			# x:46 y:31
			OperatableStateMachine.add('Set Empty Array',
										SetKey(Value=[]),
										transitions={'done': 'Set initial index'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'containers'})

			# x:50 y:110
			OperatableStateMachine.add('Set initial index',
										SetKey(Value=2),
										transitions={'done': 'Set Loop Max'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'iLoop'})

			# x:49 y:192
			OperatableStateMachine.add('Set Loop Max',
										CalculationState(calculation=lambda x: len(x)),
										transitions={'done': 'Check Loop End'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'command', 'output_value': 'iLoopMax'})

			# x:514 y:278
			OperatableStateMachine.add('Increment',
										CalculationState(calculation=lambda x: x+1),
										transitions={'done': 'Print container array'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'iLoop', 'output_value': 'iLoop'})

			# x:271 y:154
			OperatableStateMachine.add('Add Container to Array',
										FlexibleCalculationState(calculation=lambda x: x[2]+[ x[0][ x[1] ] ], input_keys=['command','iLoop','containers']),
										transitions={'done': 'Increment'},
										autonomy={'done': Autonomy.Off},
										remapping={'command': 'command', 'iLoop': 'iLoop', 'containers': 'containers', 'output_value': 'containers'})

			# x:42 y:287
			OperatableStateMachine.add('Check Loop End',
										FlexibleCheckConditionState(predicate=lambda x: x[0] < x[1], input_keys=['iLoop','iLoopMax']),
										transitions={'true': 'Add Container to Array', 'false': 'done'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'iLoop': 'iLoop', 'iLoopMax': 'iLoopMax'})

			# x:279 y:401
			OperatableStateMachine.add('Print container array',
										LogKeyState(text="Containers: \n {}", severity=Logger.REPORT_HINT),
										transitions={'done': 'Check Loop End'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'containers'})


		# x:30 y:458
		_sm_export_waypoint_1 = OperatableStateMachine(outcomes=['done'], input_keys=['entities'], output_keys=['waipoint', 'area_name'])

		with _sm_export_waypoint_1:
			# x:55 y:46
			OperatableStateMachine.add('Extract Wayppoint',
										CalculationState(calculation=lambda x: x.waypoint),
										transitions={'done': 'Extract Name'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'entities', 'output_value': 'waipoint'})

			# x:257 y:46
			OperatableStateMachine.add('LogWaypoint',
										LogKeyState(text="Will go to waypoint:\n{}", severity=Logger.REPORT_HINT),
										transitions={'done': 'LogName'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'waipoint'})

			# x:61 y:120
			OperatableStateMachine.add('Extract Name',
										CalculationState(calculation=lambda x: x.name),
										transitions={'done': 'LogWaypoint'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'entities', 'output_value': 'area_name'})

			# x:256 y:121
			OperatableStateMachine.add('LogName',
										LogKeyState(text="(Area name: {})", severity=Logger.REPORT_HINT),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'area_name'})


		# x:30 y:458
		_sm_export_no_waypoint_2 = OperatableStateMachine(outcomes=['done'], output_keys=['waipoint', 'area_name'])

		with _sm_export_no_waypoint_2:
			# x:30 y:40
			OperatableStateMachine.add('noWaypoint',
										SetKey(Value=None),
										transitions={'done': 'NoName'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'waipoint'})

			# x:127 y:44
			OperatableStateMachine.add('NoName',
										SetKey(Value=None),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'area_name'})


		# x:77 y:738
		_sm_list_areas_3 = OperatableStateMachine(outcomes=['done'], input_keys=['entities'], output_keys=['sentence'])

		with _sm_list_areas_3:
			# x:68 y:52
			OperatableStateMachine.add('initLoop',
										SetKey(Value=0),
										transitions={'done': 'GetSize'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'iLoop'})

			# x:46 y:142
			OperatableStateMachine.add('GetSize',
										CalculationState(calculation=lambda x: len(x.entities)),
										transitions={'done': 'InitSentence'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'entities', 'output_value': 'iMaxLoop'})

			# x:29 y:344
			OperatableStateMachine.add('CheckEndLoop',
										FlexibleCheckConditionState(predicate=lambda x: x[0] >= x[1], input_keys=['iLoop', 'iMaxLoop']),
										transitions={'true': 'done', 'false': 'getIndexEntity'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'iLoop': 'iLoop', 'iMaxLoop': 'iMaxLoop'})

			# x:287 y:375
			OperatableStateMachine.add('incrementIndex',
										CalculationState(calculation=lambda x: x+1),
										transitions={'done': 'CheckEndLoop'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'iLoop', 'output_value': 'iLoop'})

			# x:653 y:376
			OperatableStateMachine.add('log entity name',
										LogKeyState(text="Present Entity: \n{}", severity=Logger.REPORT_HINT),
										transitions={'done': 'ConcatSentence'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'areaName'})

			# x:265 y:163
			OperatableStateMachine.add('getIndexEntity',
										FlexibleCalculationState(calculation=lambda x: x[0].entities[x[1]], input_keys=['entities','iLoop']),
										transitions={'done': 'set area name'},
										autonomy={'done': Autonomy.Off},
										remapping={'entities': 'entities', 'iLoop': 'iLoop', 'output_value': 'entity'})

			# x:52 y:235
			OperatableStateMachine.add('InitSentence',
										SetKey(Value=""),
										transitions={'done': 'CheckEndLoop'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'sentence'})

			# x:454 y:377
			OperatableStateMachine.add('ConcatSentence',
										FlexibleCalculationState(calculation=lambda x: str(x[0]) + str(x[1]) + ", ", input_keys=['first', 'second']),
										transitions={'done': 'incrementIndex'},
										autonomy={'done': Autonomy.Off},
										remapping={'first': 'sentence', 'second': 'areaName', 'output_value': 'sentence'})

			# x:483 y:163
			OperatableStateMachine.add('set area name',
										CalculationState(calculation=lambda x: "The " + x.name),
										transitions={'done': 'Is there a container ?'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'entity', 'output_value': 'areaName'})

			# x:1034 y:404
			OperatableStateMachine.add('Get Container',
										WonderlandGetEntityByID(),
										transitions={'found': 'Add container to area name', 'not_found': 'log entity name', 'error': 'log entity name'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off, 'error': Autonomy.Off},
										remapping={'id': 'id', 'entity': 'entity', 'depth_position': 'depth_position', 'depth_waypoint': 'depth_waypoint'})

			# x:980 y:240
			OperatableStateMachine.add('Get Entity Id',
										CalculationState(calculation=lambda x: x.containerId),
										transitions={'done': 'Get Container'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'entity', 'output_value': 'id'})

			# x:1157 y:170
			OperatableStateMachine.add('Add container to area name',
										FlexibleCalculationState(calculation=lambda x: x[0] + " in " + x[1].name, input_keys=['areaName','entity']),
										transitions={'done': 'Is there a container ?'},
										autonomy={'done': Autonomy.Off},
										remapping={'areaName': 'areaName', 'entity': 'entity', 'output_value': 'areaName'})

			# x:657 y:164
			OperatableStateMachine.add('Is there a container ?',
										CheckConditionState(predicate=lambda x: x.containerId is not None),
										transitions={'true': 'Get Entity Id', 'false': 'log entity name'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'entity'})


		# x:871 y:59
		_sm_decomposecommand_4 = OperatableStateMachine(outcomes=['done'], input_keys=['command'], output_keys=['containers', 'area'])

		with _sm_decomposecommand_4:
			# x:163 y:34
			OperatableStateMachine.add('Set State Command',
										Set_a_step(step=0),
										transitions={'done': 'Get area name'},
										autonomy={'done': Autonomy.Off})

			# x:377 y:34
			OperatableStateMachine.add('Get area name',
										CalculationState(calculation=lambda x: x[1]),
										transitions={'done': 'Get area containers'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'command', 'output_value': 'area'})

			# x:600 y:30
			OperatableStateMachine.add('Get area containers',
										_sm_get_area_containers_0,
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Inherit},
										remapping={'command': 'command', 'containers': 'containers'})


		# x:1620 y:109, x:1648 y:375
		_sm_try_to_find_area_5 = OperatableStateMachine(outcomes=['found', 'not_found'], input_keys=['area_to_search', 'containers'], output_keys=['area_name', 'waypoint'])

		with _sm_try_to_find_area_5:
			# x:49 y:40
			OperatableStateMachine.add('Set state Find Area',
										Set_a_step(step=1),
										transitions={'done': 'GetEntityLocation'},
										autonomy={'done': Autonomy.Off})

			# x:152 y:219
			OperatableStateMachine.add('GetEntityLocation',
										WonderlandGetEntityVerbal(),
										transitions={'one': 'Export Waypoint', 'multiple': 'List areas', 'none': 'Say No Area', 'error': 'Say Error'},
										autonomy={'one': Autonomy.Off, 'multiple': Autonomy.Off, 'none': Autonomy.Off, 'error': Autonomy.Off},
										remapping={'name': 'area_to_search', 'containers': 'containers', 'entities': 'entities'})

			# x:431 y:200
			OperatableStateMachine.add('List areas',
										_sm_list_areas_3,
										transitions={'done': 'Say More Than One'},
										autonomy={'done': Autonomy.Inherit},
										remapping={'entities': 'entities', 'sentence': 'sentence'})

			# x:781 y:210
			OperatableStateMachine.add('Say Room List',
										SaraSayKey(Format=lambda x: "There is :" + x, emotion=1, block=True),
										transitions={'done': 'Say Be More Precise'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'sentence'})

			# x:600 y:209
			OperatableStateMachine.add('Say More Than One',
										SaraSayKey(Format=lambda x: "There is more than one " + str(x), emotion=1, block=True),
										transitions={'done': 'Say Room List'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'area_to_search'})

			# x:930 y:211
			OperatableStateMachine.add('Say Be More Precise',
										SaraSay(sentence="Can you repeat and be more precise please ?", emotion=1, block=True),
										transitions={'done': 'Export No Waypoint'},
										autonomy={'done': Autonomy.Off})

			# x:1246 y:294
			OperatableStateMachine.add('Export No Waypoint',
										_sm_export_no_waypoint_2,
										transitions={'done': 'not_found'},
										autonomy={'done': Autonomy.Inherit},
										remapping={'waipoint': 'waypoint', 'area_name': 'area_name'})

			# x:619 y:303
			OperatableStateMachine.add('Say No Area',
										SaraSayKey(Format=lambda x: "There is no " + str(x), emotion=1, block=True),
										transitions={'done': 'Export No Waypoint'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'area_to_search'})

			# x:628 y:383
			OperatableStateMachine.add('Say Error',
										SaraSay(sentence="I experience memory problem", emotion=1, block=True),
										transitions={'done': 'Say Error 2'},
										autonomy={'done': Autonomy.Off})

			# x:813 y:385
			OperatableStateMachine.add('Say Error 2',
										SaraSay(sentence="Can you try again please ?", emotion=1, block=True),
										transitions={'done': 'Export No Waypoint'},
										autonomy={'done': Autonomy.Off})

			# x:623 y:115
			OperatableStateMachine.add('Say going',
										SaraSayKey(Format=lambda x: "I'm going to the " + x, emotion=1, block=True),
										transitions={'done': 'found'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'area_name'})

			# x:429 y:116
			OperatableStateMachine.add('Export Waypoint',
										_sm_export_waypoint_1,
										transitions={'done': 'Say going'},
										autonomy={'done': Autonomy.Inherit},
										remapping={'entities': 'entities', 'waipoint': 'waypoint', 'area_name': 'area_name'})



		with _state_machine:
			# x:44 y:27
			OperatableStateMachine.add('Set Wrapper Story',
										Set_Story(titre="Move to Location", storyline=["Decompose Command","Find Area","Join Area","Finished"]),
										transitions={'done': 'DecomposeCommand'},
										autonomy={'done': Autonomy.Off})

			# x:58 y:340
			OperatableStateMachine.add('Set step Join Area',
										Set_a_step(step=2),
										transitions={'done': 'Set Finished'},
										autonomy={'done': Autonomy.Off})

			# x:45 y:226
			OperatableStateMachine.add('Try_to_find_area',
										_sm_try_to_find_area_5,
										transitions={'found': 'Set step Join Area', 'not_found': 'Set Finished'},
										autonomy={'found': Autonomy.Inherit, 'not_found': Autonomy.Inherit},
										remapping={'area_to_search': 'area', 'containers': 'containers', 'area_name': 'area_name', 'waypoint': 'waypoint'})

			# x:30 y:117
			OperatableStateMachine.add('DecomposeCommand',
										_sm_decomposecommand_4,
										transitions={'done': 'Try_to_find_area'},
										autonomy={'done': Autonomy.Inherit},
										remapping={'command': 'Action', 'containers': 'containers', 'area': 'area'})

			# x:325 y:269
			OperatableStateMachine.add('Set Finished',
										Set_a_step(step=3),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
