#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.WonderlandGetEntityVerbal import WonderlandGetEntityVerbal
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.SetKey import SetKey
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on 22/05/2018
@author: Lucas Maurice
'''
class WonderlandUniqueEnitySM(Behavior):
	'''
	Will try to fin an entity verbally selected. Will give a vocal feedback of the action and return done or failed.

`name` is the yolo class of the object of the name of a room.
`container` is the yolo class or the container of the name if it is a room. Can be an array.
	'''


	def __init__(self):
		super(WonderlandUniqueEnitySM, self).__init__()
		self.name = 'WonderlandUniqueEnity'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
        
        # [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:395 y:74, x:403 y:154
		_state_machine = OperatableStateMachine(outcomes=['found', 'not_found'], input_keys=['name', 'containers'], output_keys=['entity'])
		_state_machine.userdata.containers = ['dining']
		_state_machine.userdata.name = 'table'
		_state_machine.userdata.entity = None

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

		# x:847 y:29, x:855 y:216
		_sm_try_to_find_area_0 = OperatableStateMachine(outcomes=['found', 'not_found'], input_keys=['area_to_search', 'containers'], output_keys=['entity'])

		with _sm_try_to_find_area_0:
			# x:54 y:36
			OperatableStateMachine.add('GetEntityLocation',
										WonderlandGetEntityVerbal(),
										transitions={'one': 'found', 'multiple': 'Say_More_Than_One', 'none': 'Say_No_Area', 'error': 'Say Error'},
										autonomy={'one': Autonomy.Off, 'multiple': Autonomy.Off, 'none': Autonomy.Off, 'error': Autonomy.Off},
										remapping={'name': 'area_to_search', 'containers': 'containers', 'entities': 'entity'})

			# x:478 y:107
			OperatableStateMachine.add('Say Be More Precise',
										SaraSay(sentence="Can you repeat and be more precise please ?", input_keys=[], emotion=5, block=True),
										transitions={'done': 'setNone'},
										autonomy={'done': Autonomy.Off})

			# x:321 y:308
			OperatableStateMachine.add('Say Error',
										SaraSay(sentence="I experience memory problem", input_keys=[], emotion=1, block=True),
										transitions={'done': 'Say Error 2'},
										autonomy={'done': Autonomy.Off})

			# x:478 y:321
			OperatableStateMachine.add('Say Error 2',
										SaraSay(sentence="Can you try again please ?", input_keys=[], emotion=1, block=True),
										transitions={'done': 'setNone'},
										autonomy={'done': Autonomy.Off})

			# x:663 y:195
			OperatableStateMachine.add('setNone',
										SetKey(Value=None),
										transitions={'done': 'not_found'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'entity'})

			# x:294 y:107
			OperatableStateMachine.add('Say_More_Than_One',
										SaraSay(sentence=lambda x: "There is more than one " + str(x), input_keys=["name"], emotion=3, block=True),
										transitions={'done': 'Say Be More Precise'},
										autonomy={'done': Autonomy.Off},
										remapping={'name': 'area_to_search'})

			# x:302 y:204
			OperatableStateMachine.add('Say_No_Area',
										SaraSay(sentence=lambda x: "There is no " + str(x), input_keys=[], emotion=0, block=True),
										transitions={'done': 'setNone'},
										autonomy={'done': Autonomy.Off})



		with _state_machine:
			# x:132 y:88
			OperatableStateMachine.add('Try_to_find_area',
										_sm_try_to_find_area_0,
										transitions={'found': 'found', 'not_found': 'not_found'},
										autonomy={'found': Autonomy.Inherit, 'not_found': Autonomy.Inherit},
										remapping={'area_to_search': 'name', 'containers': 'containers', 'entity': 'entity'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
