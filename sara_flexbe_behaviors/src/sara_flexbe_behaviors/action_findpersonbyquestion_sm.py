#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.sara_set_head_angle import SaraSetHeadAngle
from flexbe_states.wait_state import WaitState
from sara_flexbe_states.list_entities_by_name import list_entities_by_name
from sara_flexbe_states.for_loop import ForLoop
from flexbe_states.flexible_check_condition_state import FlexibleCheckConditionState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sat Jun 01 2019
@author: Quentin Gaillot
'''
class Action_FindPersonByQuestionSM(Behavior):
	'''
	Find a person by asking a question and return an entity (ex: Are you John?)
Look 180 degres, do not rotate
	'''


	def __init__(self):
		super(Action_FindPersonByQuestionSM, self).__init__()
		self.name = 'Action_FindPersonByQuestion'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:699 y:543, x:709 y:126, x:676 y:54
		_state_machine = OperatableStateMachine(outcomes=['found', 'failed', 'not_found'], input_keys=['question'], output_keys=['entityFound'])
		_state_machine.userdata.question = ""
		_state_machine.userdata.entityFound = ""
		_state_machine.userdata.personKey = "person"

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:54 y:25
			OperatableStateMachine.add('look left',
										SaraSetHeadAngle(pitch=0.1, yaw=1.5),
										transitions={'done': 'waitleft'},
										autonomy={'done': Autonomy.Off})

			# x:72 y:90
			OperatableStateMachine.add('waitleft',
										WaitState(wait_time=4),
										transitions={'done': 'look right'},
										autonomy={'done': Autonomy.Off})

			# x:57 y:155
			OperatableStateMachine.add('look right',
										SaraSetHeadAngle(pitch=0.1, yaw=-1.5),
										transitions={'done': 'get list of person'},
										autonomy={'done': Autonomy.Off})

			# x:55 y:225
			OperatableStateMachine.add('get list of person',
										list_entities_by_name(frontality_level=0.5, distance_max=4),
										transitions={'found': 'for each item', 'none_found': 'not_found'},
										autonomy={'found': Autonomy.Off, 'none_found': Autonomy.Off},
										remapping={'name': 'personKey', 'entity_list': 'entity_list', 'number': 'number'})

			# x:54 y:287
			OperatableStateMachine.add('for each item',
										ForLoop(repeat=5),
										transitions={'do': 'if index greater than number of entity in list', 'end': 'not_found'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index'})

			# x:17 y:354
			OperatableStateMachine.add('if index greater than number of entity in list',
										FlexibleCheckConditionState(predicate=lambda x: x[0] >= len(x[1]), input_keys=["index","entity_list"]),
										transitions={'true': 'not_found', 'false': 'found'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'index': 'index', 'entity_list': 'entity_list'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
