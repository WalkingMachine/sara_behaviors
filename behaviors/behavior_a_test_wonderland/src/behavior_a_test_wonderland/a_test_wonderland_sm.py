#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_a_test_wonderland')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.Wonderland_Add_Human import Wonderland_Add_Human
from sara_flexbe_states.test_log import test_log
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

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:340 y:478, x:232 y:476, x:498 y:55
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'registered'], input_keys=['x1', 'x2', 'x3', 'x4', 'y1', 'y2', 'y3', 'y4'])
		_state_machine.userdata.name = "Prout"
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
		_state_machine.userdata.roomID = None
		_state_machine.userdata.id = 2
		_state_machine.userdata.is_operator = None
		_state_machine.userdata.gender = "M"

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:84 y:538
			OperatableStateMachine.add('Wonderland_Add_Human',
										Wonderland_Add_Human(),
										transitions={'done': 'test_log', 'error': 'failed'},
										autonomy={'done': Autonomy.Off, 'error': Autonomy.Off},
										remapping={'id': 'id', 'name': 'name', 'roomID': 'roomID', 'x_pos': 'x_pos', 'y_pos': 'y_pos', 'z_pos': 'z_pos', 'gender': 'gender', 'is_operator': 'is_operator'})

			# x:274 y:538
			OperatableStateMachine.add('test_log',
										test_log(),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'text': 'id'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
