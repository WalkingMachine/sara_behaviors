#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.GetRosParam import GetRosParam
from sara_flexbe_behaviors.action_place_sm import Action_placeSM
from sara_flexbe_states.pose_gen_euler import GenPoseEuler
from sara_flexbe_states.TF_transform import TF_transformation
from flexbe_states.check_condition_state import CheckConditionState
from sara_flexbe_states.sara_say import SaraSay
from flexbe_states.flexible_calculation_state import FlexibleCalculationState
from flexbe_states.log_state import LogState
from flexbe_states.log_key_state import LogKeyState
from sara_flexbe_states.SetRosParam import SetRosParam
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_states.moveit_move import MoveitMove
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Tue Jul 11 2017
@author: Philippe La Madeleine
'''
class ActionWrapper_PlaceSM(Behavior):
	'''
	action wrapper pour place
	'''


	def __init__(self):
		super(ActionWrapper_PlaceSM, self).__init__()
		self.name = 'ActionWrapper_Place'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(Action_placeSM, 'Action_place')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
        
        # [/MANUAL_INIT]

		# Behavior comments:

		# O 369 2 
		# Place|n1- where to put the object

		# O 588 404 
		# Chercher un objet de type container (le plus proche?) et se deplacer la bas



	def create(self):
		# x:702 y:576, x:764 y:158, x:766 y:33
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'critical_fail'], input_keys=['Action'])
		_state_machine.userdata.Action = ["Place", "table"]
		_state_machine.userdata.Empty = None
		_state_machine.userdata.IdlePos = "IdlePose"

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


		with _state_machine:
			# x:44 y:28
			OperatableStateMachine.add('gripper contain',
										GetRosParam(ParamName="behavior/GripperContent"),
										transitions={'done': 'if contain something', 'failed': 'cause1'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'Value': 'content'})

			# x:222 y:497
			OperatableStateMachine.add('Action_place',
										self.use_behavior(Action_placeSM, 'Action_place'),
										transitions={'finished': 'idlearm', 'failed': 'cause3'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pos': 'MapPosition'})

			# x:39 y:367
			OperatableStateMachine.add('genPoseArm',
										GenPoseEuler(x=0.75, y=-0.25, z=0.85, roll=0, pitch=0, yaw=0),
										transitions={'done': 'referential from robot to map'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose': 'position'})

			# x:8 y:433
			OperatableStateMachine.add('referential from robot to map',
										TF_transformation(in_ref="base_link", out_ref="map"),
										transitions={'done': 'log pose', 'fail': 'log tf error'},
										autonomy={'done': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'in_pos': 'position', 'out_pos': 'MapPosition'})

			# x:25 y:98
			OperatableStateMachine.add('if contain something',
										CheckConditionState(predicate=lambda x: x != ''),
										transitions={'true': 'cond', 'false': 'say nothing in gripper'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'content'})

			# x:209 y:98
			OperatableStateMachine.add('say nothing in gripper',
										SaraSay(sentence="It seems I have nothing in my gripper", input_keys=[], emotion=1, block=True),
										transitions={'done': 'cause1'},
										autonomy={'done': Autonomy.Off})

			# x:28 y:236
			OperatableStateMachine.add('construction phrase',
										FlexibleCalculationState(calculation=lambda x: "I will place this "+str(x[0])+" on the "+str(x[1][1]), input_keys=["content", "Action"]),
										transitions={'done': 'Say_Place_object'},
										autonomy={'done': Autonomy.Off},
										remapping={'content': 'content', 'Action': 'Action', 'output_value': 'sentence'})

			# x:33 y:167
			OperatableStateMachine.add('cond',
										CheckConditionState(predicate=lambda x: x[1] != ''),
										transitions={'true': 'construction phrase', 'false': 'cause2'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'Action'})

			# x:257 y:413
			OperatableStateMachine.add('log tf error',
										LogState(text="tf error", severity=Logger.REPORT_HINT),
										transitions={'done': 'cause3'},
										autonomy={'done': Autonomy.Off})

			# x:42 y:502
			OperatableStateMachine.add('log pose',
										LogKeyState(text="the placement pose will be: {}", severity=Logger.REPORT_HINT),
										transitions={'done': 'Action_place'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'MapPosition'})

			# x:493 y:535
			OperatableStateMachine.add('empty hand',
										SetRosParam(ParamName="behavior/GripperContent"),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'Value': 'Empty'})

			# x:448 y:54
			OperatableStateMachine.add('cause1',
										SetKey(Value="I didn't have any object in my gripper"),
										transitions={'done': 'setrosparamcause'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Key'})

			# x:422 y:149
			OperatableStateMachine.add('cause2',
										SetKey(Value="I didn't know where to place the object."),
										transitions={'done': 'setrosparamcause'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Key'})

			# x:575 y:158
			OperatableStateMachine.add('setrosparamcause',
										SetRosParam(ParamName="behavior/GPSR/CauseOfFailure"),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off},
										remapping={'Value': 'Key'})

			# x:449 y:325
			OperatableStateMachine.add('cause3',
										SetKey(Value="I was unable to calculate how to place the object."),
										transitions={'done': 'setrosparamcause'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Key'})

			# x:342 y:583
			OperatableStateMachine.add('idlearm',
										MoveitMove(move=True, waitForExecution=False, group="RightArm", watchdog=15),
										transitions={'done': 'empty hand', 'failed': 'empty hand'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'IdlePos'})

			# x:706 y:460
			OperatableStateMachine.add('Say_Place_It_This_Place',
										SaraSay(sentence=lambda x: "I will place this "+x+" right there.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:35 y:301
			OperatableStateMachine.add('Say_Place_object',
										SaraSay(sentence=lambda x: x, input_keys=[], emotion=0, block=True),
										transitions={'done': 'genPoseArm'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
