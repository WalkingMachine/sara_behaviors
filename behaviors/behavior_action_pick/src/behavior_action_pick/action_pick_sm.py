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

		# O 252 95 
		# prend ID de objet, on verifie sil est accessible ou non en calculant sa position

		# O 401 310 
		# avec la position de objet connu, bouge le gripper, ouvre et ferme sur objet



	def create(self):
		# x:801 y:536, x:47 y:594, x:19 y:425, x:756 y:642
		_state_machine = OperatableStateMachine(outcomes=['success', 'unreachable', 'not found', 'dropped'], input_keys=['objectID'])
		_state_machine.userdata.objectID = 0
		_state_machine.userdata.PreGripPose = "PreGripPose"
		_state_machine.userdata.PostGripPose = "PostGripPose"

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


		with _state_machine:
			# x:44 y:30
			OperatableStateMachine.add('getobject',
										GetEntityByID(),
										transitions={'found': 'getpose', 'not_found': 'not found'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ID': 'objectID', 'Entity': 'Entity'})

			# x:102 y:178
			OperatableStateMachine.add('gripper',
										GenGripperPose(l=0.0),
										transitions={'done': 'checkifposeaccess'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose_in': 'posobjet', 'pose_out': 'grippose'})

			# x:142 y:248
			OperatableStateMachine.add('checkifposeaccess',
										MoveitMove(move=False, waitForExecution=True, group="RightArm"),
										transitions={'done': 'movearm1', 'failed': 'unreachable'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'grippose'})

			# x:335 y:437
			OperatableStateMachine.add('gripperopen',
										SetGripperState(width=0.15, effort=1),
										transitions={'object': 'movetopose', 'no_object': 'movetopose'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:186 y:329
			OperatableStateMachine.add('movearm1',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'getapproach', 'failed': 'unreachable'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'PreGripPose'})

			# x:507 y:479
			OperatableStateMachine.add('gripclose',
										SetGripperState(width=0, effort=1),
										transitions={'object': 'success', 'no_object': 'dropped'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:52 y:109
			OperatableStateMachine.add('getpose',
										CalculationState(calculation=lambda x: x.position),
										transitions={'done': 'gripper'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Entity', 'output_value': 'posobjet'})

			# x:191 y:487
			OperatableStateMachine.add('movearm2',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'gripperopen', 'failed': 'unreachable'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'pose_app'})

			# x:181 y:410
			OperatableStateMachine.add('getapproach',
										GenGripperPose(l=0.25),
										transitions={'done': 'movearm2'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose_in': 'posobjet', 'pose_out': 'pose_app'})

			# x:388 y:568
			OperatableStateMachine.add('movetopose',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'gripclose', 'failed': 'unreachable'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'grippose'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
