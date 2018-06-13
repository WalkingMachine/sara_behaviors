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
from sara_flexbe_states.sara_say_key import SaraSayKey
from flexbe_states.calculation_state import CalculationState
from behavior_wonderlanduniqueenity.wonderlanduniqueenity_sm import WonderlandUniqueEnitySM
from sara_flexbe_states.SetKey import SetKey
from flexbe_states.flexible_calculation_state import FlexibleCalculationState
from flexbe_states.flexible_check_condition_state import FlexibleCheckConditionState
from flexbe_states.log_key_state import LogKeyState
from behavior_action_move.action_move_sm import Action_MoveSM
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
		self.add_behavior(WonderlandUniqueEnitySM, 'Try to find area/WonderlandUniqueEnity')
		self.add_behavior(Action_MoveSM, 'Try to reach/Action_Move')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
        
        # [/MANUAL_INIT]

		# Behavior comments:

		# O 1262 27 
		# Move|n1- Location|n2- Location Container|n3- Location Container

		# O 1260 94 
		# Story|n0- Decompose Command|n1- Find Area|n2- Join Area|n3- END



	def create(self):
		# x:470 y:280, x:374 y:185, x:408 y:396
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'critical_fail'], input_keys=['Action'])
		_state_machine.userdata.Action = ["Move",'table','kitchen']
		_state_machine.userdata.relative = False

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

		# x:98 y:451
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
		_sm_export_no_waypoint_1 = OperatableStateMachine(outcomes=['done'], output_keys=['waipoint', 'area_name'])

		with _sm_export_no_waypoint_1:
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


		# x:30 y:458
		_sm_export_waypoint_2 = OperatableStateMachine(outcomes=['done'], input_keys=['entity'], output_keys=['waipoint', 'area_name'])

		with _sm_export_waypoint_2:
			# x:58 y:107
			OperatableStateMachine.add('Extract Wayppoint',
										CalculationState(calculation=lambda x: x.waypoint),
										transitions={'done': 'Extract Name'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'entity', 'output_value': 'waipoint'})

			# x:67 y:257
			OperatableStateMachine.add('Extract Name',
										CalculationState(calculation=lambda x: x.name),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'entity', 'output_value': 'area_name'})


		# x:38 y:481, x:447 y:470, x:230 y:365
		_sm_try_to_reach_3 = OperatableStateMachine(outcomes=['finished', 'failed', 'critical_fail'], input_keys=['waypoint', 'relative', 'areaName'])

		with _sm_try_to_reach_3:
			# x:34 y:40
			OperatableStateMachine.add('Set step Join Area',
										Set_a_step(step=2),
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Off})

			# x:30 y:145
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(Action_MoveSM, 'Try to reach/Action_Move'),
										transitions={'finished': 'Say reached', 'failed': 'Say not reached'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'waypoint', 'relative': 'relative'})

			# x:46 y:307
			OperatableStateMachine.add('Say reached',
										SaraSayKey(Format=lambda x: "I'm here.", emotion=1, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'areaName'})

			# x:198 y:295
			OperatableStateMachine.add('Say not reached',
										SaraSayKey(Format=lambda x: "I have not reach the " + x + "!", emotion=1, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'areaName'})


		# x:871 y:59
		_sm_decompose_command_4 = OperatableStateMachine(outcomes=['done'], input_keys=['command'], output_keys=['containers', 'area'])

		with _sm_decompose_command_4:
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
			# x:136 y:46
			OperatableStateMachine.add('Set state Find Area',
										Set_a_step(step=1),
										transitions={'done': 'WonderlandUniqueEnity'},
										autonomy={'done': Autonomy.Off})

			# x:1274 y:95
			OperatableStateMachine.add('Say going',
										SaraSayKey(Format=lambda x: "I'm going to the " + x, emotion=1, block=True),
										transitions={'done': 'found'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'area_name'})

			# x:966 y:71
			OperatableStateMachine.add('Export Waypoint',
										_sm_export_waypoint_2,
										transitions={'done': 'Say going'},
										autonomy={'done': Autonomy.Inherit},
										remapping={'entity': 'entity', 'waipoint': 'waypoint', 'area_name': 'area_name'})

			# x:517 y:67
			OperatableStateMachine.add('WonderlandUniqueEnity',
										self.use_behavior(WonderlandUniqueEnitySM, 'Try to find area/WonderlandUniqueEnity'),
										transitions={'found': 'Export Waypoint', 'not_found': 'Export No Waypoint'},
										autonomy={'found': Autonomy.Inherit, 'not_found': Autonomy.Inherit},
										remapping={'name': 'area_to_search', 'containers': 'containers', 'entity': 'entity'})

			# x:1247 y:295
			OperatableStateMachine.add('Export No Waypoint',
										_sm_export_no_waypoint_1,
										transitions={'done': 'not_found'},
										autonomy={'done': Autonomy.Inherit},
										remapping={'waipoint': 'waypoint', 'area_name': 'area_name'})



		with _state_machine:
			# x:44 y:27
			OperatableStateMachine.add('Set Wrapper Story',
										Set_Story(titre="Move to Location", storyline=["Decompose Command","Find Area","Join Area","Finished"]),
										transitions={'done': 'Decompose Command'},
										autonomy={'done': Autonomy.Off})

			# x:69 y:234
			OperatableStateMachine.add('Try to find area',
										_sm_try_to_find_area_5,
										transitions={'found': 'Try to reach', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Inherit, 'not_found': Autonomy.Inherit},
										remapping={'area_to_search': 'area', 'containers': 'containers', 'area_name': 'area_name', 'waypoint': 'waypoint'})

			# x:62 y:123
			OperatableStateMachine.add('Decompose Command',
										_sm_decompose_command_4,
										transitions={'done': 'Try to find area'},
										autonomy={'done': Autonomy.Inherit},
										remapping={'command': 'Action', 'containers': 'containers', 'area': 'area'})

			# x:325 y:306
			OperatableStateMachine.add('Set Finished',
										Set_a_step(step=3),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:76 y:355
			OperatableStateMachine.add('Try to reach',
										_sm_try_to_reach_3,
										transitions={'finished': 'Set Finished', 'failed': 'failed', 'critical_fail': 'critical_fail'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'waypoint': 'waypoint', 'relative': 'relative', 'areaName': 'area_name'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
