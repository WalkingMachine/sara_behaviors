#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_action_point_at2')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.Get_direction_to_point import Get_direction_to_point
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_states.pose_gen_euler_key import GenPoseEulerKey
from sara_flexbe_states.moveit_move import MoveitMove
from flexbe_states.calculation_state import CalculationState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed May 02 2018
@author: Huynh-Anh
'''
class Action_point_at2SM(Behavior):
	'''
	pointe
	'''


	def __init__(self):
		super(Action_point_at2SM, self).__init__()
		self.name = 'Action_point_at2'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:739 y:301, x:61 y:579
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['targetPoint'])
		_state_machine.userdata.targetPoint = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:113 y:102
			OperatableStateMachine.add('direction',
										Get_direction_to_point(frame_origin="base_link", frame_reference="right_upper_arm_upper_link"),
										transitions={'done': 'posx', 'fail': 'failed'},
										autonomy={'done': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'targetPoint': 'targetPoint', 'yaw': 'yaw', 'pitch': 'pitch'})

			# x:297 y:337
			OperatableStateMachine.add('setkey',
										SetKey(Value=-0.25),
										transitions={'done': 'invert'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'posy'})

			# x:175 y:226
			OperatableStateMachine.add('posx',
										SetKey(Value=0.8),
										transitions={'done': 'setroll'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'posx'})

			# x:136 y:336
			OperatableStateMachine.add('setroll',
										SetKey(Value=0),
										transitions={'done': 'posz'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'setroll'})

			# x:378 y:187
			OperatableStateMachine.add('genpose',
										GenPoseEulerKey(),
										transitions={'done': 'move'},
										autonomy={'done': Autonomy.Off},
										remapping={'xpos': 'posx', 'ypos': 'posy', 'zpos': 'posz', 'yaw': 'yaw', 'pitch': 'pitch', 'roll': 'setroll', 'pose': 'pose'})

			# x:583 y:193
			OperatableStateMachine.add('move',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'finished', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'pose'})

			# x:189 y:412
			OperatableStateMachine.add('posz',
										SetKey(Value=1.0),
										transitions={'done': 'setkey'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'posz'})

			# x:441 y:405
			OperatableStateMachine.add('invert',
										CalculationState(calculation=lambda x: -x),
										transitions={'done': 'genpose'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'pitch', 'output_value': 'pitch'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
