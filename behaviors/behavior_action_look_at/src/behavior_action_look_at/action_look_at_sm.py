#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_action_look_at')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.Get_direction_to_point import Get_direction_to_point
from sara_flexbe_states.sara_set_head_angle_key import SaraSetHeadAngleKey
from flexbe_states.calculation_state import CalculationState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed Apr 25 2018
@author: Veronica
'''
class action_look_atSM(Behavior):
	'''
	Makes sara look at a given point
	'''


	def __init__(self):
		super(action_look_atSM, self).__init__()
		self.name = 'action_look_at'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
        
        # [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:259 y:36
		_state_machine = OperatableStateMachine(outcomes=['finished'], input_keys=['Position'])
		_state_machine.userdata.Position = None

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


		with _state_machine:
			# x:39 y:28
			OperatableStateMachine.add('Direction',
										Get_direction_to_point(frame_origin="base_link", frame_reference="head_xtion_link"),
										transitions={'done': 'limit yaw', 'fail': 'finished'},
										autonomy={'done': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'targetPoint': 'Position', 'yaw': 'yaw', 'pitch': 'pitch'})

			# x:30 y:272
			OperatableStateMachine.add('Tete',
										SaraSetHeadAngleKey(),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'yaw': 'yaw', 'pitch': 'pitch'})

			# x:41 y:191
			OperatableStateMachine.add('invertPitch',
										CalculationState(calculation=lambda x: max(min(-x, 0.7),-0.7)+0.2),
										transitions={'done': 'Tete'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'pitch', 'output_value': 'pitch'})

			# x:46 y:104
			OperatableStateMachine.add('limit yaw',
										CalculationState(calculation=lambda x: max(min(x, 2), -2)),
										transitions={'done': 'invertPitch'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'yaw', 'output_value': 'yaw'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]

    
    # [/MANUAL_FUNC]
