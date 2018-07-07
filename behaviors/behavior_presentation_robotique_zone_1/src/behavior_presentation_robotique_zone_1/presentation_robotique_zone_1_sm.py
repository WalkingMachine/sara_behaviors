#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_presentation_robotique_zone_1')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.GetClosestObstacle import GetClosestObstacle
from sara_flexbe_states.sara_set_head_angle_key import SaraSetHeadAngleKey
from flexbe_states.calculation_state import CalculationState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Fri Jul 06 2018
@author: Philippe La Madeleine
'''
class Presentation_Robotique_Zone_1SM(Behavior):
	'''
	Presentation_Robotique_Zone_1
	'''


	def __init__(self):
		super(Presentation_Robotique_Zone_1SM, self).__init__()
		self.name = 'Presentation_Robotique_Zone_1'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:30 y:324, x:130 y:324
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.pitch = 0.5

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:77 y:112
			OperatableStateMachine.add('GetClosestObstacle',
										GetClosestObstacle(topic="/scan", maximumDistance=2),
										transitions={'done': 'limit angle'},
										autonomy={'done': Autonomy.Off},
										remapping={'Angle': 'Angle'})

			# x:389 y:162
			OperatableStateMachine.add('SaraSetHeadAngleKey',
										SaraSetHeadAngleKey(),
										transitions={'done': 'GetClosestObstacle'},
										autonomy={'done': Autonomy.Off},
										remapping={'yaw': 'Angle', 'pitch': 'pitch'})

			# x:286 y:81
			OperatableStateMachine.add('limit angle',
										CalculationState(calculation=lambda x: max(min(x,1), -1)),
										transitions={'done': 'SaraSetHeadAngleKey'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Angle', 'output_value': 'Angle'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
