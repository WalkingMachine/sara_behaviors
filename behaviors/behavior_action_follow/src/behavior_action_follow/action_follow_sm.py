#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_action_follow')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.Get_Entity_By_ID import GetEntityByID
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.get_distance2D import getDistance2D
from sara_flexbe_states.get_robot_pose import Get_Robot_Pose
from sara_flexbe_states.process_follow_distance import processFollowDistance
from sara_flexbe_states.get_reachable_waypoint import Get_Reacheable_Waypoint
from sara_flexbe_states.sara_move_base import SaraMoveBase
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
		# x:447 y:47
		_state_machine = OperatableStateMachine(outcomes=['failed'], input_keys=['ID'])
		_state_machine.userdata.ID = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


		with _state_machine:
			# x:30 y:40
			OperatableStateMachine.add('GetEntityByID',
										GetEntityByID(),
										transitions={'found': 'getPositionFromEntity', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ID': 'ID', 'Entity': 'Entity'})

			# x:21 y:164
			OperatableStateMachine.add('getPositionFromEntity',
										CalculationState(calculation=lambda x: x.position),
										transitions={'done': 'Get_Robot_Pose'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Entity', 'output_value': 'position'})

			# x:42 y:433
			OperatableStateMachine.add('getDistance2D',
										getDistance2D(),
										transitions={'done': 'processFollowDistance'},
										autonomy={'done': Autonomy.Off},
										remapping={'point1': 'position', 'point2': 'sara_position', 'distance': 'distance'})

			# x:51 y:232
			OperatableStateMachine.add('Get_Robot_Pose',
										Get_Robot_Pose(),
										transitions={'done': 'getPositionFromPose'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose': 'pose'})

			# x:37 y:327
			OperatableStateMachine.add('getPositionFromPose',
										CalculationState(calculation=lambda x: x.position),
										transitions={'done': 'getDistance2D'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'pose', 'output_value': 'sara_position'})

			# x:41 y:532
			OperatableStateMachine.add('processFollowDistance',
										processFollowDistance(minimum_distance=2, divisor_distance=2, threshold=.5),
										transitions={'move': 'Get_Reacheable_Waypoint', 'done': 'Get_Reacheable_Waypoint'},
										autonomy={'move': Autonomy.Off, 'done': Autonomy.Off},
										remapping={'distance_of_target': 'distance', 'distance': 'distance'})

			# x:145 y:626
			OperatableStateMachine.add('Get_Reacheable_Waypoint',
										Get_Reacheable_Waypoint(),
										transitions={'done': 'SaraMoveBase'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose_in': 'position', 'distance': 'distance', 'pose_out': 'pose_out'})

			# x:417 y:374
			OperatableStateMachine.add('SaraMoveBase',
										SaraMoveBase(),
										transitions={'arrived': 'GetEntityByID', 'failed': 'GetEntityByID'},
										autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'pose_out'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
