#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_wonderland_get_origin')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.Wonderland_Request import Wonderland_Request
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Fri Jul 21 2017
@author: Nicolas Nadeau
'''
class Wonderland_Get_OriginSM(Behavior):
	'''
	Get the Origin Waypoint
	'''


	def __init__(self):
		super(Wonderland_Get_OriginSM, self).__init__()
		self.name = 'Wonderland_Get_Origin'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:531 y:406, x:770 y:386
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], output_keys=['waypoint'])
		_state_machine.userdata.name = "origin"
		_state_machine.userdata.waypoint = ""

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:327 y:130
			OperatableStateMachine.add('calc',
										CalculationState(calculation=lambda x: "waypoint?name="+x),
										transitions={'done': 'Wonderland_Request'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'name', 'output_value': 'url'})

			# x:608 y:168
			OperatableStateMachine.add('Wonderland_Request',
										Wonderland_Request(),
										transitions={'done': 'finished', 'error': 'failed'},
										autonomy={'done': Autonomy.Off, 'error': Autonomy.Off},
										remapping={'url': 'url', 'response': 'waypoint'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
