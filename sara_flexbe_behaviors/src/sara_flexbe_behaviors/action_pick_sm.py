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
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.KeepLookingAt import KeepLookingAt
from flexbe_states.wait_state import WaitState
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.set_gripper_state import SetGripperState
from sara_flexbe_states.moveit_move import MoveitMove
from sara_flexbe_states.gen_gripper_pose import GenGripperPose
from sara_flexbe_states.TF_transform import TF_transformation
from sara_flexbe_states.pose_gen_euler import GenPoseEuler
from sara_flexbe_states.sara_rel_move_base import SaraRelMoveBase
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

		# O 396 28 
		# prend ID de objet, on verifie sil est accessible ou non en calculant sa position

		# O 467 163 
		# avec la position de objet connu, bouge le gripper, ouvre et ferme sur objet



	def create(self):
		# x:934 y:534, x:520 y:222, x:335 y:32, x:926 y:585
		_state_machine = OperatableStateMachine(outcomes=['success', 'unreachable', 'not found', 'dropped'], input_keys=['objectID', 'Entity'])
		_state_machine.userdata.objectID = 1585
		_state_machine.userdata.PreGripPose = "PreGripPose"
		_state_machine.userdata.PostGripPose = "PostGripPose"
		_state_machine.userdata.Entity = 0

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
										WaitState(wait_time=3),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off})


		# x:499 y:227, x:263 y:214, x:271 y:492
		_sm_pregrip_1 = OperatableStateMachine(outcomes=['fail', 'failed', 'done'], input_keys=['PreGripPose', 'posobjet'], output_keys=['pose_app', 'grippose', 'pose_lift', 'pose_ret'])

		with _sm_pregrip_1:
			# x:70 y:40
			OperatableStateMachine.add('gen_gripPose',
										GenGripperPose(l=0.0, z=0, planar=True),
										transitions={'done': 'checkifposeaccess', 'fail': 'fail'},
										autonomy={'done': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'pose_in': 'posobjet', 'pose_out': 'grippose'})

			# x:56 y:256
			OperatableStateMachine.add('move_PreGrip',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'gen_returnPose', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'PreGripPose'})

			# x:30 y:398
			OperatableStateMachine.add('gen_approachPose',
										GenGripperPose(l=0.15, z=0, planar=True),
										transitions={'done': 'gen_liftPose', 'fail': 'fail'},
										autonomy={'done': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'pose_in': 'posobjet', 'pose_out': 'pose_app'})

			# x:40 y:469
			OperatableStateMachine.add('gen_liftPose',
										GenGripperPose(l=0, z=0.1, planar=True),
										transitions={'done': 'done', 'fail': 'fail'},
										autonomy={'done': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'pose_in': 'posobjet', 'pose_out': 'pose_lift'})

			# x:43 y:326
			OperatableStateMachine.add('gen_returnPose',
										GenGripperPose(l=0.2, z=0.1, planar=True),
										transitions={'done': 'gen_approachPose', 'fail': 'fail'},
										autonomy={'done': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'pose_in': 'posobjet', 'pose_out': 'pose_ret'})

			# x:63 y:184
			OperatableStateMachine.add('say can reach',
										SaraSay(sentence="I will grab it", input_keys=[], emotion=1, block=False),
										transitions={'done': 'move_PreGrip'},
										autonomy={'done': Autonomy.Off})

			# x:58 y:114
			OperatableStateMachine.add('checkifposeaccess',
										MoveitMove(move=False, waitForExecution=True, group="RightArm"),
										transitions={'done': 'say can reach', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'grippose'})


		# x:315 y:40, x:130 y:465
		_sm_get_object_2 = OperatableStateMachine(outcomes=['not_found', 'finished'], input_keys=['objectID'], output_keys=['posobjet'])

		with _sm_get_object_2:
			# x:55 y:40
			OperatableStateMachine.add('getobject',
										GetEntityByID(),
										transitions={'found': 'Say_See_It', 'not_found': 'not_found'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ID': 'objectID', 'Entity': 'Entity'})

			# x:77 y:370
			OperatableStateMachine.add('getpose',
										CalculationState(calculation=lambda x: x.position),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Entity', 'output_value': 'posobjet'})

			# x:71 y:262
			OperatableStateMachine.add('Look at it for 3s',
										_sm_look_at_it_for_3s_0,
										transitions={'done': 'getpose'},
										autonomy={'done': Autonomy.Inherit},
										remapping={'ID': 'objectID'})

			# x:31 y:133
			OperatableStateMachine.add('Say_See_It',
										SaraSay(sentence=lambda x: "I see the " + x.name, input_keys=["Entity"], emotion=0, block=True),
										transitions={'done': 'Look at it for 3s'},
										autonomy={'done': Autonomy.Off},
										remapping={'Entity': 'Entity'})



		with _state_machine:
			# x:77 y:23
			OperatableStateMachine.add('Get object',
										_sm_get_object_2,
										transitions={'not_found': 'not found', 'finished': 'transform point'},
										autonomy={'not_found': Autonomy.Inherit, 'finished': Autonomy.Inherit},
										remapping={'objectID': 'objectID', 'posobjet': 'posobjet'})

			# x:47 y:279
			OperatableStateMachine.add('gripperopen',
										SetGripperState(width=0.15, effort=1),
										transitions={'object': 'move_approach', 'no_object': 'move_approach'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:237 y:523
			OperatableStateMachine.add('gripclose',
										SetGripperState(width=0, effort=250),
										transitions={'object': 'say picked', 'no_object': 'open 2'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:41 y:368
			OperatableStateMachine.add('move_approach',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'almost have it', 'failed': 'almost have it'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'pose_app'})

			# x:40 y:520
			OperatableStateMachine.add('move_on_object',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'gripclose', 'failed': 'cant reach'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'grippose'})

			# x:420 y:450
			OperatableStateMachine.add('move_lift_object',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'genpose', 'failed': 'genpose'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'pose_lift'})

			# x:864 y:371
			OperatableStateMachine.add('move_PostGrip',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'welcome', 'failed': 'unreachable'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'PostGripPose'})

			# x:618 y:450
			OperatableStateMachine.add('move_Return',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'move_PostGrip', 'failed': 'move_PostGrip'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'pose_ret'})

			# x:623 y:538
			OperatableStateMachine.add('move back',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'dropped', 'failed': 'dropped'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'PostGripPose'})

			# x:418 y:528
			OperatableStateMachine.add('open 2',
										SetGripperState(width=0.1, effort=1),
										transitions={'object': 'move back', 'no_object': 'move back'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:277 y:200
			OperatableStateMachine.add('cant reach',
										SaraSay(sentence="Hum. I can't reach it.", input_keys=[], emotion=1, block=True),
										transitions={'done': 'unreachable'},
										autonomy={'done': Autonomy.Off})

			# x:253 y:448
			OperatableStateMachine.add('say picked',
										SaraSay(sentence="I think I got it", input_keys=[], emotion=1, block=False),
										transitions={'done': 'move_lift_object'},
										autonomy={'done': Autonomy.Off})

			# x:50 y:443
			OperatableStateMachine.add('almost have it',
										SaraSay(sentence="I am close", input_keys=[], emotion=1, block=True),
										transitions={'done': 'move_on_object'},
										autonomy={'done': Autonomy.Off})

			# x:888 y:464
			OperatableStateMachine.add('welcome',
										SaraSay(sentence="you are welcome", input_keys=[], emotion=1, block=True),
										transitions={'done': 'success'},
										autonomy={'done': Autonomy.Off})

			# x:62 y:190
			OperatableStateMachine.add('PreGrip',
										_sm_pregrip_1,
										transitions={'fail': 'cant reach', 'failed': 'cant reach', 'done': 'gripperopen'},
										autonomy={'fail': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'done': Autonomy.Inherit},
										remapping={'PreGripPose': 'PreGripPose', 'posobjet': 'posobjet', 'pose_app': 'pose_app', 'grippose': 'grippose', 'pose_lift': 'pose_lift', 'pose_ret': 'pose_ret'})

			# x:67 y:114
			OperatableStateMachine.add('transform point',
										TF_transformation(in_ref="map", out_ref="base_link"),
										transitions={'done': 'PreGrip', 'fail': 'Get object'},
										autonomy={'done': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'in_pos': 'posobjet', 'out_pos': 'posobjet'})

			# x:428 y:319
			OperatableStateMachine.add('genpose',
										GenPoseEuler(x=-0.2, y=0, z=0, roll=0, pitch=0, yaw=0),
										transitions={'done': 'moveback'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose': 'backPose'})

			# x:611 y:321
			OperatableStateMachine.add('moveback',
										SaraRelMoveBase(),
										transitions={'arrived': 'move_PostGrip', 'failed': 'unreachable'},
										autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'backPose'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
