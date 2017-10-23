#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_test_continue')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.move_arm_named_pose import MoveArmNamedPose
from flexbe_states.log_key_state import LogKeyState
from flexbe_states.log_state import LogState
from sara_flexbe_states.sara_move_base import SaraMoveBase
from behavior_action_pick.action_pick_sm import Action_pickSM
from sara_flexbe_states.Wonderland_Get_Object import GetObject
from sara_flexbe_states.sara_say_key import SaraSayKey
from sara_flexbe_states.get_robot_pose import Get_Robot_Pose
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.for_loop import ForLoop
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Tue Jul 25 2017
@author: Philippe la Madeleine
'''
class Test_continueSM(Behavior):
	'''
	test the continue button
	'''


	def __init__(self):
		super(Test_continueSM, self).__init__()
		self.name = 'Test_continue'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(Action_pickSM, 'Action_pick')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]

	# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:653 y:645, x:641 y:194
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.id = None
		_state_machine.userdata.name = "cup"
		_state_machine.userdata.color = None
		_state_machine.userdata.type = None
		_state_machine.userdata.room = None

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]

		# [/MANUAL_CREATE]


		with _state_machine:
			# x:42 y:30
			OperatableStateMachine.add('place arm',
										MoveArmNamedPose(pose_name="PreGripPose", wait=True),
										transitions={'done': 'get pose', 'failed': 'get pose'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

			# x:49 y:491
			OperatableStateMachine.add('log',
										LogKeyState(text="{}", severity=Logger.REPORT_HINT),
										transitions={'done': 'Action_pick'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'object_color'})

			# x:312 y:259
			OperatableStateMachine.add('fail',
										LogState(text="fail", severity=Logger.REPORT_HINT),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:38 y:377
			OperatableStateMachine.add('move',
										SaraMoveBase(),
										transitions={'arrived': 'log', 'failed': 'fail'},
										autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'object_pose'})

			# x:45 y:590
			OperatableStateMachine.add('Action_pick',
										self.use_behavior(Action_pickSM, 'Action_pick'),
										transitions={'success': 'say3', 'too far': 'failed', 'unreachable': 'failed', 'not seen': 'failed', 'critical fail': 'failed', 'missed': 'say2'},
										autonomy={'success': Autonomy.Inherit, 'too far': Autonomy.Inherit, 'unreachable': Autonomy.Inherit, 'not seen': Autonomy.Inherit, 'critical fail': Autonomy.Inherit, 'missed': Autonomy.Inherit},
										remapping={'object': 'object_name', 'grip_pose': 'grip_pose'})

			# x:47 y:193
			OperatableStateMachine.add('obj',
										GetObject(),
										transitions={'found': 'say1', 'unknown': 'say 3', 'error': 'fail'},
										autonomy={'found': Autonomy.Off, 'unknown': Autonomy.Off, 'error': Autonomy.Off},
										remapping={'id': 'id', 'name': 'name', 'color': 'color', 'room': 'room', 'type': 'type', 'expected_pose': 'expected_pose', 'object_pose': 'object_pose', 'object_name': 'object_name', 'object_color': 'object_color', 'object_room': 'object_room', 'object_type': 'object_type'})

			# x:37 y:282
			OperatableStateMachine.add('say1',
										SaraSayKey(Format=lambda x: "I'm going to pick the "+x, emotion=1, block=False),
										transitions={'done': 'move'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'name'})

			# x:41 y:112
			OperatableStateMachine.add('get pose',
										Get_Robot_Pose(),
										transitions={'done': 'obj'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose': 'expected_pose'})

			# x:175 y:426
			OperatableStateMachine.add('say2',
										SaraSay(sentence=lambda x: "I got it, it is "+x, emotion=1, block=False),
										transitions={'done': 'for'},
										autonomy={'done': Autonomy.Off})

			# x:240 y:511
			OperatableStateMachine.add('for',
										ForLoop(repeat=1),
										transitions={'do': 'Action_pick', 'end': 'failed'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index'})

			# x:358 y:589
			OperatableStateMachine.add('say3',
										SaraSayKey(Format=lambda x: "I got it, it is "+x, emotion=1, block=False),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'object_color'})

			# x:226 y:162
			OperatableStateMachine.add('say 3',
										SaraSayKey(Format=lambda x: "I don't know this "+x, emotion=1, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'name'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]

	# [/MANUAL_FUNC]
