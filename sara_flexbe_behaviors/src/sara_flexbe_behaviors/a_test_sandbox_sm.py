#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.pose_gen_euler import GenPoseEuler
from flexbe_states.log_state import LogState
from sara_flexbe_states.moveit_moveCartesian import MoveitMoveCartesian
from sara_flexbe_states.moveit_move import MoveitMove
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu May 10 2018
@author: Philippe La Madeleine
'''
class ATestSandboxSM(Behavior):
	'''
	Une behavior pour faire des tests rapidement.
	'''


	def __init__(self):
		super(ATestSandboxSM, self).__init__()
		self.name = 'A Test Sandbox'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:537 y:110, x:166 y:479
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.Pose1 = "PostGripPose"
		_state_machine.userdata.Pose2 = "IdlePose"
		_state_machine.userdata.actionList = [["Find", "bottle"], ["move", "kitchen"]]
		_state_machine.userdata.titre = "test"
		_state_machine.userdata.relative = False
		_state_machine.userdata.pitch = -0.8
		_state_machine.userdata.Action1 = ["move", "counter"]
		_state_machine.userdata.Action2 = ["move", "table"]
		_state_machine.userdata.pose = "Dining room"

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:47 y:88
			OperatableStateMachine.add('gen',
										GenPoseEuler(x=0.8, y=0, z=1.1, roll=0, pitch=0, yaw=0),
										transitions={'done': 'gen2'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose': 'pose1'})

			# x:411 y:111
			OperatableStateMachine.add('log',
										LogState(text="ok", severity=Logger.REPORT_HINT),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:302 y:211
			OperatableStateMachine.add('mp',
										MoveitMoveCartesian(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'log', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'targetPose': 'pose2'})

			# x:61 y:235
			OperatableStateMachine.add('move',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'mp', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'pose1'})

			# x:203 y:94
			OperatableStateMachine.add('gen2',
										GenPoseEuler(x=0.8, y=-0.5, z=1.1, roll=0, pitch=0, yaw=0),
										transitions={'done': 'move'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose': 'pose2'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
