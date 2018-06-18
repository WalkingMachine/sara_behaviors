#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_a_test_sandbox')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.GetClosestObstacle import GetClosestObstacle
from flexbe_states.log_state import LogState
from behavior_action_move.action_move_sm import Action_MoveSM
from sara_flexbe_states.pose_gen_euler import GenPoseEuler
from sara_flexbe_states.sara_set_head_angle_key import SaraSetHeadAngleKey
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
		self.add_behavior(Action_MoveSM, 'Action_Move')
		self.add_behavior(Action_MoveSM, 'Action_Move_2')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:824 y:62, x:824 y:212
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.Pose1 = "PostGripPose"
		_state_machine.userdata.Pose2 = "IdlePose"
		_state_machine.userdata.actionList = [["Find", "bottle"], ["move", "kitchen"]]
		_state_machine.userdata.titre = "test"
		_state_machine.userdata.relative = False
		_state_machine.userdata.pitch = 0.8

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:135 y:57
			OperatableStateMachine.add('pose',
										GenPoseEuler(x=1, y=-8, z=0, roll=0, pitch=0, yaw=0),
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose': 'pose'})

			# x:725 y:32
			OperatableStateMachine.add('success',
										LogState(text="The test is a success", severity=Logger.REPORT_HINT),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:361 y:47
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(Action_MoveSM, 'Action_Move'),
										transitions={'finished': 'gen', 'failed': 'Failure'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'pose', 'relative': 'relative'})

			# x:718 y:180
			OperatableStateMachine.add('Failure',
										LogState(text="The test is a failure", severity=Logger.REPORT_HINT),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:491 y:271
			OperatableStateMachine.add('gen',
										GenPoseEuler(x=1, y=0, z=0, roll=0, pitch=0, yaw=0),
										transitions={'done': 'Action_Move_2'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose': 'pose'})

			# x:142 y:264
			OperatableStateMachine.add('Action_Move_2',
										self.use_behavior(Action_MoveSM, 'Action_Move_2'),
										transitions={'finished': 'pose', 'failed': 'Failure'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'pose', 'relative': 'relative'})

			# x:499 y:499
			OperatableStateMachine.add('turn',
										SaraSetHeadAngleKey(),
										transitions={'done': 'ob'},
										autonomy={'done': Autonomy.Off},
										remapping={'yaw': 'Angle', 'pitch': 'pitch'})

			# x:261 y:488
			OperatableStateMachine.add('ob',
										GetClosestObstacle(topic="/scan", maximumDistance=2),
										transitions={'done': 'turn'},
										autonomy={'done': Autonomy.Off},
										remapping={'Angle': 'Angle'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
