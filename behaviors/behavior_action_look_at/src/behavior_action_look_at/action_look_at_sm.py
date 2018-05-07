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
		# x:873 y:200, x:801 y:120
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['Position'])
		_state_machine.userdata.Position = None

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


		with _state_machine:
			# x:352 y:107
			OperatableStateMachine.add('Direction',
										Get_direction_to_point(frame_origin="base_link", frame_reference="head_link"),
										transitions={'done': 'invertPitch', 'fail': 'failed'},
										autonomy={'done': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'targetPoint': 'Position', 'yaw': 'yaw', 'pitch': 'pitch'})

			# x:676 y:191
			OperatableStateMachine.add('Tete',
										SaraSetHeadAngleKey(),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'yaw': 'yaw', 'pitch': 'pitch'})

			# x:529 y:141
			OperatableStateMachine.add('invertPitch',
										CalculationState(calculation=lambda x: -x),
										transitions={'done': 'Tete'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'pitch', 'output_value': 'pitch'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
