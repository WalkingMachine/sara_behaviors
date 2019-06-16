#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.sara_follow import SaraFollow
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Apr 30 2018
@author: Raphael Duchaine
'''
class Action_followSM(Behavior):
	'''
	Permet de suivre quelqu'un.
Demande le id de la personne a suivre
	'''


	def __init__(self):
		super(Action_followSM, self).__init__()
		self.name = 'Action_follow'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
        
        # [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:572 y:135
		_state_machine = OperatableStateMachine(outcomes=['failed'], input_keys=['ID'])
		_state_machine.userdata.ID = 627

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

		# x:30 y:365
		_sm_follow_0 = OperatableStateMachine(outcomes=['failed'], input_keys=['ID'])

		with _sm_follow_0:
			# x:65 y:167
			OperatableStateMachine.add('follow',
										SaraFollow(distance=1.5, ReplanPeriod=1),
										transitions={'failed': 'follow'},
										autonomy={'failed': Autonomy.Off},
										remapping={'ID': 'ID'})


		# x:368 y:271, x:423 y:158, x:230 y:458
		_sm_follow_1 = ConcurrencyContainer(outcomes=['not_found'], input_keys=['ID'], conditions=[
										('not_found', [('Follow', 'failed')])
										])

		with _sm_follow_1:
			# x:185 y:134
			OperatableStateMachine.add('Follow',
										_sm_follow_0,
										transitions={'failed': 'not_found'},
										autonomy={'failed': Autonomy.Inherit},
										remapping={'ID': 'ID'})



		with _state_machine:
			# x:150 y:130
			OperatableStateMachine.add('Follow',
										_sm_follow_1,
										transitions={'not_found': 'failed'},
										autonomy={'not_found': Autonomy.Inherit},
										remapping={'ID': 'ID'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
