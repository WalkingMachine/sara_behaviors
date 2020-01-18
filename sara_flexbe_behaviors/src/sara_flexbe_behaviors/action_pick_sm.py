#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_states.set_gripper_state import SetGripperState
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.moveit_move import MoveitMove
from sara_flexbe_states.moveit_moveCartesian import MoveitMoveCartesian
from sara_flexbe_states.run_trajectory import RunTrajectory
from sara_flexbe_states.pose_gen_euler import GenPoseEuler
from sara_flexbe_states.sara_move_base import SaraMoveBase
from sara_flexbe_states.GetGraspFromEntity import GetGraspFromEntity
from sara_flexbe_states.gen_gripper_pose import GenGripperPose
from sara_flexbe_states.GetAttribute import GetAttribute
from sara_flexbe_states.get_reachable_waypoint import Get_Reacheable_Waypoint
from sara_flexbe_states.for_loop_with_input import ForLoopWithInput
from sara_flexbe_states.SetSegmentationRosParam import SetSegmentationRosParam
from sara_flexbe_states.Get_Entity_By_ID import GetEntityByID
from sara_flexbe_states.KeepLookingAt import KeepLookingAt
from flexbe_states.wait_state import WaitState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on May 12 2018
@author: Huynh-Anh Le
'''
class Action_pickSM(Behavior):
	'''
	Try to pick an object
	'''


	def __init__(self):
		super(Action_pickSM, self).__init__()
		self.name = 'Action_pick'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:

		# O 377 4 
		# prend ID de objet, on verifie sil est accessible ou non en calculant sa position

		# O 594 142 
		# avec la position de objet connu, bouge le gripper, ouvre et ferme sur objet



	def create(self):
		# x:960 y:715, x:912 y:318, x:904 y:185, x:941 y:610
		_state_machine = OperatableStateMachine(outcomes=['success', 'unreachable', 'not found', 'dropped'], input_keys=['objectID'])
		_state_machine.userdata.objectID = 60
		_state_machine.userdata.PreGripPose = "pre_grip_pose"
		_state_machine.userdata.entity = 0
		_state_machine.userdata.grasp_pose = 0
		_state_machine.userdata.approach_pose = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:30 y:365, x:130 y:365, x:230 y:365
		_sm_look_at_it_for_3s_0 = ConcurrencyContainer(outcomes=['done'], input_keys=['ID'], conditions=[
										('done', [('look', 'failed')]),
										('done', [('wait', 'done')])
										])

		with _sm_look_at_it_for_3s_0:
			# x:30 y:54
			OperatableStateMachine.add('look',
										KeepLookingAt(),
										transitions={'failed': 'done'},
										autonomy={'failed': Autonomy.Off},
										remapping={'ID': 'ID'})

			# x:187 y:111
			OperatableStateMachine.add('wait',
										WaitState(wait_time=6),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off})


		# x:334 y:336, x:96 y:627
		_sm_get_object_1 = OperatableStateMachine(outcomes=['not_found', 'finished'], input_keys=['objectID'], output_keys=['entity'])

		with _sm_get_object_1:
			# x:67 y:27
			OperatableStateMachine.add('start segmentation',
										SetSegmentationRosParam(ValueTableSegmentation=True, ValueObjectSegmentation=True),
										transitions={'done': 'Look at it for 3s'},
										autonomy={'done': Autonomy.Off})

			# x:61 y:410
			OperatableStateMachine.add('Say_See_It',
										SaraSay(sentence=lambda x: "I see the " + x[0].name, input_keys=["Entity"], emotion=0, block=True),
										transitions={'done': 'pregrip'},
										autonomy={'done': Autonomy.Off},
										remapping={'Entity': 'entity'})

			# x:72 y:322
			OperatableStateMachine.add('getobject',
										GetEntityByID(),
										transitions={'found': 'Say_See_It', 'not_found': 'not_found'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ID': 'objectID', 'Entity': 'entity'})

			# x:62 y:224
			OperatableStateMachine.add('stop segmentation',
										SetSegmentationRosParam(ValueTableSegmentation=False, ValueObjectSegmentation=False),
										transitions={'done': 'getobject'},
										autonomy={'done': Autonomy.Off})

			# x:70 y:122
			OperatableStateMachine.add('Look at it for 3s',
										_sm_look_at_it_for_3s_0,
										transitions={'done': 'stop segmentation'},
										autonomy={'done': Autonomy.Inherit},
										remapping={'ID': 'objectID'})

			# x:57 y:513
			OperatableStateMachine.add('pregrip',
										RunTrajectory(file="pre_grip_pose", duration=5),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		# x:153 y:506, x:350 y:396
		_sm_get_closer_2 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['entity'])

		with _sm_get_closer_2:
			# x:120 y:61
			OperatableStateMachine.add('set distance',
										SetKey(Value=0.6),
										transitions={'done': 'get att'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'distance'})

			# x:113 y:172
			OperatableStateMachine.add('get att',
										GetAttribute(attributes=["position"]),
										transitions={'done': 'get waypoint'},
										autonomy={'done': Autonomy.Off},
										remapping={'object': 'entity', 'position': 'position'})

			# x:116 y:390
			OperatableStateMachine.add('move to waypoint',
										SaraMoveBase(reference="map"),
										transitions={'arrived': 'finished', 'failed': 'failed'},
										autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'pose'})

			# x:107 y:272
			OperatableStateMachine.add('get waypoint',
										Get_Reacheable_Waypoint(),
										transitions={'done': 'move to waypoint'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose_in': 'position', 'distance': 'distance', 'pose_out': 'pose'})


		# x:280 y:183, x:92 y:289
		_sm_get_on_it_3 = OperatableStateMachine(outcomes=['failed', 'done'], input_keys=['grasp_pose'])

		with _sm_get_on_it_3:
			# x:76 y:26
			OperatableStateMachine.add('open gripper',
										SetGripperState(width=0.1, effort=0),
										transitions={'object': 'move forward', 'no_object': 'move forward'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:64 y:158
			OperatableStateMachine.add('move forward',
										MoveitMoveCartesian(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'done', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'targetPose': 'grasp_pose'})


		# x:30 y:324, x:130 y:324
		_sm_get_away_from_failure_4 = OperatableStateMachine(outcomes=['done', 'failed'])

		with _sm_get_away_from_failure_4:
			# x:30 y:40
			OperatableStateMachine.add('open 2',
										SetGripperState(width=0.1, effort=1),
										transitions={'object': 'go back', 'no_object': 'go back'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:44 y:167
			OperatableStateMachine.add('go back',
										RunTrajectory(file="pre_grip_pose", duration=0),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off})


		# x:68 y:579, x:349 y:211
		_sm_lift_object_5 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['approach_pose', 'up_pose'])

		with _sm_lift_object_5:
			# x:45 y:34
			OperatableStateMachine.add('move up',
										MoveitMoveCartesian(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'genpose', 'failed': 'genpose'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'targetPose': 'up_pose'})

			# x:39 y:480
			OperatableStateMachine.add('place arm',
										RunTrajectory(file="transport", duration=0),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off})

			# x:40 y:144
			OperatableStateMachine.add('genpose',
										GenPoseEuler(x=-0.2, y=0, z=0, roll=0, pitch=0, yaw=0),
										transitions={'done': 'move_back'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose': 'backPose'})

			# x:42 y:382
			OperatableStateMachine.add('move_back',
										SaraMoveBase(reference="base_link"),
										transitions={'arrived': 'place arm', 'failed': 'place arm'},
										autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'backPose'})


		# x:263 y:214, x:271 y:492
		_sm_validation_and_approach_6 = OperatableStateMachine(outcomes=['failed', 'done'], input_keys=['grasp_pose', 'approach_pose'])

		with _sm_validation_and_approach_6:
			# x:85 y:30
			OperatableStateMachine.add('checkifposeaccess',
										MoveitMove(move=False, waitForExecution=True, group="RightArm"),
										transitions={'done': 'say can reach', 'failed': 'sayapp'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'grasp_pose'})

			# x:48 y:236
			OperatableStateMachine.add('move approach',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'done', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'approach_pose'})

			# x:71 y:115
			OperatableStateMachine.add('say can reach',
										SaraSay(sentence="I will grab it", input_keys=[], emotion=1, block=False),
										transitions={'done': 'move approach'},
										autonomy={'done': Autonomy.Off})

			# x:342 y:93
			OperatableStateMachine.add('sayapp',
										SaraSay(sentence="unreachable", input_keys=[], emotion=0, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})



		with _state_machine:
			# x:40 y:26
			OperatableStateMachine.add('start loop',
										SetKey(Value=0),
										transitions={'done': 'Get object'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'i'})

			# x:256 y:616
			OperatableStateMachine.add('gripclose',
										SetGripperState(width=0, effort=250),
										transitions={'object': 'say picked', 'no_object': 'get away from failure'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:255 y:507
			OperatableStateMachine.add('cant reach',
										SaraSay(sentence="Hum! I can't reach it.", input_keys=[], emotion=1, block=True),
										transitions={'done': 'for 2 try'},
										autonomy={'done': Autonomy.Off})

			# x:261 y:732
			OperatableStateMachine.add('say picked',
										SaraSay(sentence="I think I got it", input_keys=[], emotion=1, block=False),
										transitions={'done': 'Lift object'},
										autonomy={'done': Autonomy.Off})

			# x:751 y:715
			OperatableStateMachine.add('welcome',
										SaraSay(sentence="you are welcome", input_keys=[], emotion=1, block=True),
										transitions={'done': 'success'},
										autonomy={'done': Autonomy.Off})

			# x:9 y:403
			OperatableStateMachine.add('validation and approach',
										_sm_validation_and_approach_6,
										transitions={'failed': 'say plan', 'done': 'gen up pose'},
										autonomy={'failed': Autonomy.Inherit, 'done': Autonomy.Inherit},
										remapping={'grasp_pose': 'grasp_pose', 'approach_pose': 'approach_pose'})

			# x:516 y:717
			OperatableStateMachine.add('Lift object',
										_sm_lift_object_5,
										transitions={'done': 'welcome', 'failed': 'welcome'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'approach_pose': 'approach_pose', 'up_pose': 'up_pose'})

			# x:480 y:609
			OperatableStateMachine.add('get away from failure',
										_sm_get_away_from_failure_4,
										transitions={'done': 'say missed', 'failed': 'say missed'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:25 y:311
			OperatableStateMachine.add('get grasps',
										GetGraspFromEntity(approachDistance=0.2, distanceScoringMultiplier=1, orientationScoringMultiplier=2, graspScoringMultiplier=1),
										transitions={'done': 'validation and approach', 'failed': 'say cant handle'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'Entity': 'entity', 'ApproachPose': 'approach_pose', 'GraspingPose': 'grasp_pose'})

			# x:738 y:602
			OperatableStateMachine.add('say missed',
										SaraSay(sentence="Oops! I missed.", input_keys=[], emotion=2, block=True),
										transitions={'done': 'dropped'},
										autonomy={'done': Autonomy.Off})

			# x:257 y:279
			OperatableStateMachine.add('say cant handle',
										SaraSay(sentence="I don't understand how to grab it.", input_keys=[], emotion=3, block=True),
										transitions={'done': 'for 2 try'},
										autonomy={'done': Autonomy.Off})

			# x:18 y:605
			OperatableStateMachine.add('get on it',
										_sm_get_on_it_3,
										transitions={'failed': 'cant reach', 'done': 'gripclose'},
										autonomy={'failed': Autonomy.Inherit, 'done': Autonomy.Inherit},
										remapping={'grasp_pose': 'grasp_pose'})

			# x:261 y:387
			OperatableStateMachine.add('say plan',
										SaraSay(sentence="Planing failed", input_keys=[], emotion=0, block=True),
										transitions={'done': 'for 2 try'},
										autonomy={'done': Autonomy.Off})

			# x:20 y:496
			OperatableStateMachine.add('gen up pose',
										GenGripperPose(l=0, z=0.1, planar=False),
										transitions={'done': 'get on it', 'fail': 'cant reach'},
										autonomy={'done': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'pose_in': 'grasp_pose', 'pose_out': 'up_pose'})

			# x:558 y:231
			OperatableStateMachine.add('get closer',
										_sm_get_closer_2,
										transitions={'finished': 'Get object', 'failed': 'unreachable'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'entity': 'entity'})

			# x:553 y:390
			OperatableStateMachine.add('for 2 try',
										ForLoopWithInput(repeat=1),
										transitions={'do': 'get closer', 'end': 'unreachable'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index_in': 'i', 'index_out': 'i'})

			# x:28 y:217
			OperatableStateMachine.add('Get object',
										_sm_get_object_1,
										transitions={'not_found': 'not found', 'finished': 'get grasps'},
										autonomy={'not_found': Autonomy.Inherit, 'finished': Autonomy.Inherit},
										remapping={'objectID': 'objectID', 'entity': 'entity'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
