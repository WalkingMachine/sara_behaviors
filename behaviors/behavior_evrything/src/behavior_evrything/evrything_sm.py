#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_evrything')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from behavior_init_sequence.init_sequence_sm import Init_SequenceSM
from sara_flexbe_states.for_state import SaraSay
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu Jul 27 2017
@author: Redouane Laref Nicolas Nadeau
'''
class EvrythingSM(Behavior):
	'''
	This is our last chance!
	'''


	def __init__(self):
		super(EvrythingSM, self).__init__()
		self.name = 'Evrything'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(Init_SequenceSM, 'Init_Sequence')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:747 y:44, x:209 y:197
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:204 y:38
			OperatableStateMachine.add('Init_Sequence',
										self.use_behavior(Init_SequenceSM, 'Init_Sequence'),
										transitions={'finished': 'Presentation', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:486 y:38
			OperatableStateMachine.add('Presentation',
										SaraSay(sentence="Hi I am SARA do you have instructions for me?", emotion=1),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
