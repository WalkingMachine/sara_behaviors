#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.Get_Entity_By_ID import GetEntityByID
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_behaviors.action_turn_sm import action_turnSM as action_turnSM
from flexbe_states.wait_state import WaitState
from sara_flexbe_states.sara_set_head_angle import SaraSetHeadAngle
from sara_flexbe_states.list_entities_by_name import list_entities_by_name
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_behaviors.action_move_sm import Action_MoveSM as Action_MoveSM
from sara_flexbe_behaviors.action_findperson_sm import Action_findPersonSM as Action_findPersonSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on 05/06/2018
@author: Philippe La Madeleine
'''
class Action_Guide2SM(Behavior):
	'''
	action pour indiquer la route a un operateur.
	'''


	def __init__(self):
		super(Action_Guide2SM, self).__init__()
		self.name = 'Action_Guide2'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(action_turnSM, 'operator is still there/Move head and base end /move head and base at the end/action_turn')
		self.add_behavior(action_turnSM, 'operator is still there/Move head and base end /move head and base at the end/action_turn_2')
		self.add_behavior(Action_MoveSM, 'Try to reach/Container/navigate to the point/Action_Move')
		self.add_behavior(action_turnSM, 'Try to reach/check person behind/move head and base/turn around/action_turn')
		self.add_behavior(action_turnSM, 'Try to reach/check person behind/move head and base/turn around/action_turn_2')
		self.add_behavior(Action_findPersonSM, 'Action_findPerson')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
        
        # [/MANUAL_INIT]

		# Behavior comments:

		# O 1262 27 
		# Move|n1- Location|n2- Location Container|n3- Location Container

		# O 1260 94 
		# Story|n0- Decompose Command|n1- Find Area|n2- Join Area|n3- END



	def create(self):
		# x:666 y:331, x:502 y:199, x:797 y:103
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'critical_fail'], input_keys=['Position', 'ID'])
		_state_machine.userdata.relative = False
		_state_machine.userdata.Position = 0
		_state_machine.userdata.ID = 0
		_state_machine.userdata.className = "person"

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

		# x:379 y:221
		_sm_wait_to_compte_0 = OperatableStateMachine(outcomes=['finished'])

		with _sm_wait_to_compte_0:
			# x:77 y:195
			OperatableStateMachine.add('one more wait',
										WaitState(wait_time=60),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		# x:535 y:314
		_sm_turn_around_1 = OperatableStateMachine(outcomes=['failed'])

		with _sm_turn_around_1:
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
										self.use_behavior(action_turnSM, 'Try to reach/check person behind/move head and base/turn around/action_turn'),
										transitions={'finished': 'move head', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'rotation': 'rotation'})

			# x:31 y:434
			OperatableStateMachine.add('action_turn_2',
										self.use_behavior(action_turnSM, 'Try to reach/check person behind/move head and base/turn around/action_turn_2'),
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

			# x:262 y:652
			OperatableStateMachine.add('wait wait wait',
										WaitState(wait_time=10),
										transitions={'done': 'head left right'},
										autonomy={'done': Autonomy.Off})


		# x:845 y:395
		_sm_find_human_2 = OperatableStateMachine(outcomes=['finished'], input_keys=['ID'])

		with _sm_find_human_2:
			# x:143 y:40
			OperatableStateMachine.add('set name',
										SetKey(Value="person"),
										transitions={'done': 'list'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'name'})

			# x:361 y:53
			OperatableStateMachine.add('list',
										list_entities_by_name(frontality_level=0.5, distance_max=3),
										transitions={'found': 'finished', 'none_found': 'list'},
										autonomy={'found': Autonomy.Off, 'none_found': Autonomy.Off},
										remapping={'name': 'name', 'entity_list': 'entity_list', 'number': 'number'})


		# x:549 y:135, x:555 y:269, x:230 y:458
		_sm_move_head_and_base_3 = ConcurrencyContainer(outcomes=['failed'], conditions=[
										('failed', [('turn around', 'failed')]),
										('failed', [('wait to compte', 'finished')])
										])

		with _sm_move_head_and_base_3:
			# x:268 y:77
			OperatableStateMachine.add('turn around',
										_sm_turn_around_1,
										transitions={'failed': 'failed'},
										autonomy={'failed': Autonomy.Inherit})

			# x:263 y:246
			OperatableStateMachine.add('wait to compte',
										_sm_wait_to_compte_0,
										transitions={'finished': 'failed'},
										autonomy={'finished': Autonomy.Inherit})


		# x:493 y:206
		_sm_container_4 = OperatableStateMachine(outcomes=['check'])

		with _sm_container_4:
			# x:230 y:160
			OperatableStateMachine.add('wait long',
										WaitState(wait_time=40),
										transitions={'done': 'check'},
										autonomy={'done': Autonomy.Off})


		# x:30 y:458, x:706 y:447
		_sm_navigate_to_the_point_5 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['pose'])

		with _sm_navigate_to_the_point_5:
			# x:174 y:122
			OperatableStateMachine.add('set relative',
										SetKey(Value=False),
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'relative'})

			# x:347 y:191
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(Action_MoveSM, 'Try to reach/Container/navigate to the point/Action_Move'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'pose', 'relative': 'relative'})


		# x:728 y:335, x:792 y:103, x:738 y:249, x:724 y:448
		_sm_check_person_behind_6 = ConcurrencyContainer(outcomes=['finished', 'failed'], input_keys=['ID'], conditions=[
										('failed', [('move head and base', 'failed')]),
										('finished', [('find human', 'finished')])
										])

		with _sm_check_person_behind_6:
			# x:250 y:72
			OperatableStateMachine.add('move head and base',
										_sm_move_head_and_base_3,
										transitions={'failed': 'failed'},
										autonomy={'failed': Autonomy.Inherit})

			# x:261 y:238
			OperatableStateMachine.add('find human',
										_sm_find_human_2,
										transitions={'finished': 'finished'},
										autonomy={'finished': Autonomy.Inherit},
										remapping={'ID': 'ID'})


		# x:635 y:61, x:634 y:159, x:597 y:300, x:330 y:458, x:430 y:458, x:530 y:458
		_sm_container_7 = ConcurrencyContainer(outcomes=['finished', 'failed', 'check'], input_keys=['waypoint'], conditions=[
										('check', [('Container', 'check')]),
										('finished', [('navigate to the point', 'finished')]),
										('failed', [('navigate to the point', 'failed')])
										])

		with _sm_container_7:
			# x:315 y:51
			OperatableStateMachine.add('navigate to the point',
										_sm_navigate_to_the_point_5,
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'waypoint'})

			# x:322 y:257
			OperatableStateMachine.add('Container',
										_sm_container_4,
										transitions={'check': 'check'},
										autonomy={'check': Autonomy.Inherit})


		# x:30 y:458
		_sm_groupwait_8 = OperatableStateMachine(outcomes=['end'])

		with _sm_groupwait_8:
			# x:30 y:40
			OperatableStateMachine.add('waitwait',
										WaitState(wait_time=20),
										transitions={'done': 'end'},
										autonomy={'done': Autonomy.Off})


		# x:534 y:319
		_sm_move_head_and_base_at_the_end_9 = OperatableStateMachine(outcomes=['failed'])

		with _sm_move_head_and_base_at_the_end_9:
			# x:52 y:31
			OperatableStateMachine.add('setkeyorientation',
										SetKey(Value=1.5),
										transitions={'done': 'action_turn'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'rotation'})

			# x:51 y:114
			OperatableStateMachine.add('action_turn',
										self.use_behavior(action_turnSM, 'operator is still there/Move head and base end /move head and base at the end/action_turn'),
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
										self.use_behavior(action_turnSM, 'operator is still there/Move head and base end /move head and base at the end/action_turn_2'),
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
		_sm_find_a_human_10 = OperatableStateMachine(outcomes=['finished'], input_keys=['ID'])

		with _sm_find_a_human_10:
			# x:168 y:102
			OperatableStateMachine.add('set name',
										SetKey(Value="person"),
										transitions={'done': 'list'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'name'})

			# x:275 y:203
			OperatableStateMachine.add('list',
										list_entities_by_name(frontality_level=0.5, distance_max=3),
										transitions={'found': 'finished', 'none_found': 'list'},
										autonomy={'found': Autonomy.Off, 'none_found': Autonomy.Off},
										remapping={'name': 'name', 'entity_list': 'entity_list', 'number': 'number'})


		# x:415 y:99, x:318 y:246, x:442 y:295
		_sm_move_head_and_base_end__11 = ConcurrencyContainer(outcomes=['failed'], conditions=[
										('failed', [('move head and base at the end', 'failed')]),
										('failed', [('Groupwait', 'end')])
										])

		with _sm_move_head_and_base_end__11:
			# x:132 y:57
			OperatableStateMachine.add('move head and base at the end',
										_sm_move_head_and_base_at_the_end_9,
										transitions={'failed': 'failed'},
										autonomy={'failed': Autonomy.Inherit})

			# x:121 y:218
			OperatableStateMachine.add('Groupwait',
										_sm_groupwait_8,
										transitions={'end': 'failed'},
										autonomy={'end': Autonomy.Inherit})


		# x:323 y:632, x:638 y:631
		_sm_try_to_reach_12 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['waypoint', 'relative', 'ID'])

		with _sm_try_to_reach_12:
			# x:186 y:130
			OperatableStateMachine.add('Container',
										_sm_container_7,
										transitions={'finished': 'Say_Reached', 'failed': 'say_not_reached', 'check': 'say check'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'check': Autonomy.Inherit},
										remapping={'waypoint': 'waypoint'})

			# x:581 y:163
			OperatableStateMachine.add('check person behind',
										_sm_check_person_behind_6,
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

			# x:520 y:409
			OperatableStateMachine.add('say_not_reached',
										SaraSay(sentence=lambda x: "I have not reach the destination", input_keys=[], emotion=0, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:139 y:339
			OperatableStateMachine.add('Say_Reached',
										SaraSay(sentence=lambda x: "I have reach the destination", input_keys=[], emotion=0, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		# x:626 y:228, x:607 y:71, x:230 y:458, x:330 y:458
		_sm_operator_is_still_there_13 = ConcurrencyContainer(outcomes=['finished', 'failed'], input_keys=['ID'], conditions=[
										('finished', [('find a human', 'finished')]),
										('failed', [('Move head and base end ', 'failed')])
										])

		with _sm_operator_is_still_there_13:
			# x:207 y:54
			OperatableStateMachine.add('Move head and base end ',
										_sm_move_head_and_base_end__11,
										transitions={'failed': 'failed'},
										autonomy={'failed': Autonomy.Inherit})

			# x:222 y:190
			OperatableStateMachine.add('find a human',
										_sm_find_a_human_10,
										transitions={'finished': 'finished'},
										autonomy={'finished': Autonomy.Inherit},
										remapping={'ID': 'ID'})



		with _state_machine:
			# x:52 y:98
			OperatableStateMachine.add('GetPerson',
										GetEntityByID(),
										transitions={'found': 'sayfollowme', 'not_found': 'Action_findPerson'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ID': 'ID', 'Entity': 'Entity'})

			# x:29 y:416
			OperatableStateMachine.add('operator is still there',
										_sm_operator_is_still_there_13,
										transitions={'finished': 'head to middle', 'failed': 'say lost operator'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'ID': 'ID'})

			# x:290 y:324
			OperatableStateMachine.add('say lost operator',
										SaraSay(sentence="I have reach my goal but I lost the person I was guiding.", input_keys=[], emotion=1, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:43 y:214
			OperatableStateMachine.add('sayfollowme',
										SaraSay(sentence="Follow me please.", input_keys=[], emotion=1, block=True),
										transitions={'done': 'Try to reach'},
										autonomy={'done': Autonomy.Off})

			# x:413 y:441
			OperatableStateMachine.add('head to middle',
										SaraSetHeadAngle(pitch=0, yaw=0),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:39 y:330
			OperatableStateMachine.add('Try to reach',
										_sm_try_to_reach_12,
										transitions={'finished': 'operator is still there', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'waypoint': 'Position', 'relative': 'relative', 'ID': 'ID'})

			# x:443 y:95
			OperatableStateMachine.add('Cant Find Person',
										SaraSay(sentence="I can't find a person.", input_keys=[], emotion=1, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:201 y:57
			OperatableStateMachine.add('Action_findPerson',
										self.use_behavior(Action_findPersonSM, 'Action_findPerson'),
										transitions={'done': 'sayfollowme', 'pas_done': 'Cant Find Person'},
										autonomy={'done': Autonomy.Inherit, 'pas_done': Autonomy.Inherit},
										remapping={'className': 'className', 'entity': 'Entity'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
