#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_entity_exists')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from behavior_wonderland_get_entity.wonderland_get_entity_sm import Wonderland_Get_EntitySM
from sara_flexbe_states.for_state import SaraSay
from sara_flexbe_states.Wonderland_Read_Entity import Wonderland_Read_Entity
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu Jul 27 2017
@author: Redouane Laref Nicolas Nadeau
'''
class Entity_ExistsSM(Behavior):
	'''
	the entity exists
	'''


	def __init__(self):
		super(Entity_ExistsSM, self).__init__()
		self.name = 'Entity_Exists'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(Wonderland_Get_EntitySM, 'Wonderland_Get_Entity')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:843 y:107, x:413 y:27, x:873 y:207
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'can't'], input_keys=['name', 'input_value'])
		_state_machine.userdata.name = ""
		_state_machine.userdata.input_value = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:109 y:148
			OperatableStateMachine.add('Wonderland_Get_Entity',
										self.use_behavior(Wonderland_Get_EntitySM, 'Wonderland_Get_Entity'),
										transitions={'done': 'Reading_Entity', 'failed': 'failed'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'name': 'name', 'entity': 'entity'})

			# x:680 y:189
			OperatableStateMachine.add('Dont Know',
										SaraSay(sentence="I do not know that object, please ask me again", emotion=1),
										transitions={'done': 'can't'},
										autonomy={'done': Autonomy.Off})

			# x:692 y:80
			OperatableStateMachine.add('Pleasure',
										SaraSay(sentence="It would be a pleasure to help you", emotion=1),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:422 y:160
			OperatableStateMachine.add('Reading_Entity',
										Wonderland_Read_Entity(index_function=lambda x: 0),
										transitions={'done': 'Pleasure', 'empty': 'Dont Know', 'error': 'failed'},
										autonomy={'done': Autonomy.Off, 'empty': Autonomy.Off, 'error': Autonomy.Off},
										remapping={'json_text': 'entity', 'input_value': 'input_value', 'id': 'id', 'name': 'name', 'time': 'time', 'x_pos': 'x_pos', 'y_pos': 'y_pos', 'z_pos': 'z_pos', 'waypoint_id': 'waypoint_id'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
