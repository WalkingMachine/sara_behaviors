#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_wonderland_waypoint_id')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.Wonderland_Request import Wonderland_Request
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed Jul 26 2017
@author: Redouane Laref
'''
class wonderland_waypoint_idSM(Behavior):
	'''
	wonderland move base waypoint to pose
	'''


	def __init__(self):
		super(wonderland_waypoint_idSM, self).__init__()
		self.name = 'wonderland_waypoint_id'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:278 y:355, x:568 y:340
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['waypoint_id'])
		_state_machine.userdata.waypoint_id = ""

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:179 y:112
			OperatableStateMachine.add('calcu',
										CalculationState(calculation=lambda x: "waypoint?id="+x),
										transitions={'done': 'Request to wonderland'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'waypoint_id', 'output_value': 'url'})

			# x:387 y:133
			OperatableStateMachine.add('Request to wonderland',
										Wonderland_Request(),
										transitions={'done': 'finished', 'error': 'failed'},
										autonomy={'done': Autonomy.Off, 'error': Autonomy.Off},
										remapping={'url': 'url', 'response': 'waypoint_id'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
