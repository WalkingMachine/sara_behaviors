#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_actionwrapper_guide')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.GetRosParam import GetRosParam
from sara_flexbe_states.set_a_step import Set_a_step
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.SetKey import SetKey
from flexbe_states.flexible_calculation_state import FlexibleCalculationState
from flexbe_states.flexible_check_condition_state import FlexibleCheckConditionState
from flexbe_states.log_key_state import LogKeyState
from behavior_action_move.action_move_sm import Action_MoveSM
from sara_flexbe_states.sara_say_key import SaraSayKey
from flexbe_states.wait_state import WaitState
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.Get_Entity_By_ID import GetEntityByID
from behavior_wonderlanduniqueenity.wonderlanduniqueenity_sm import WonderlandUniqueEnitySM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on 05/06/2018
@author: Lucas Maurice
'''
class ActionWrapper_GuideSM(Behavior):
	'''
	action wrapper pour indiquer la route à un opérateur.
	'''


	def __init__(self):
		super(ActionWrapper_GuideSM, self).__init__()
		self.name = 'ActionWrapper_Guide'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(Action_MoveSM, 'Try to reach/Action_Move')
		self.add_behavior(WonderlandUniqueEnitySM, 'Try to find area/WonderlandUniqueEnity')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
        
        # [/MANUAL_INIT]

		# Behavior comments:

		# O 1262 27 
		# Move|n1- Location|n2- Location Container|n3- Location Container

		# O 1260 94 
		# Story|n0- Decompose Command|n1- Find Area|n2- Join Area|n3- END



	def create(self):
		# x:587 y:780, x:781 y:419, x:951 y:679
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'critical_fail'], input_keys=['Action'])
		_state_machine.userdata.Action = ["Move",'table','kitchen']
		_state_machine.userdata.relative = False

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

		# x:67 y:227
		_sm_export_no_waypoint_0 = OperatableStateMachine(outcomes=['done'], output_keys=['waipoint', 'area_name'])

		with _sm_export_no_waypoint_0:
			# x:30 y:40
			OperatableStateMachine.add('noWaypoint',
										SetKey(Value=None),
										transitions={'done': 'NoName'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'waipoint'})

			# x:43 y:129
			OperatableStateMachine.add('NoName',
										SetKey(Value=None),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'area_name'})


		# x:30 y:458
		_sm_export_waypoint_1 = OperatableStateMachine(outcomes=['done'], input_keys=['entity'], output_keys=['waipoint', 'area_name'])

		with _sm_export_waypoint_1:
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


		# x:30 y:458, x:130 y:458
		_sm_container_2 = PriorityContainer(outcomes=['finished', 'failed'])

		with _sm_container_2:
			# x:156 y:176
			OperatableStateMachine.add('WaitState',
										WaitState(wait_time=10),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		# x:98 y:451
		_sm_get_area_containers_3 = OperatableStateMachine(outcomes=['done'], input_keys=['command'], output_keys=['containers'])

		with _sm_get_area_containers_3:
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


		# x:1620 y:109, x:1648 y:375
		_sm_try_to_find_area_4 = OperatableStateMachine(outcomes=['found', 'not_found'], input_keys=['area_to_search', 'containers'], output_keys=['area_name', 'waypoint'])

		with _sm_try_to_find_area_4:
			# x:517 y:67
			OperatableStateMachine.add('WonderlandUniqueEnity',
										self.use_behavior(WonderlandUniqueEnitySM, 'Try to find area/WonderlandUniqueEnity'),
										transitions={'found': 'Export Waypoint', 'not_found': 'Export No Waypoint'},
										autonomy={'found': Autonomy.Inherit, 'not_found': Autonomy.Inherit},
										remapping={'name': 'area_to_search', 'containers': 'containers', 'entity': 'entity'})

			# x:966 y:71
			OperatableStateMachine.add('Export Waypoint',
										_sm_export_waypoint_1,
										transitions={'done': 'Say going'},
										autonomy={'done': Autonomy.Inherit},
										remapping={'entity': 'entity', 'waipoint': 'waypoint', 'area_name': 'area_name'})

			# x:1247 y:295
			OperatableStateMachine.add('Export No Waypoint',
										_sm_export_no_waypoint_0,
										transitions={'done': 'not_found'},
										autonomy={'done': Autonomy.Inherit},
										remapping={'waipoint': 'waypoint', 'area_name': 'area_name'})

			# x:1274 y:95
			OperatableStateMachine.add('Say going',
										SaraSayKey(Format=lambda x: "I'm going to the " + x, emotion=1, block=True),
										transitions={'done': 'found'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'area_name'})


		# x:323 y:632, x:370 y:631
		_sm_try_to_reach_5 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['waypoint', 'relative', 'areaName'])

		with _sm_try_to_reach_5:
			# x:322 y:272
			OperatableStateMachine.add('Container',
										_sm_container_2,
										transitions={'finished': 'Say reached', 'failed': 'Say not reached'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:106 y:453
			OperatableStateMachine.add('Say reached',
										SaraSayKey(Format=lambda x: "I have reach the " + x + "!", emotion=1, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'areaName'})

			# x:516 y:463
			OperatableStateMachine.add('Say not reached',
										SaraSayKey(Format=lambda x: "I have not reach the " + x + "!", emotion=1, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'areaName'})

			# x:287 y:57
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(Action_MoveSM, 'Try to reach/Action_Move'),
										transitions={'finished': 'Action_Move', 'failed': 'Action_Move'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'waypoint', 'relative': 'relative'})


		# x:871 y:59
		_sm_decompose_command_6 = OperatableStateMachine(outcomes=['done'], input_keys=['command'], output_keys=['containers', 'area'])

		with _sm_decompose_command_6:
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
										_sm_get_area_containers_3,
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Inherit},
										remapping={'command': 'command', 'containers': 'containers'})



		with _state_machine:
			# x:88 y:77
			OperatableStateMachine.add('Get Person Id',
										GetRosParam(ParamName="behavior/FoundPerson/Id"),
										transitions={'done': 'GetPerson', 'failed': 'Cant Find Person'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'Value': 'ID'})

			# x:72 y:240
			OperatableStateMachine.add('Decompose Command',
										_sm_decompose_command_6,
										transitions={'done': 'Try to find area'},
										autonomy={'done': Autonomy.Inherit},
										remapping={'command': 'Action', 'containers': 'containers', 'area': 'area'})

			# x:124 y:783
			OperatableStateMachine.add('Set Finished',
										Set_a_step(step=3),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:110 y:415
			OperatableStateMachine.add('Try to reach',
										_sm_try_to_reach_5,
										transitions={'finished': 'Set Finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'waypoint': 'waypoint', 'relative': 'relative', 'areaName': 'area_name'})

			# x:477 y:234
			OperatableStateMachine.add('Cant Find Person',
										SaraSay(sentence="I can't find a person.", emotion=1, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:91 y:159
			OperatableStateMachine.add('GetPerson',
										GetEntityByID(),
										transitions={'found': 'Decompose Command', 'not_found': 'Cant Find Person'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ID': 'ID', 'Entity': 'Entity'})

			# x:103 y:324
			OperatableStateMachine.add('Try to find area',
										_sm_try_to_find_area_4,
										transitions={'found': 'Try to reach', 'not_found': 'Cant Find Person'},
										autonomy={'found': Autonomy.Inherit, 'not_found': Autonomy.Inherit},
										remapping={'area_to_search': 'area', 'containers': 'containers', 'area_name': 'area_name', 'waypoint': 'waypoint'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
