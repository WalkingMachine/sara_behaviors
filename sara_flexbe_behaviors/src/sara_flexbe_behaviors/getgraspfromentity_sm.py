#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.Get_Entity_By_ID import GetEntityByID
from sara_flexbe_states.GetGraspFromEntity import GetGraspFromEntity
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Jun 03 2019
@author: Jeffrey Cousineau
'''
class GetGraspFromEntitySM(Behavior):
	'''
	Find an entity Id and send it to the grasp state which return the pose to grasp it.
	'''


	def __init__(self):
		super(GetGraspFromEntitySM, self).__init__()
		self.name = 'GetGraspFromEntity'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:31 y:469, x:29 y:271
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.ID = 3

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:255 y:101
			OperatableStateMachine.add('GetEntity',
										GetEntityByID(),
										transitions={'found': 'GetGrasp', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ID': 'ID', 'Entity': 'Entity'})

			# x:505 y:135
			OperatableStateMachine.add('GetGrasp',
										GetGraspFromEntity(approachDistance=0, distanceScoringMultiplier=0.5, orientationScoringMultiplier=0.5, graspScoringMultiplier=0.5),
										transitions={'done': 'finished', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'Entity': 'Entity', 'ApproachPose': 'ApproachPose', 'GraspingPose': 'GraspingPose'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
