#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_actionwrapper_follow')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.story import Set_Story
from sara_flexbe_states.set_a_step import Set_a_step
from sara_flexbe_states.WonderlandGetEntityVerbal import WonderlandGetEntityVerbal
from sara_flexbe_states.SetKey import SetKey
from flexbe_states.calculation_state import CalculationState
from flexbe_states.flexible_check_condition_state import FlexibleCheckConditionState
from flexbe_states.log_key_state import LogKeyState
from flexbe_states.flexible_calculation_state import FlexibleCalculationState
from flexbe_states.check_condition_state import CheckConditionState
from sara_flexbe_states.sara_say_key import SaraSayKey
from sara_flexbe_states.sara_say import SaraSay
from behavior_action_move.action_move_sm import Action_MoveSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on 22/05/2018
@author: Lucas Maurice
'''
class ActionWrapper_FollowSM(Behavior):
	'''
	action wrapper pour follow
	'''


	def __init__(self):
		super(ActionWrapper_FollowSM, self).__init__()
		self.name = 'ActionWrapper_Follow'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(Action_MoveSM, 'Action_Move')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
        
        # [/MANUAL_INIT]

		# Behavior comments:

		# O 1262 27 
		# Follow|n1- person|n2- area where the person is|n3- path (unused)

		# O 1260 94 
		# Story|n0- Decompose Command|n1- Find Area|n2- Join Area|n3- Find Person|n4- Follow Person|n5- END



	def create(self):
		# x:470 y:280, x:618 y:290
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'critical_fail'], input_keys=['Action'])
		_state_machine.userdata.Action = ["Follow", "rachel", "bedroom", ""]
		_state_machine.userdata.relative = False

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

		# x:30 y:458
		_sm_export_waypoint_0 = OperatableStateMachine(outcomes=['done'], input_keys=['entities'], output_keys=['waipoint', 'area_name'])

		with _sm_export_waypoint_0:
			# x:30 y:56
			OperatableStateMachine.add('Extract Wayppoint',
										CalculationState(calculation=lambda x: x.waypoint),
										transitions={'done': 'Extract Name'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'entities', 'output_value': 'waipoint'})

			# x:245 y:40
			OperatableStateMachine.add('LogWaypoint',
										LogKeyState(text="Will go to waypoint:\n{}", severity=Logger.REPORT_HINT),
										transitions={'done': 'LogName'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'waipoint'})

			# x:40 y:133
			OperatableStateMachine.add('Extract Name',
										CalculationState(calculation=lambda x: x.name),
										transitions={'done': 'LogWaypoint'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'entities', 'output_value': 'area_name'})

			# x:242 y:136
			OperatableStateMachine.add('LogName',
										LogKeyState(text="(Area name: {})", severity=Logger.REPORT_HINT),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'area_name'})


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


		# x:77 y:738
		_sm_list_areas_2 = OperatableStateMachine(outcomes=['done'], input_keys=['entities'], output_keys=['sentence'])

		with _sm_list_areas_2:
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

			# x:467 y:165
			OperatableStateMachine.add('log entity name',
										LogKeyState(text="Present Entity: {}", severity=Logger.REPORT_HINT),
										transitions={'done': 'check first'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'areaName'})

			# x:270 y:163
			OperatableStateMachine.add('getIndexEntity',
										FlexibleCalculationState(calculation=lambda x: x[0].entities[x[1]].name, input_keys=['entities','iLoop']),
										transitions={'done': 'log entity name'},
										autonomy={'done': Autonomy.Off},
										remapping={'entities': 'entities', 'iLoop': 'iLoop', 'output_value': 'areaName'})

			# x:654 y:169
			OperatableStateMachine.add('check first',
										CheckConditionState(predicate=lambda x: x == 0),
										transitions={'true': 'generate room', 'false': 'generate and room'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'iLoop'})

			# x:52 y:235
			OperatableStateMachine.add('InitSentence',
										SetKey(Value=""),
										transitions={'done': 'CheckEndLoop'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'sentence'})

			# x:647 y:455
			OperatableStateMachine.add('ConcatSentence',
										FlexibleCalculationState(calculation=lambda x: str(x[0]) + str(x[1]), input_keys=['first', 'second']),
										transitions={'done': 'incrementIndex'},
										autonomy={'done': Autonomy.Off},
										remapping={'first': 'sentence', 'second': 'areaName', 'output_value': 'sentence'})

			# x:589 y:326
			OperatableStateMachine.add('generate room',
										CalculationState(calculation=lambda x: "The " + x),
										transitions={'done': 'ConcatSentence'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'areaName', 'output_value': 'areaName'})

			# x:746 y:342
			OperatableStateMachine.add('generate and room',
										CalculationState(calculation=lambda x: "And the " + x),
										transitions={'done': 'ConcatSentence'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'areaName', 'output_value': 'areaName'})


		# x:1007 y:466
		_sm_decomposecommand_3 = OperatableStateMachine(outcomes=['done'], input_keys=['command'], output_keys=['person', 'area'])

		with _sm_decomposecommand_3:
			# x:209 y:42
			OperatableStateMachine.add('Set State Command',
										Set_a_step(step=0),
										transitions={'done': 'getPerson'},
										autonomy={'done': Autonomy.Off})

			# x:424 y:227
			OperatableStateMachine.add('getArea',
										CalculationState(calculation=lambda x: x[2]),
										transitions={'done': 'logPerson'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'command', 'output_value': 'area'})

			# x:645 y:227
			OperatableStateMachine.add('logPerson',
										LogKeyState(text="Will find {}", severity=Logger.REPORT_HINT),
										transitions={'done': 'logArea'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'person'})

			# x:645 y:327
			OperatableStateMachine.add('logArea',
										LogKeyState(text="In {}", severity=Logger.REPORT_HINT),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'area'})

			# x:423 y:114
			OperatableStateMachine.add('getPerson',
										CalculationState(calculation=lambda x: x[1]),
										transitions={'done': 'getArea'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'command', 'output_value': 'person'})


		# x:1620 y:109, x:1648 y:375
		_sm_try_to_find_area_4 = OperatableStateMachine(outcomes=['found', 'not_found'], input_keys=['area_to_search'], output_keys=['area_name', 'waypoint'])

		with _sm_try_to_find_area_4:
			# x:49 y:40
			OperatableStateMachine.add('Set state Find Area',
										Set_a_step(step=1),
										transitions={'done': 'noneKey'},
										autonomy={'done': Autonomy.Off})

			# x:152 y:219
			OperatableStateMachine.add('GetEntityLocation',
										WonderlandGetEntityVerbal(),
										transitions={'one': 'Export Waypoint', 'multiple': 'List areas', 'none': 'Say No Area', 'error': 'Say Error'},
										autonomy={'one': Autonomy.Off, 'multiple': Autonomy.Off, 'none': Autonomy.Off, 'error': Autonomy.Off},
										remapping={'name': 'area_to_search', 'containers': 'none_key', 'entities': 'entities'})

			# x:431 y:200
			OperatableStateMachine.add('List areas',
										_sm_list_areas_2,
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
										_sm_export_no_waypoint_1,
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
										_sm_export_waypoint_0,
										transitions={'done': 'Say going'},
										autonomy={'done': Autonomy.Inherit},
										remapping={'entities': 'entities', 'waipoint': 'waypoint', 'area_name': 'area_name'})

			# x:163 y:133
			OperatableStateMachine.add('noneKey',
										SetKey(Value=None),
										transitions={'done': 'GetEntityLocation'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'none_key'})



		with _state_machine:
			# x:44 y:27
			OperatableStateMachine.add('Set Wrapper Story',
										Set_Story(titre="Follow Person", storyline=["Decompose Command","Find Area","Join Area","Find Person","Follow Person", "Finished"]),
										transitions={'done': 'DecomposeCommand'},
										autonomy={'done': Autonomy.Off})

			# x:39 y:330
			OperatableStateMachine.add('Set step Join Area',
										Set_a_step(step=2),
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Off})

			# x:35 y:224
			OperatableStateMachine.add('Try_to_find_area',
										_sm_try_to_find_area_4,
										transitions={'found': 'Set step Join Area', 'not_found': 'Set Finished'},
										autonomy={'found': Autonomy.Inherit, 'not_found': Autonomy.Inherit},
										remapping={'area_to_search': 'area', 'area_name': 'area_name', 'waypoint': 'waypoint'})

			# x:30 y:117
			OperatableStateMachine.add('DecomposeCommand',
										_sm_decomposecommand_3,
										transitions={'done': 'Try_to_find_area'},
										autonomy={'done': Autonomy.Inherit},
										remapping={'command': 'Action', 'person': 'person', 'area': 'area'})

			# x:325 y:269
			OperatableStateMachine.add('Set Finished',
										Set_a_step(step=5),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:33 y:420
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(Action_MoveSM, 'Action_Move'),
										transitions={'finished': 'Set Finished', 'failed': 'Set Finished'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'waypoint', 'relative': 'relative'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
