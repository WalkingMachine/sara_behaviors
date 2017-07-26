#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_entity_pose_creator')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.log_state import LogState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Tue Jul 25 2017
@author: Redouane Laref - Nicolas Nadeau
'''
class Entity_Pose_CreatorSM(Behavior):
	'''
	comparing waypoint vs xyz
	'''


	def __init__(self):
		super(Entity_Pose_CreatorSM, self).__init__()
		self.name = 'Entity_Pose_Creator'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:30 y:321
		_state_machine = OperatableStateMachine(outcomes=['finished'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:163 y:159
			OperatableStateMachine.add('log',
										LogState(text='asdasdasd', severity=Logger.REPORT_HINT),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
