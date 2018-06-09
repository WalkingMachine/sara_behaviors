#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_action_receive_bag')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_states.moveit_move import MoveitMove
from sara_flexbe_states.torque_reader import ReadTorque
from sara_flexbe_states.set_gripper_state import SetGripperState
from sara_flexbe_states.sara_say import SaraSay
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

		# O 128 372 
		# Prend le sac et le rapporte dans son idle pose



	def create(self):
		# x:867 y:64, x:469 y:60
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['Closed_Gripper_Width', 'Open_Gripper_Width', 'Closed_Gripper_Width'])
		_state_machine.userdata.Closed_Gripper_Width = 1
		_state_machine.userdata.Open_Gripper_Width = 255
		_state_machine.userdata.effort = 50

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:120 y:63
			OperatableStateMachine.add('setTarget1',
										SetKey(Value="Help_me_carry"),
										transitions={'done': 'Go_to_receive_bag_pose'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'target'})

			# x:660 y:57
			OperatableStateMachine.add('Go_to_Pose',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'finished', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'target'})

			# x:381 y:295
			OperatableStateMachine.add('Torque_Reader',
										ReadTorque(watchdog=10, Joint="right_elbow_pitch_joint", Threshold=1, min_time=1),
										transitions={'threshold': 'close_gripper', 'watchdog': 'Torque_Reader', 'fail': 'failed'},
										autonomy={'threshold': Autonomy.Off, 'watchdog': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'torque': 'torque'})

			# x:668 y:133
			OperatableStateMachine.add('setTarget2',
										SetKey(Value="PostGripPose"),
										transitions={'done': 'Go_to_Pose'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'target'})

			# x:78 y:177
			OperatableStateMachine.add('Go_to_receive_bag_pose',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'opengripper', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'target'})

			# x:498 y:273
			OperatableStateMachine.add('close_gripper',
										SetGripperState(width=0, effort=1),
										transitions={'object': 'thank you', 'no_object': 'thank you'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:638 y:216
			OperatableStateMachine.add('thank you',
										SaraSay(sentence="Thank you", emotion=1, block=True),
										transitions={'done': 'setTarget2'},
										autonomy={'done': Autonomy.Off})

			# x:208 y:269
			OperatableStateMachine.add('opengripper',
										SetGripperState(width=0.25, effort=1),
										transitions={'object': 'Torque_Reader', 'no_object': 'Torque_Reader'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
