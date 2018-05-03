#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_a_test_wonderland')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.pose_gen_euler import GenPoseEuler
from flexbe_states.calculation_state import CalculationState
from behavior_action_point_at2.action_point_at2_sm import Action_point_at2SM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Jul 17 2017
@author: Lucas
'''
class A_TEST_WONDERLANDSM(Behavior):
	'''
	sfdf
	'''


	def __init__(self):
		super(A_TEST_WONDERLANDSM, self).__init__()
		self.name = 'A_TEST_WONDERLAND'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(Action_point_at2SM, 'Action_point_at2')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:30 y:365, x:130 y:365, x:230 y:365
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'registered'], input_keys=['x1', 'x2', 'x3', 'x4', 'y1', 'y2', 'y3', 'y4'])
		_state_machine.userdata.name = "Jean Eude"
		_state_machine.userdata.x1 = 1
		_state_machine.userdata.x2 = 2
		_state_machine.userdata.x3 = 3
		_state_machine.userdata.x4 = 4
		_state_machine.userdata.y1 = 5
		_state_machine.userdata.y2 = 6
		_state_machine.userdata.y3 = 7
		_state_machine.userdata.y4 = 8
		_state_machine.userdata.x_pos = 100
		_state_machine.userdata.y_pos = 200
		_state_machine.userdata.z_pos = 300
		_state_machine.userdata.roomID = 2
		_state_machine.userdata.id = 5
		_state_machine.userdata.is_operator = None
		_state_machine.userdata.gender = "M"

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:61 y:59
			OperatableStateMachine.add('genpose',
										GenPoseEuler(x=2, y=2, z=1.4, roll=0, pitch=0, yaw=0),
										transitions={'done': 'obtenirpointdanspose'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose': 'pose'})

			# x:69 y:151
			OperatableStateMachine.add('obtenirpointdanspose',
										CalculationState(calculation=lambda x: x.position),
										transitions={'done': 'Action_point_at2'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'pose', 'output_value': 'targetPoint'})

			# x:289 y:171
			OperatableStateMachine.add('Action_point_at2',
										self.use_behavior(Action_point_at2SM, 'Action_point_at2'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'targetPoint': 'targetPoint'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
