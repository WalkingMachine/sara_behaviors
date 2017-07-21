#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_wonderland_test')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from behavior_wonderland_get_entity.wonderland_get_entity_sm import Wonderland_Get_EntitySM
from sara_flexbe_states.Wonderland_Get_Entity_Room import Wonderland_Get_Entity_Room
from sara_flexbe_states.test_log import test_log
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Jul 17 2017
@author: Lucas
'''
class Wonderland_TestSM(Behavior):
	'''
	Test state for wonderland
	'''


	def __init__(self):
		super(Wonderland_TestSM, self).__init__()
		self.name = 'Wonderland_Test'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(Wonderland_Get_EntitySM, 'Wonderland_Get_Entity')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:834 y:68, x:299 y:325
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['name', 'index'])
		_state_machine.userdata.name = "Jean Eude"
		_state_machine.userdata.index = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:70 y:60
			OperatableStateMachine.add('Wonderland_Get_Entity',
										self.use_behavior(Wonderland_Get_EntitySM, 'Wonderland_Get_Entity'),
										transitions={'done': 'Wonderland_Get_Entity_Room', 'failed': 'failed'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'name': 'name', 'entity': 'json_text'})

			# x:362 y:64
			OperatableStateMachine.add('Wonderland_Get_Entity_Room',
										Wonderland_Get_Entity_Room(index_function=lambda x: x),
										transitions={'done': 'test_log', 'no_room': 'failed', 'error': 'failed'},
										autonomy={'done': Autonomy.Off, 'no_room': Autonomy.Off, 'error': Autonomy.Off},
										remapping={'json_text': 'json_text', 'input_value': 'index', 'id': 'id', 'name': 'name', 'x1': 'x1', 'x2': 'x2', 'x3': 'x3', 'x4': 'x4', 'y1': 'y1', 'y2': 'y2', 'y3': 'y3', 'y4': 'y4'})

			# x:650 y:63
			OperatableStateMachine.add('test_log',
										test_log(),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'text': 'name'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
