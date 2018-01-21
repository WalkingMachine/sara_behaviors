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
from sara_flexbe_states.set_gripper_state import SetGripperState
from sara_flexbe_states.torque_reader import ReadTorque
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
		# x:867 y:64, x:469 y:60
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['Closed_Gripper_Width', 'Open_Gripper_Width', 'Closed_Gripper_Width'])
		_state_machine.userdata.Closed_Gripper_Width = 1
		_state_machine.userdata.Open_Gripper_Width = 255
		_state_machine.userdata.effort = 50

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:175 y:49
			OperatableStateMachine.add('setTarget1',
										SetKey(Value="Help_me_carry"),
										transitions={'done': 'Go_to_receive_bag_pose'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'target'})

			# x:660 y:57
			OperatableStateMachine.add('Go_to_IdlePose',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'finished', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'target'})

			# x:563 y:256
			OperatableStateMachine.add('Close_gripper',
										SetGripperState(width=0, effort=1),
										transitions={'object': 'setTarget2', 'no_object': 'setTarget2'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:362 y:251
			OperatableStateMachine.add('Torque_Reader',
										ReadTorque(),
										transitions={'done': 'Close_gripper'},
										autonomy={'done': Autonomy.Off})

			# x:664 y:147
			OperatableStateMachine.add('setTarget2',
										SetKey(Value="IdlePose"),
										transitions={'done': 'Go_to_IdlePose'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'target'})

			# x:160 y:163
			OperatableStateMachine.add('Go_to_receive_bag_pose',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'Torque_Reader', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'target'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
