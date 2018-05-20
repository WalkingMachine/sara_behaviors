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
from flexbe_states.log_key_state import LogKeyState
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.sara_move_base import SaraMoveBase
from flexbe_states.wait_state import WaitState
from sara_flexbe_states.get_distance2D import getDistance2D
from sara_flexbe_states.get_robot_pose import Get_Robot_Pose
from sara_flexbe_states.get_reachable_waypoint import Get_Reacheable_Waypoint
from sara_flexbe_states.process_follow_distance import processFollowDistance
from sara_flexbe_states.SetKey import SetKey
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
		_state_machine = OperatableStateMachine(outcomes=['failed'], input_keys=['ID', 'distance'])
		_state_machine.userdata.ID = 74
		_state_machine.userdata.distance = 1

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

		# x:549 y:52, x:392 y:555
		_sm_group_2_0 = OperatableStateMachine(outcomes=['not_found', 'update'], input_keys=['ID', 'TargetPose', 'distance'], output_keys=['TargetPose'])

		with _sm_group_2_0:
			# x:309 y:115
			OperatableStateMachine.add('wait1',
										WaitState(wait_time=2),
										transitions={'done': 'GetEntityByID'},
										autonomy={'done': Autonomy.Off})

			# x:32 y:113
			OperatableStateMachine.add('getPositionFromEntity',
										CalculationState(calculation=lambda x: x.position),
										transitions={'done': 'Get_Reacheable_Waypoint'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Entity', 'output_value': 'position'})

			# x:95 y:341
			OperatableStateMachine.add('getDistance2D',
										getDistance2D(),
										transitions={'done': 'processFollowDistance'},
										autonomy={'done': Autonomy.Off},
										remapping={'point1': 'position', 'point2': 'sara_position', 'distance': 'distance'})

			# x:105 y:186
			OperatableStateMachine.add('Get_Robot_Pose',
										Get_Robot_Pose(),
										transitions={'done': 'getPositionFromPose'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose': 'pose'})

			# x:89 y:259
			OperatableStateMachine.add('getPositionFromPose',
										CalculationState(calculation=lambda x: x.position),
										transitions={'done': 'getDistance2D'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'pose', 'output_value': 'sara_position'})

			# x:41 y:500
			OperatableStateMachine.add('Get_Reacheable_Waypoint',
										Get_Reacheable_Waypoint(),
										transitions={'done': 'lo'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose_in': 'position', 'distance': 'distance', 'pose_out': 'TargetPose'})

			# x:100 y:42
			OperatableStateMachine.add('GetEntityByID',
										GetEntityByID(),
										transitions={'found': 'getPositionFromEntity', 'not_found': 'not_found'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ID': 'ID', 'Entity': 'Entity'})

			# x:294 y:456
			OperatableStateMachine.add('lo',
										LogKeyState(text="send {}", severity=Logger.REPORT_HINT),
										transitions={'done': 'update'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'TargetPose'})

			# x:97 y:418
			OperatableStateMachine.add('processFollowDistance',
										processFollowDistance(minimum_distance=1, divisor_distance=2, threshold=.5),
										transitions={'move': 'Get_Reacheable_Waypoint', 'done': 'Get_Reacheable_Waypoint'},
										autonomy={'move': Autonomy.Off, 'done': Autonomy.Off},
										remapping={'distance_of_target': 'distance', 'distance': 'distance'})


		# x:130 y:365
		_sm_group_1 = OperatableStateMachine(outcomes=['failed'], input_keys=['TargetPose'], output_keys=['TargetPose'])

		with _sm_group_1:
			# x:124 y:145
			OperatableStateMachine.add('move',
										SaraMoveBase(),
										transitions={'arrived': 'failed', 'failed': 'failed'},
										autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'TargetPose'})


		# x:257 y:158, x:87 y:246, x:246 y:82, x:37 y:281
		_sm_group_3_2 = ConcurrencyContainer(outcomes=['not_found', 'updatePose'], input_keys=['ID', 'TargetPose', 'distance'], output_keys=['TargetPose'], conditions=[
										('not_found', [('Group_2', 'not_found')]),
										('updatePose', [('Group_2', 'update'), ('Group', 'failed')])
										])

		with _sm_group_3_2:
			# x:389 y:52
			OperatableStateMachine.add('Group',
										_sm_group_1,
										transitions={'failed': 'updatePose'},
										autonomy={'failed': Autonomy.Inherit},
										remapping={'TargetPose': 'TargetPose'})

			# x:58 y:121
			OperatableStateMachine.add('Group_2',
										_sm_group_2_0,
										transitions={'not_found': 'not_found', 'update': 'updatePose'},
										autonomy={'not_found': Autonomy.Inherit, 'update': Autonomy.Inherit},
										remapping={'ID': 'ID', 'TargetPose': 'TargetPose', 'distance': 'distance'})



		with _state_machine:
			# x:95 y:26
			OperatableStateMachine.add('En',
										GetEntityByID(),
										transitions={'found': 'dist', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ID': 'ID', 'Entity': 'Entity'})

			# x:300 y:408
			OperatableStateMachine.add('log',
										LogKeyState(text="{}", severity=Logger.REPORT_HINT),
										transitions={'done': 'Group_3'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'TargetPose'})

			# x:77 y:212
			OperatableStateMachine.add('pos',
										CalculationState(calculation=lambda x: x.position),
										transitions={'done': 're'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Entity', 'output_value': 'TargetPose'})

			# x:287 y:299
			OperatableStateMachine.add('Group_3',
										_sm_group_3_2,
										transitions={'not_found': 'failed', 'updatePose': 'log'},
										autonomy={'not_found': Autonomy.Inherit, 'updatePose': Autonomy.Inherit},
										remapping={'ID': 'ID', 'TargetPose': 'TargetPose', 'distance': 'distance'})

			# x:47 y:307
			OperatableStateMachine.add('re',
										Get_Reacheable_Waypoint(),
										transitions={'done': 'Group_3'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose_in': 'TargetPose', 'distance': 'distance', 'pose_out': 'TargetPose'})

			# x:90 y:113
			OperatableStateMachine.add('dist',
										SetKey(Value=1),
										transitions={'done': 'pos'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'distance'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
