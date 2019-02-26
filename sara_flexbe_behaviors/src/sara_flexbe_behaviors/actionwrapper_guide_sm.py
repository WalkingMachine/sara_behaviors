#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.GetRosParam import GetRosParam
from sara_flexbe_states.set_a_step import Set_a_step
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.SetKey import SetKey
from flexbe_states.flexible_calculation_state import FlexibleCalculationState
from flexbe_states.flexible_check_condition_state import FlexibleCheckConditionState
from flexbe_states.log_key_state import LogKeyState
from sara_flexbe_behaviors.action_move_sm import Action_MoveSM as sara_flexbe_behaviors__Action_MoveSM
from flexbe_states.wait_state import WaitState
from sara_flexbe_states.sara_set_head_angle import SaraSetHeadAngle
from sara_flexbe_behaviors.action_turn_sm import action_turnSM as sara_flexbe_behaviors__action_turnSM
from sara_flexbe_states.Get_Entity_By_ID import GetEntityByID
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_behaviors.wonderlanduniqueenity_sm import WonderlandUniqueEnitySM as sara_flexbe_behaviors__WonderlandUniqueEnitySM
from sara_flexbe_states.WonderlandGetEntityVerbal import WonderlandGetEntityVerbal
from sara_flexbe_behaviors.action_point_at_sm import Action_point_atSM as sara_flexbe_behaviors__Action_point_atSM
from sara_flexbe_states.SetRosParam import SetRosParam
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on 05/06/2018
@author: Lucas Maurice
'''
class ActionWrapper_GuideSM(Behavior):
	'''
	action wrapper pour indiquer la route a un operateur.
	'''


	def __init__(self):
		super(ActionWrapper_GuideSM, self).__init__()
		self.name = 'ActionWrapper_Guide'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'Try to reach/Container/navigate to the point/Action_Move')
		self.add_behavior(sara_flexbe_behaviors__action_turnSM, 'Try to reach/check person behind/move head and base/turn around/action_turn')
		self.add_behavior(sara_flexbe_behaviors__action_turnSM, 'Try to reach/check person behind/move head and base/turn around/action_turn_2')
		self.add_behavior(sara_flexbe_behaviors__WonderlandUniqueEnitySM, 'Try to find area/WonderlandUniqueEnity')
		self.add_behavior(sara_flexbe_behaviors__action_turnSM, 'operator is still there/Move head and base end /move head and base at the end/action_turn')
		self.add_behavior(sara_flexbe_behaviors__action_turnSM, 'operator is still there/Move head and base end /move head and base at the end/action_turn_2')
		self.add_behavior(sara_flexbe_behaviors__Action_point_atSM, 'Action_point_at')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
        
        # [/MANUAL_INIT]

		# Behavior comments:

		# O 1262 27 
		# Move|n1- Location|n2- Location Container|n3- Location Container

		# O 1260 94 
		# Story|n0- Decompose Command|n1- Find Area|n2- Join Area|n3- END

		# ! 174 65 /Try to reach
		# Je vous doit des donuts!



	def create(self):
		# x:1023 y:473, x:791 y:291, x:797 y:103
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'critical_fail'], input_keys=['Action'])
		_state_machine.userdata.Action = ["Guide",'table', 'kitchen']
		_state_machine.userdata.relative = False

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

		# x:30 y:458
		_sm_groupwait_0 = OperatableStateMachine(outcomes=['end'])

		with _sm_groupwait_0:
			# x:30 y:40
			OperatableStateMachine.add('waitwait',
										WaitState(wait_time=20),
										transitions={'done': 'end'},
										autonomy={'done': Autonomy.Off})


		# x:534 y:319
		_sm_move_head_and_base_at_the_end_1 = OperatableStateMachine(outcomes=['failed'])

		with _sm_move_head_and_base_at_the_end_1:
			# x:52 y:31
			OperatableStateMachine.add('setkeyorientation',
										SetKey(Value=1.5),
										transitions={'done': 'action_turn'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'rotation'})

			# x:51 y:114
			OperatableStateMachine.add('action_turn',
										self.use_behavior(sara_flexbe_behaviors__action_turnSM, 'operator is still there/Move head and base end /move head and base at the end/action_turn'),
										transitions={'finished': 'turn right head', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'rotation': 'rotation'})

			# x:48 y:272
			OperatableStateMachine.add('wait while head turn',
										WaitState(wait_time=4),
										transitions={'done': 'action_turn_2'},
										autonomy={'done': Autonomy.Off})

			# x:47 y:199
			OperatableStateMachine.add('turn right head',
										SaraSetHeadAngle(pitch=0, yaw=1.57),
										transitions={'done': 'wait while head turn'},
										autonomy={'done': Autonomy.Off})

			# x:45 y:348
			OperatableStateMachine.add('action_turn_2',
										self.use_behavior(sara_flexbe_behaviors__action_turnSM, 'operator is still there/Move head and base end /move head and base at the end/action_turn_2'),
										transitions={'finished': 'left to rigth', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'rotation': 'rotation'})

			# x:43 y:592
			OperatableStateMachine.add('left to rigth',
										SaraSetHeadAngle(pitch=0, yaw=-1.57),
										transitions={'done': 'waitwait1'},
										autonomy={'done': Autonomy.Off})

			# x:420 y:602
			OperatableStateMachine.add('right to left',
										SaraSetHeadAngle(pitch=0, yaw=1.57),
										transitions={'done': 'waitwait2'},
										autonomy={'done': Autonomy.Off})

			# x:266 y:541
			OperatableStateMachine.add('waitwait1',
										WaitState(wait_time=8),
										transitions={'done': 'right to left'},
										autonomy={'done': Autonomy.Off})

			# x:236 y:674
			OperatableStateMachine.add('waitwait2',
										WaitState(wait_time=8),
										transitions={'done': 'left to rigth'},
										autonomy={'done': Autonomy.Off})


		# x:231 y:538
		_sm_find_a_human_2 = OperatableStateMachine(outcomes=['finished'], input_keys=['ID'])

		with _sm_find_a_human_2:
			# x:78 y:275
			OperatableStateMachine.add('find the human',
										GetEntityByID(),
										transitions={'found': 'finished', 'not_found': 'find the human'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ID': 'ID', 'Entity': 'Entity'})


		# x:415 y:99, x:318 y:246, x:442 y:295
		_sm_move_head_and_base_end__3 = ConcurrencyContainer(outcomes=['failed'], conditions=[
										('failed', [('move head and base at the end', 'failed')]),
										('failed', [('Groupwait', 'end')])
										])

		with _sm_move_head_and_base_end__3:
			# x:132 y:57
			OperatableStateMachine.add('move head and base at the end',
										_sm_move_head_and_base_at_the_end_1,
										transitions={'failed': 'failed'},
										autonomy={'failed': Autonomy.Inherit})

			# x:121 y:218
			OperatableStateMachine.add('Groupwait',
										_sm_groupwait_0,
										transitions={'end': 'failed'},
										autonomy={'end': Autonomy.Inherit})


		# x:67 y:227
		_sm_export_no_waypoint_4 = OperatableStateMachine(outcomes=['done'], output_keys=['waipoint', 'area_name'])

		with _sm_export_no_waypoint_4:
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
		_sm_export_waypoint_5 = OperatableStateMachine(outcomes=['done'], input_keys=['entity'], output_keys=['waipoint', 'area_name'])

		with _sm_export_waypoint_5:
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


		# x:379 y:221
		_sm_wait_to_compte_6 = OperatableStateMachine(outcomes=['finished'])

		with _sm_wait_to_compte_6:
			# x:77 y:195
			OperatableStateMachine.add('one more wait',
										WaitState(wait_time=60),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		# x:535 y:314
		_sm_turn_around_7 = OperatableStateMachine(outcomes=['failed'])

		with _sm_turn_around_7:
			# x:47 y:45
			OperatableStateMachine.add('set orientation',
										SetKey(Value=1.57),
										transitions={'done': 'action_turn'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'rotation'})

			# x:42 y:213
			OperatableStateMachine.add('move head',
										SaraSetHeadAngle(pitch=0, yaw=1.57),
										transitions={'done': 'waitwait'},
										autonomy={'done': Autonomy.Off})

			# x:53 y:294
			OperatableStateMachine.add('waitwait',
										WaitState(wait_time=10),
										transitions={'done': 'action_turn_2'},
										autonomy={'done': Autonomy.Off})

			# x:33 y:122
			OperatableStateMachine.add('action_turn',
										self.use_behavior(sara_flexbe_behaviors__action_turnSM, 'Try to reach/check person behind/move head and base/turn around/action_turn'),
										transitions={'finished': 'move head', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'rotation': 'rotation'})

			# x:31 y:434
			OperatableStateMachine.add('action_turn_2',
										self.use_behavior(sara_flexbe_behaviors__action_turnSM, 'Try to reach/check person behind/move head and base/turn around/action_turn_2'),
										transitions={'finished': 'head left right', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'rotation': 'rotation'})

			# x:35 y:595
			OperatableStateMachine.add('head left right',
										SaraSetHeadAngle(pitch=0, yaw=1.57),
										transitions={'done': 'wait turn head'},
										autonomy={'done': Autonomy.Off})

			# x:308 y:537
			OperatableStateMachine.add('wait turn head',
										WaitState(wait_time=10),
										transitions={'done': 'head right left'},
										autonomy={'done': Autonomy.Off})

			# x:495 y:604
			OperatableStateMachine.add('head right left',
										SaraSetHeadAngle(pitch=0, yaw=-1.57),
										transitions={'done': 'wait wait wait'},
										autonomy={'done': Autonomy.Off})

			# x:271 y:711
			OperatableStateMachine.add('wait wait wait',
										WaitState(wait_time=10),
										transitions={'done': 'head left right'},
										autonomy={'done': Autonomy.Off})


		# x:845 y:395
		_sm_find_human_8 = OperatableStateMachine(outcomes=['finished'], input_keys=['ID'])

		with _sm_find_human_8:
			# x:223 y:137
			OperatableStateMachine.add('find person',
										GetEntityByID(),
										transitions={'found': 'finished', 'not_found': 'find person'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ID': 'ID', 'Entity': 'Entity'})


		# x:549 y:135, x:555 y:269, x:230 y:458
		_sm_move_head_and_base_9 = ConcurrencyContainer(outcomes=['failed'], conditions=[
										('failed', [('turn around', 'failed')]),
										('failed', [('wait to compte', 'finished')])
										])

		with _sm_move_head_and_base_9:
			# x:268 y:77
			OperatableStateMachine.add('turn around',
										_sm_turn_around_7,
										transitions={'failed': 'failed'},
										autonomy={'failed': Autonomy.Inherit})

			# x:263 y:246
			OperatableStateMachine.add('wait to compte',
										_sm_wait_to_compte_6,
										transitions={'finished': 'failed'},
										autonomy={'finished': Autonomy.Inherit})


		# x:493 y:206
		_sm_container_10 = OperatableStateMachine(outcomes=['check'])

		with _sm_container_10:
			# x:230 y:160
			OperatableStateMachine.add('wait long',
										WaitState(wait_time=40),
										transitions={'done': 'check'},
										autonomy={'done': Autonomy.Off})


		# x:30 y:458, x:706 y:447
		_sm_navigate_to_the_point_11 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['pose'])

		with _sm_navigate_to_the_point_11:
			# x:174 y:122
			OperatableStateMachine.add('set relative',
										SetKey(Value=False),
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'relative'})

			# x:347 y:191
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'Try to reach/Container/navigate to the point/Action_Move'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'pose', 'relative': 'relative'})


		# x:728 y:335, x:792 y:103, x:738 y:249, x:724 y:448
		_sm_check_person_behind_12 = ConcurrencyContainer(outcomes=['finished', 'failed'], input_keys=['ID'], conditions=[
										('failed', [('move head and base', 'failed')]),
										('finished', [('find human', 'finished')])
										])

		with _sm_check_person_behind_12:
			# x:250 y:72
			OperatableStateMachine.add('move head and base',
										_sm_move_head_and_base_9,
										transitions={'failed': 'failed'},
										autonomy={'failed': Autonomy.Inherit})

			# x:261 y:238
			OperatableStateMachine.add('find human',
										_sm_find_human_8,
										transitions={'finished': 'finished'},
										autonomy={'finished': Autonomy.Inherit},
										remapping={'ID': 'ID'})


		# x:635 y:61, x:634 y:159, x:597 y:300, x:330 y:458, x:430 y:458, x:530 y:458
		_sm_container_13 = ConcurrencyContainer(outcomes=['finished', 'failed', 'check'], input_keys=['waypoint'], conditions=[
										('check', [('Container', 'check')]),
										('finished', [('navigate to the point', 'finished')]),
										('failed', [('navigate to the point', 'failed')])
										])

		with _sm_container_13:
			# x:315 y:51
			OperatableStateMachine.add('navigate to the point',
										_sm_navigate_to_the_point_11,
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'waypoint'})

			# x:322 y:257
			OperatableStateMachine.add('Container',
										_sm_container_10,
										transitions={'check': 'check'},
										autonomy={'check': Autonomy.Inherit})


		# x:98 y:451
		_sm_get_area_containers_14 = OperatableStateMachine(outcomes=['done'], input_keys=['command'], output_keys=['containers'])

		with _sm_get_area_containers_14:
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


		# x:626 y:228, x:607 y:71, x:230 y:458, x:330 y:458
		_sm_operator_is_still_there_15 = ConcurrencyContainer(outcomes=['finished', 'failed'], input_keys=['ID'], conditions=[
										('finished', [('find a human', 'finished')]),
										('failed', [('Move head and base end ', 'failed')])
										])

		with _sm_operator_is_still_there_15:
			# x:207 y:54
			OperatableStateMachine.add('Move head and base end ',
										_sm_move_head_and_base_end__3,
										transitions={'failed': 'failed'},
										autonomy={'failed': Autonomy.Inherit})

			# x:222 y:190
			OperatableStateMachine.add('find a human',
										_sm_find_a_human_2,
										transitions={'finished': 'finished'},
										autonomy={'finished': Autonomy.Inherit},
										remapping={'ID': 'ID'})


		# x:1620 y:109, x:1648 y:375
		_sm_try_to_find_area_16 = OperatableStateMachine(outcomes=['found', 'not_found'], input_keys=['area_to_search', 'containers'], output_keys=['area_name', 'waypoint'])

		with _sm_try_to_find_area_16:
			# x:517 y:67
			OperatableStateMachine.add('WonderlandUniqueEnity',
										self.use_behavior(sara_flexbe_behaviors__WonderlandUniqueEnitySM, 'Try to find area/WonderlandUniqueEnity'),
										transitions={'found': 'Export Waypoint', 'not_found': 'Export No Waypoint'},
										autonomy={'found': Autonomy.Inherit, 'not_found': Autonomy.Inherit},
										remapping={'name': 'area_to_search', 'containers': 'containers', 'entity': 'entity'})

			# x:966 y:71
			OperatableStateMachine.add('Export Waypoint',
										_sm_export_waypoint_5,
										transitions={'done': 'say_going'},
										autonomy={'done': Autonomy.Inherit},
										remapping={'entity': 'entity', 'waipoint': 'waypoint', 'area_name': 'area_name'})

			# x:1247 y:295
			OperatableStateMachine.add('Export No Waypoint',
										_sm_export_no_waypoint_4,
										transitions={'done': 'not_found'},
										autonomy={'done': Autonomy.Inherit},
										remapping={'waipoint': 'waypoint', 'area_name': 'area_name'})

			# x:1273 y:106
			OperatableStateMachine.add('say_going',
										SaraSay(sentence=lambda x: "I'm going to the " + x, input_keys=[], emotion=0, block=True),
										transitions={'done': 'found'},
										autonomy={'done': Autonomy.Off})


		# x:323 y:632, x:638 y:631
		_sm_try_to_reach_17 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['waypoint', 'relative', 'areaName', 'ID'])

		with _sm_try_to_reach_17:
			# x:252 y:161
			OperatableStateMachine.add('Container',
										_sm_container_13,
										transitions={'finished': 'say_reached', 'failed': 'Say_not_reached', 'check': 'say check'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'check': Autonomy.Inherit},
										remapping={'waypoint': 'waypoint'})

			# x:581 y:163
			OperatableStateMachine.add('check person behind',
										_sm_check_person_behind_12,
										transitions={'finished': 'say found', 'failed': 'say lost'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'ID': 'ID'})

			# x:706 y:484
			OperatableStateMachine.add('say lost',
										SaraSay(sentence="Oh no! I lost my operator!", input_keys=[], emotion=1, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:445 y:69
			OperatableStateMachine.add('say check',
										SaraSay(sentence="I check if my operator is still there", input_keys=[], emotion=1, block=True),
										transitions={'done': 'check person behind'},
										autonomy={'done': Autonomy.Off})

			# x:443 y:187
			OperatableStateMachine.add('say found',
										SaraSay(sentence="Great. You are still there.", input_keys=[], emotion=1, block=True),
										transitions={'done': 'Container'},
										autonomy={'done': Autonomy.Off})

			# x:463 y:398
			OperatableStateMachine.add('Say_not_reached',
										SaraSay(sentence=lambda x: "I have not reach the " + x + "!", input_keys=[], emotion=1, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:61 y:366
			OperatableStateMachine.add('say_reached',
										SaraSay(sentence=lambda x: "I have reach the " + x + "!", input_keys=[], emotion=1, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		# x:871 y:59
		_sm_decompose_command_18 = OperatableStateMachine(outcomes=['done'], input_keys=['command'], output_keys=['containers', 'area'])

		with _sm_decompose_command_18:
			# x:163 y:34
			OperatableStateMachine.add('Set State Command',
										Set_a_step(step=0),
										transitions={'done': 'Get area name'},
										autonomy={'done': Autonomy.Off})

			# x:387 y:58
			OperatableStateMachine.add('Get area name',
										CalculationState(calculation=lambda x: x[1]),
										transitions={'done': 'Get area containers'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'command', 'output_value': 'area'})

			# x:597 y:94
			OperatableStateMachine.add('Get area containers',
										_sm_get_area_containers_14,
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Inherit},
										remapping={'command': 'command', 'containers': 'containers'})



		with _state_machine:
			# x:54 y:24
			OperatableStateMachine.add('Get Person Id',
										GetRosParam(ParamName="behavior/FoundPerson/Id"),
										transitions={'done': 'GetPerson', 'failed': 'Cant Find Person'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'Value': 'ID'})

			# x:19 y:152
			OperatableStateMachine.add('Decompose Command',
										_sm_decompose_command_18,
										transitions={'done': 'Try to find area'},
										autonomy={'done': Autonomy.Inherit},
										remapping={'command': 'Action', 'containers': 'containers', 'area': 'area'})

			# x:43 y:358
			OperatableStateMachine.add('Try to reach',
										_sm_try_to_reach_17,
										transitions={'finished': 'operator is still there', 'failed': 'cause2'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'waypoint': 'waypoint', 'relative': 'relative', 'areaName': 'area_name', 'ID': 'ID'})

			# x:360 y:109
			OperatableStateMachine.add('Cant Find Person',
										SaraSay(sentence="I can't find a person.", input_keys=[], emotion=1, block=True),
										transitions={'done': 'cause1'},
										autonomy={'done': Autonomy.Off})

			# x:52 y:82
			OperatableStateMachine.add('GetPerson',
										GetEntityByID(),
										transitions={'found': 'Decompose Command', 'not_found': 'Cant Find Person'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ID': 'ID', 'Entity': 'Entity'})

			# x:36 y:219
			OperatableStateMachine.add('Try to find area',
										_sm_try_to_find_area_16,
										transitions={'found': 'sayfollowme', 'not_found': 'Cant Find Person'},
										autonomy={'found': Autonomy.Inherit, 'not_found': Autonomy.Inherit},
										remapping={'area_to_search': 'area', 'containers': 'containers', 'area_name': 'area_name', 'waypoint': 'waypoint'})

			# x:27 y:438
			OperatableStateMachine.add('operator is still there',
										_sm_operator_is_still_there_15,
										transitions={'finished': 'getentitybyID', 'failed': 'say lost operator'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'ID': 'ID'})

			# x:347 y:370
			OperatableStateMachine.add('say lost operator',
										SaraSay(sentence="I have reach my goal but I lost the person I was guiding.", input_keys=[], emotion=1, block=True),
										transitions={'done': 'cause3'},
										autonomy={'done': Autonomy.Off})

			# x:49 y:291
			OperatableStateMachine.add('sayfollowme',
										SaraSay(sentence="Follow me please.", input_keys=[], emotion=1, block=True),
										transitions={'done': 'Try to reach'},
										autonomy={'done': Autonomy.Off})

			# x:808 y:451
			OperatableStateMachine.add('head to middle',
										SaraSetHeadAngle(pitch=0, yaw=0),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:48 y:525
			OperatableStateMachine.add('getentitybyID',
										GetEntityByID(),
										transitions={'found': 'get entity to point', 'not_found': 'say_reach_the_entity'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ID': 'ID', 'Entity': 'Entity'})

			# x:249 y:562
			OperatableStateMachine.add('get entity to point',
										WonderlandGetEntityVerbal(),
										transitions={'one': 'find the point', 'multiple': 'say_reach_the_entity', 'none': 'say_reach_the_entity', 'error': 'say_reach_the_entity'},
										autonomy={'one': Autonomy.Off, 'multiple': Autonomy.Off, 'none': Autonomy.Off, 'error': Autonomy.Off},
										remapping={'name': 'area_name', 'containers': 'containers', 'entities': 'entities'})

			# x:708 y:529
			OperatableStateMachine.add('Action_point_at',
										self.use_behavior(sara_flexbe_behaviors__Action_point_atSM, 'Action_point_at'),
										transitions={'finished': 'say_reach_the_entity', 'failed': 'say_reach_the_entity'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'targetPoint': 'targetPoint'})

			# x:539 y:558
			OperatableStateMachine.add('find the point',
										CalculationState(calculation=lambda x: x.position),
										transitions={'done': 'Action_point_at'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'entities', 'output_value': 'targetPoint'})

			# x:547 y:121
			OperatableStateMachine.add('cause1',
										SetKey(Value="I didn't find any persone"),
										transitions={'done': 'setrosparamfail'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Key'})

			# x:507 y:220
			OperatableStateMachine.add('cause2',
										SetKey(Value="I did not reach the area"),
										transitions={'done': 'setrosparamfail'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Key'})

			# x:559 y:337
			OperatableStateMachine.add('cause3',
										SetKey(Value="I lost the person I was guiding."),
										transitions={'done': 'setrosparamfail'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Key'})

			# x:656 y:250
			OperatableStateMachine.add('setrosparamfail',
										SetRosParam(ParamName="behavior/GPSR/CauseOfFailure"),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off},
										remapping={'Value': 'Key'})

			# x:523 y:462
			OperatableStateMachine.add('say_reach_the_entity',
										SaraSay(sentence=lambda x: "Here is the "+x, input_keys=[], emotion=1, block=True),
										transitions={'done': 'head to middle'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
