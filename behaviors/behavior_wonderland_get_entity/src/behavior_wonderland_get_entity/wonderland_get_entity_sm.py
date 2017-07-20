#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_wonderland_get_entity')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.Wonderland_Request import Wonderland_Request
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sun Jul 16 2017
@author: Lucas Maurice
'''
class Wonderland_Get_EntitySM(Behavior):
	'''
	Get all the data about an entity from the Wonderland DataBase
	'''


	def __init__(self):
		super(Wonderland_Get_EntitySM, self).__init__()
		self.name = 'Wonderland_Get_Entity'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:47 y:386, x:474 y:385
		_state_machine = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['name'], output_keys=['entity'])
		_state_machine.userdata.name = "Paul"
		_state_machine.userdata.entity = ""

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:77 y:80
			OperatableStateMachine.add('calc',
										CalculationState(calculation=lambda x: "entity?name="+x),
										transitions={'done': 'Wonderland_Request'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'name', 'output_value': 'url'})

			# x:252 y:153
			OperatableStateMachine.add('Wonderland_Request',
										Wonderland_Request(),
										transitions={'done': 'done', 'error': 'failed'},
										autonomy={'done': Autonomy.Off, 'error': Autonomy.Off},
										remapping={'url': 'url', 'response': 'entity'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
