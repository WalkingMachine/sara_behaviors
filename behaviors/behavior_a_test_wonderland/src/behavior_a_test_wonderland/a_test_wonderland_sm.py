#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_a_test_wonderland')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from behavior_get_operator.get_operator_sm import Get_operatorSM
from sara_flexbe_states.sara_say_key import SaraSayKey
from sara_flexbe_states.sara_say import SaraSay
from flexbe_states.wait_state import WaitState
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
		self.add_behavior(Get_operatorSM, 'Get_operator')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:607 y:186, x:130 y:365, x:230 y:365
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'registered'], input_keys=['x1', 'x2', 'x3', 'x4', 'y1', 'y2', 'y3', 'y4'])
		_state_machine.userdata.name = "Jean Eude"
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
		_state_machine.userdata.roomID = 2
		_state_machine.userdata.id = 5
		_state_machine.userdata.is_operator = None
		_state_machine.userdata.gender = "M"

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:30 y:40
			OperatableStateMachine.add('wait',
										WaitState(wait_time=4),
										transitions={'done': 'Get_operator'},
										autonomy={'done': Autonomy.Off})

			# x:378 y:169
			OperatableStateMachine.add('say',
										SaraSayKey(Format=lambda x: "You are person" + x.ID, emotion=1, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'Operator'})

			# x:146 y:259
			OperatableStateMachine.add('say2',
										SaraSay(sentence="Sorry. I failed", emotion=1, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:150 y:141
			OperatableStateMachine.add('Get_operator',
										self.use_behavior(Get_operatorSM, 'Get_operator'),
										transitions={'Found': 'say', 'NotFound': 'say2'},
										autonomy={'Found': Autonomy.Inherit, 'NotFound': Autonomy.Inherit},
										remapping={'Operator': 'Operator'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
