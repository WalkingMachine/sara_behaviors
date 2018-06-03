#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_action_pick')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.Get_Entity_By_ID import GetEntityByID
from sara_flexbe_states.gen_gripper_pose import GenGripperPose
from sara_flexbe_states.moveit_move import MoveitMove
from sara_flexbe_states.set_gripper_state import SetGripperState
from flexbe_states.calculation_state import CalculationState
from behavior_action_look_at.action_look_at_sm import action_look_atSM
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.sara_say_key import SaraSayKey
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
		self.add_behavior(action_look_atSM, 'action_look_at')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
        
        # [/MANUAL_INIT]

		# Behavior comments:

		# O 396 28 
		# prend ID de objet, on verifie sil est accessible ou non en calculant sa position

		# O 587 288 
		# avec la position de objet connu, bouge le gripper, ouvre et ferme sur objet



	def create(self):
		# x:1475 y:650, x:563 y:437, x:295 y:42, x:1405 y:842
		_state_machine = OperatableStateMachine(outcomes=['success', 'unreachable', 'not found', 'dropped'], input_keys=['objectID'])
		_state_machine.userdata.objectID = 28
		_state_machine.userdata.PreGripPose = "PreGripPose"
		_state_machine.userdata.PostGripPose = "PostGripPose"

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


		with _state_machine:
			# x:77 y:23
			OperatableStateMachine.add('getobject',
										GetEntityByID(),
										transitions={'found': 'say see it', 'not_found': 'not found'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ID': 'objectID', 'Entity': 'Entity'})

			# x:81 y:331
			OperatableStateMachine.add('gen_gripPose',
										GenGripperPose(l=0.0, z=-0.15, planar=True),
										transitions={'done': 'checkifposeaccess', 'fail': 'cant reach'},
										autonomy={'done': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'pose_in': 'posobjet', 'pose_out': 'grippose'})

			# x:68 y:405
			OperatableStateMachine.add('checkifposeaccess',
										MoveitMove(move=False, waitForExecution=True, group="RightArm"),
										transitions={'done': 'say can reach', 'failed': 'cant reach'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'grippose'})

			# x:396 y:834
			OperatableStateMachine.add('gripperopen',
										SetGripperState(width=0.15, effort=1),
										transitions={'object': 'almost have it', 'no_object': 'almost have it'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:58 y:568
			OperatableStateMachine.add('move_PreGrip',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'gen_returnPose', 'failed': 'cant reach'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'PreGripPose'})

			# x:788 y:841
			OperatableStateMachine.add('gripclose',
										SetGripperState(width=0, effort=250),
										transitions={'object': 'say picked', 'no_object': 'open 2'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:72 y:169
			OperatableStateMachine.add('getpose',
										CalculationState(calculation=lambda x: x.position),
										transitions={'done': 'action_look_at'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Entity', 'output_value': 'posobjet'})

			# x:231 y:819
			OperatableStateMachine.add('move_approach',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'gripperopen', 'failed': 'cant reach'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'pose_app'})

			# x:64 y:720
			OperatableStateMachine.add('gen_approachPose',
										GenGripperPose(l=0.15, z=-0.12, planar=True),
										transitions={'done': 'gen_liftPose', 'fail': 'cant reach'},
										autonomy={'done': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'pose_in': 'posobjet', 'pose_out': 'pose_app'})

			# x:594 y:842
			OperatableStateMachine.add('move_on_object',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'gripclose', 'failed': 'cant reach'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'grippose'})

			# x:926 y:721
			OperatableStateMachine.add('move_lift_object',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'move_Return', 'failed': 'move_Return'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'pose_lift'})

			# x:80 y:806
			OperatableStateMachine.add('gen_liftPose',
										GenGripperPose(l=0, z=0.1, planar=True),
										transitions={'done': 'move_approach', 'fail': 'cant reach'},
										autonomy={'done': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'pose_in': 'posobjet', 'pose_out': 'pose_lift'})

			# x:1226 y:669
			OperatableStateMachine.add('move_PostGrip',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'welcome', 'failed': 'unreachable'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'PostGripPose'})

			# x:1087 y:706
			OperatableStateMachine.add('move_Return',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'move_PostGrip', 'failed': 'move_PostGrip'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'pose_ret'})

			# x:75 y:648
			OperatableStateMachine.add('gen_returnPose',
										GenGripperPose(l=0.2, z=0.1, planar=True),
										transitions={'done': 'gen_approachPose', 'fail': 'cant reach'},
										autonomy={'done': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'pose_in': 'posobjet', 'pose_out': 'pose_ret'})

			# x:52 y:246
			OperatableStateMachine.add('action_look_at',
										self.use_behavior(action_look_atSM, 'action_look_at'),
										transitions={'finished': 'gen_gripPose'},
										autonomy={'finished': Autonomy.Inherit},
										remapping={'Position': 'posobjet'})

			# x:1169 y:837
			OperatableStateMachine.add('move back',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'dropped', 'failed': 'dropped'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'PostGripPose'})

			# x:993 y:835
			OperatableStateMachine.add('open 2',
										SetGripperState(width=0.1, effort=1),
										transitions={'object': 'move back', 'no_object': 'move back'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:399 y:426
			OperatableStateMachine.add('cant reach',
										SaraSay(sentence="Hum. I can't reach it.", emotion=1, block=True),
										transitions={'done': 'unreachable'},
										autonomy={'done': Autonomy.Off})

			# x:794 y:763
			OperatableStateMachine.add('say picked',
										SaraSay(sentence="I think I got it", emotion=1, block=False),
										transitions={'done': 'move_lift_object'},
										autonomy={'done': Autonomy.Off})

			# x:543 y:754
			OperatableStateMachine.add('almost have it',
										SaraSay(sentence="I am close", emotion=1, block=True),
										transitions={'done': 'move_on_object'},
										autonomy={'done': Autonomy.Off})

			# x:57 y:493
			OperatableStateMachine.add('say can reach',
										SaraSay(sentence="I will grab it", emotion=1, block=False),
										transitions={'done': 'move_PreGrip'},
										autonomy={'done': Autonomy.Off})

			# x:68 y:93
			OperatableStateMachine.add('say see it',
										SaraSayKey(Format=lambda x: "I see the " + x.name, emotion=1, block=False),
										transitions={'done': 'getpose'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'Entity'})

			# x:1361 y:655
			OperatableStateMachine.add('welcome',
										SaraSay(sentence="you are welcome", emotion=1, block=True),
										transitions={'done': 'success'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
