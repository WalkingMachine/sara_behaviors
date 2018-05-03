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
from sara_flexbe_states.moveit_move import MoveitMove
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.point_at_gen_pose import point_at_gen_pose
from flexbe_states.log_key_state import LogKeyState
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
		# x:736 y:384, x:79 y:422
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['targetPoint'])
		_state_machine.userdata.targetPoint = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:92 y:41
			OperatableStateMachine.add('direction',
										Get_direction_to_point(frame_origin="base_link", frame_reference="right_upper_arm_upper_link"),
										transitions={'done': 'print pitch', 'fail': 'failed'},
										autonomy={'done': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'targetPoint': 'targetPoint', 'yaw': 'yaw', 'pitch': 'pitch'})

			# x:547 y:239
			OperatableStateMachine.add('move',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'finished', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'pose'})

			# x:126 y:277
			OperatableStateMachine.add('invert',
										CalculationState(calculation=lambda x: -x),
										transitions={'done': 'point'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'pitch', 'output_value': 'pitch'})

			# x:308 y:250
			OperatableStateMachine.add('point',
										point_at_gen_pose(offsetx=0.4, offsety=-0.3, offsetz=1.0, l=0.5),
										transitions={'pose': 'move'},
										autonomy={'pose': Autonomy.Off},
										remapping={'yaw': 'yaw', 'pitch': 'pitch', 'pose': 'pose'})

			# x:173 y:129
			OperatableStateMachine.add('print pitch',
										LogKeyState(text="pitch = {}", severity=Logger.REPORT_HINT),
										transitions={'done': 'invert'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'pitch'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
