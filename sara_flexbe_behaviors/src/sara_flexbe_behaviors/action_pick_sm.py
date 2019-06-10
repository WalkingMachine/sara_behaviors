#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.SetSegmentationRosParam import SetSegmentationRosParam
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.Get_Entity_By_ID import GetEntityByID
from sara_flexbe_states.KeepLookingAt import KeepLookingAt
from flexbe_states.wait_state import WaitState
from sara_flexbe_states.run_trajectory import RunTrajectory
from sara_flexbe_states.set_gripper_state import SetGripperState
from sara_flexbe_states.moveit_move import MoveitMove
from sara_flexbe_states.gen_gripper_pose import GenGripperPose
from sara_flexbe_states.pose_gen_euler import GenPoseEuler
from sara_flexbe_states.sara_move_base import SaraMoveBase
from sara_flexbe_states.GetGraspFromEntity import GetGraspFromEntity
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

		# O 508 126 
		# avec la position de objet connu, bouge le gripper, ouvre et ferme sur objet



	def create(self):
		# x:929 y:479, x:925 y:237, x:922 y:34, x:926 y:362
		_state_machine = OperatableStateMachine(outcomes=['success', 'unreachable', 'not found', 'dropped'], input_keys=['objectID'])
		_state_machine.userdata.objectID = 169
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


		# x:280 y:183, x:92 y:289
		_sm_get_on_it_1 = OperatableStateMachine(outcomes=['failed', 'done'], input_keys=['grasp_pose'])

		with _sm_get_on_it_1:
			# x:76 y:26
			OperatableStateMachine.add('open gripper',
										SetGripperState(width=0.1, effort=0),
										transitions={'object': 'move on it', 'no_object': 'move on it'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:66 y:170
			OperatableStateMachine.add('move on it',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'done', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'grasp_pose'})


		# x:30 y:324, x:130 y:324
		_sm_get_away_from_failure_2 = OperatableStateMachine(outcomes=['done', 'failed'])

		with _sm_get_away_from_failure_2:
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
		_sm_lift_object_3 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['grasp_pose'])

		with _sm_lift_object_3:
			# x:30 y:40
			OperatableStateMachine.add('gen up pose',
										GenGripperPose(l=0, z=0.1, planar=False),
										transitions={'done': 'move_lift_object', 'fail': 'failed'},
										autonomy={'done': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'pose_in': 'grasp_pose', 'pose_out': 'up_pose'})

			# x:40 y:266
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

			# x:48 y:151
			OperatableStateMachine.add('move_lift_object',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'genpose', 'failed': 'genpose'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'up_pose'})

			# x:39 y:480
			OperatableStateMachine.add('place arm',
										RunTrajectory(file="transport", duration=0),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off})


		# x:263 y:214, x:271 y:492
		_sm_validation_and_approach_4 = OperatableStateMachine(outcomes=['failed', 'done'], input_keys=['grasp_pose', 'approach_pose'])

		with _sm_validation_and_approach_4:
			# x:85 y:30
			OperatableStateMachine.add('checkifposeaccess',
										MoveitMove(move=False, waitForExecution=True, group="RightArm"),
										transitions={'done': 'say can reach', 'failed': 'failed'},
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


		# x:334 y:336, x:96 y:627
		_sm_get_object_5 = OperatableStateMachine(outcomes=['not_found', 'finished'], input_keys=['objectID'], output_keys=['entity'])

		with _sm_get_object_5:
			# x:67 y:27
			OperatableStateMachine.add('start segmentation',
										SetSegmentationRosParam(ValueTableSegmentation=True, ValueObjectSegmentation=True),
										transitions={'done': 'Look at it for 3s'},
										autonomy={'done': Autonomy.Off})

			# x:70 y:508
			OperatableStateMachine.add('Say_See_It',
										SaraSay(sentence=lambda x: "I see the " + x[0].name, input_keys=["Entity"], emotion=0, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'Entity': 'entity'})

			# x:72 y:322
			OperatableStateMachine.add('getobject',
										GetEntityByID(),
										transitions={'found': 'pregrip', 'not_found': 'not_found'},
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

			# x:73 y:416
			OperatableStateMachine.add('pregrip',
										RunTrajectory(file="pre_grip_pose", duration=0),
										transitions={'done': 'Say_See_It'},
										autonomy={'done': Autonomy.Off})



		with _state_machine:
			# x:44 y:27
			OperatableStateMachine.add('Get object',
										_sm_get_object_5,
										transitions={'not_found': 'not found', 'finished': 'get grasps'},
										autonomy={'not_found': Autonomy.Inherit, 'finished': Autonomy.Inherit},
										remapping={'objectID': 'objectID', 'entity': 'entity'})

			# x:264 y:346
			OperatableStateMachine.add('gripclose',
										SetGripperState(width=0, effort=250),
										transitions={'object': 'say picked', 'no_object': 'get away from failure'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:268 y:240
			OperatableStateMachine.add('cant reach',
										SaraSay(sentence="Hum! I can't reach it.", input_keys=[], emotion=1, block=True),
										transitions={'done': 'unreachable'},
										autonomy={'done': Autonomy.Off})

			# x:267 y:452
			OperatableStateMachine.add('say picked',
										SaraSay(sentence="I think I got it", input_keys=[], emotion=1, block=False),
										transitions={'done': 'Lift object'},
										autonomy={'done': Autonomy.Off})

			# x:727 y:462
			OperatableStateMachine.add('welcome',
										SaraSay(sentence="you are welcome", input_keys=[], emotion=1, block=True),
										transitions={'done': 'success'},
										autonomy={'done': Autonomy.Off})

			# x:27 y:239
			OperatableStateMachine.add('validation and approach',
										_sm_validation_and_approach_4,
										transitions={'failed': 'cant reach', 'done': 'get on it'},
										autonomy={'failed': Autonomy.Inherit, 'done': Autonomy.Inherit},
										remapping={'grasp_pose': 'grasp_pose', 'approach_pose': 'approach_pose'})

			# x:497 y:459
			OperatableStateMachine.add('Lift object',
										_sm_lift_object_3,
										transitions={'done': 'welcome', 'failed': 'welcome'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'grasp_pose': 'grasp_pose'})

			# x:482 y:344
			OperatableStateMachine.add('get away from failure',
										_sm_get_away_from_failure_2,
										transitions={'done': 'say missed', 'failed': 'say missed'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:41 y:127
			OperatableStateMachine.add('get grasps',
										GetGraspFromEntity(approachDistance=0.2, distanceScoringMultiplier=1, orientationScoringMultiplier=2, graspScoringMultiplier=1),
										transitions={'done': 'validation and approach', 'failed': 'say cant handle'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'Entity': 'entity', 'ApproachPose': 'approach_pose', 'GraspingPose': 'grasp_pose'})

			# x:729 y:349
			OperatableStateMachine.add('say missed',
										SaraSay(sentence="Oops! I missed.", input_keys=[], emotion=2, block=True),
										transitions={'done': 'dropped'},
										autonomy={'done': Autonomy.Off})

			# x:269 y:124
			OperatableStateMachine.add('say cant handle',
										SaraSay(sentence="I don't understand how to grab it.", input_keys=[], emotion=3, block=True),
										transitions={'done': 'unreachable'},
										autonomy={'done': Autonomy.Off})

			# x:49 y:350
			OperatableStateMachine.add('get on it',
										_sm_get_on_it_1,
										transitions={'failed': 'cant reach', 'done': 'gripclose'},
										autonomy={'failed': Autonomy.Inherit, 'done': Autonomy.Inherit},
										remapping={'grasp_pose': 'grasp_pose'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
