#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_action_lookatbase')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.Get_direction_to_point import Get_direction_to_point
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.sara_set_head_angle_key import SaraSetHeadAngleKey
from sara_flexbe_states.SetKey import SetKey
from behavior_action_turn.action_turn_sm import action_turnSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed Apr 25 2018
@author: Veronica
'''
class action_lookAtBaseSM(Behavior):
	'''
	Makes sara look at a given point
	'''


	def __init__(self):
		super(action_lookAtBaseSM, self).__init__()
		self.name = 'action_lookAtBase'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(action_turnSM, 'action_turn')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
        
        # [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:400 y:37
		_state_machine = OperatableStateMachine(outcomes=['finished'], input_keys=['Position'])
		_state_machine.userdata.Position = None

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


		with _state_machine:
			# x:39 y:28
			OperatableStateMachine.add('Direction',
										Get_direction_to_point(frame_origin="base_link", frame_reference="head_link"),
										transitions={'done': 'limit yaw', 'fail': 'finished'},
										autonomy={'done': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'targetPoint': 'Position', 'yaw': 'yaw', 'pitch': 'pitch'})

			# x:41 y:191
			OperatableStateMachine.add('invertPitch',
										CalculationState(calculation=lambda x: max(min(-x, 0.5),-0.5)),
										transitions={'done': 'zero'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'pitch', 'output_value': 'pitch'})

			# x:46 y:104
			OperatableStateMachine.add('limit yaw',
										CalculationState(calculation=lambda x: max(min(x, 1.5), -1.5)),
										transitions={'done': 'invertPitch'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'yaw', 'output_value': 'yaw'})

			# x:46 y:388
			OperatableStateMachine.add('Tete',
										SaraSetHeadAngleKey(),
										transitions={'done': 'action_turn'},
										autonomy={'done': Autonomy.Off},
										remapping={'yaw': 'zero', 'pitch': 'pitch'})

			# x:61 y:291
			OperatableStateMachine.add('zero',
										SetKey(Value=0),
										transitions={'done': 'Tete'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'zero'})

			# x:353 y:387
			OperatableStateMachine.add('action_turn',
										self.use_behavior(action_turnSM, 'action_turn'),
										transitions={'finished': 'finished', 'failed': 'finished'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'rotation': 'yaw'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]

    
    # [/MANUAL_FUNC]
