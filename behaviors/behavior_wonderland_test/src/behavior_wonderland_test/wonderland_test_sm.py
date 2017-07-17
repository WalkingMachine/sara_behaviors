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
from flexbe_states.log_state import LogState
from sara_flexbe_states.Wonderland_Entity_Exist import Wonderland_Entity_Exist
from sara_flexbe_states.Wonderland_Read_Entity_Position import Wonderland_Read_Entity_Position
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
		# x:1109 y:95, x:785 y:530
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['name'])
		_state_machine.userdata.name = "Table"

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:101 y:112
			OperatableStateMachine.add('Wonderland_Get_Entity',
										self.use_behavior(Wonderland_Get_EntitySM, 'Wonderland_Get_Entity'),
										transitions={'done': 'Wonderland_Entity_Exist', 'failed': 'failed'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'name': 'name', 'entity': 'json_text'})

			# x:561 y:236
			OperatableStateMachine.add('Empty Log',
										LogState(text="There is no entity !", severity=Logger.REPORT_HINT),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:421 y:36
			OperatableStateMachine.add('Wonderland_Entity_Exist',
										Wonderland_Entity_Exist(),
										transitions={'one': 'Wonderland_Read_Entity_Position', 'multiple': 'Wonderland_Read_Entity_Position', 'empty': 'Empty Log'},
										autonomy={'one': Autonomy.Off, 'multiple': Autonomy.Off, 'empty': Autonomy.Off},
										remapping={'json_text': 'json_text', 'number': 'number'})

			# x:685 y:29
			OperatableStateMachine.add('Wonderland_Read_Entity_Position',
										Wonderland_Read_Entity_Position(),
										transitions={'done': 'finished', 'empty': 'Log', 'error': 'failed'},
										autonomy={'done': Autonomy.Off, 'empty': Autonomy.Off, 'error': Autonomy.Off},
										remapping={'json_text': 'json_text', 'x_pos': 'x_pos', 'y_pos': 'y_pos', 'z_pos': 'z_pos'})

			# x:958 y:245
			OperatableStateMachine.add('Log',
										LogState(text="Empty 2", severity=Logger.REPORT_HINT),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
