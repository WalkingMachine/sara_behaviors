#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_action_receive_bag')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.move_joint import MoveJoint
from flexbe_states.wait_state import WaitState
from sara_flexbe_states.publisher_gripper_state import PublisherGripperState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu Jul 27 2017
@author: Redouane Laref
'''
class Action_Receive_BagSM(Behavior):
	'''
	Action for receiving the bag for help me carry scenario.
	'''


	def __init__(self):
		super(Action_Receive_BagSM, self).__init__()
		self.name = 'Action_Receive_Bag'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1076 y:112, x:566 y:14
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['Closed_Gripper_Width', 'Open_Gripper_Width', 'Closed_Gripper_Width'])
		_state_machine.userdata.Closed_Gripper_Width = 1
		_state_machine.userdata.Open_Gripper_Width = 255
		_state_machine.userdata.effort = 50

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:132 y:109
			OperatableStateMachine.add('Go_to_receive_bag_pose',
										MoveJoint(pose_name="Help_me_carry"),
										transitions={'done': 'Wait_to_close_gripper', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

			# x:865 y:112
			OperatableStateMachine.add('Go_to_IdlePose',
										MoveJoint(pose_name="IdlePose"),
										transitions={'done': 'finished', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

			# x:371 y:107
			OperatableStateMachine.add('Wait_to_close_gripper',
										WaitState(wait_time=5),
										transitions={'done': 'Close_gripper'},
										autonomy={'done': Autonomy.Off})

			# x:599 y:111
			OperatableStateMachine.add('Close_gripper',
										PublisherGripperState(),
										transitions={'done': 'Go_to_IdlePose'},
										autonomy={'done': Autonomy.Off},
										remapping={'width': 'Closed_Gripper_Width', 'effort': 'effort'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
