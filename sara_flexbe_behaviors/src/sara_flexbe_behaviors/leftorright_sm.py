#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.ClosestObject import ClosestObject
from flexbe_states.check_condition_state import CheckConditionState
from sara_flexbe_states.sara_say import SaraSay
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Fri Jul 05 2019
@author: Huynh-Anh
'''
class leftOrRightSM(Behavior):
	'''
	return if an object is at the left or right of the robot
	'''


	def __init__(self):
		super(leftOrRightSM, self).__init__()
		self.name = 'leftOrRight'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:818 y:151, x:162 y:460
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['PosFInal', 'object'])
		_state_machine.userdata.object = object
		_state_machine.userdata.PosFInal = PosFinal

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:124 y:77
			OperatableStateMachine.add('ClosestObject',
										ClosestObject(),
										transitions={'found': 'CheckAngle', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'object': 'object', 'angle': 'angle', 'closestObject': 'closestObject'})

			# x:342 y:132
			OperatableStateMachine.add('CheckAngle',
										CheckConditionState(predicate=lambda x: x>0),
										transitions={'true': 'left', 'false': 'sayright'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'angle'})

			# x:552 y:92
			OperatableStateMachine.add('left',
										SaraSay(sentence=lambda x: "The "+ str(x[0]) + " is on the left of" + str(x[0]), input_keys=["object", "closestObject"], emotion=0, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'object': 'object', 'closestObject': 'closestObject'})

			# x:441 y:296
			OperatableStateMachine.add('sayright',
										SaraSay(sentence=lambda x: "The " + str(x[0]) + " is close to ", input_keys=["object","closestObject"], emotion=0, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'object': 'object', 'closestObject': 'closestObject'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
