#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_action_lookatfacebase')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.Get_direction_to_point import Get_direction_to_point
from sara_flexbe_states.sara_set_head_angle_key import SaraSetHeadAngleKey
from flexbe_states.check_condition_state import CheckConditionState
from sara_flexbe_states.pose_gen_euler_key import GenPoseEulerKey
from sara_flexbe_states.SetKey import SetKey
from flexbe_states.log_state import LogState
from behavior_action_turn.action_turn_sm import action_turnSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu Apr 26 2018
@author: Veronica Romero
'''
class action_lookAtFaceBaseSM(Behavior):
	'''
	Moves Sara's head towards the face of an entity
	'''


	def __init__(self):
		super(action_lookAtFaceBaseSM, self).__init__()
		self.name = 'action_lookAtFaceBase'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(action_turnSM, 'action_turn')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
        
        # [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:846 y:681, x:513 y:416
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['Entity'])
		_state_machine.userdata.Entity = 0
		_state_machine.userdata.yaw = 0
		_state_machine.userdata.pitch = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


		with _state_machine:
			# x:54 y:28
			OperatableStateMachine.add('ExtractPos',
										CalculationState(calculation=lambda x: x.position),
										transitions={'done': 'set zero'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Entity', 'output_value': 'Position'})

			# x:471 y:323
			OperatableStateMachine.add('direction',
										Get_direction_to_point(frame_origin="base_link", frame_reference="head_link"),
										transitions={'done': 'limit yaw', 'fail': 'failed'},
										autonomy={'done': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'targetPoint': 'Position', 'yaw': 'yaw', 'pitch': 'pitch'})

			# x:791 y:325
			OperatableStateMachine.add('InvertPitch',
										CalculationState(calculation=lambda x: max(min(-x, 0.7), -0.7)),
										transitions={'done': 'Head'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'pitch', 'output_value': 'pitch'})

			# x:795 y:478
			OperatableStateMachine.add('Head',
										SaraSetHeadAngleKey(),
										transitions={'done': 'action_turn'},
										autonomy={'done': Autonomy.Off},
										remapping={'yaw': 'zero', 'pitch': 'pitch'})

			# x:65 y:113
			OperatableStateMachine.add('if person',
										CheckConditionState(predicate=lambda x: x.name == "person"),
										transitions={'true': 'calc x', 'false': 'get pos obj'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'Entity'})

			# x:66 y:197
			OperatableStateMachine.add('calc x',
										CalculationState(calculation=lambda x: x.position.x),
										transitions={'done': 'calc y'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Entity', 'output_value': 'X'})

			# x:63 y:280
			OperatableStateMachine.add('calc y',
										CalculationState(calculation=lambda x: x.position.y),
										transitions={'done': 'if face'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Entity', 'output_value': 'Y'})

			# x:58 y:514
			OperatableStateMachine.add('calc z',
										CalculationState(calculation=lambda x: x.face.boundingBox.Center.z),
										transitions={'done': 'gen pose'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Entity', 'output_value': 'Z'})

			# x:57 y:751
			OperatableStateMachine.add('gen pose',
										GenPoseEulerKey(),
										transitions={'done': 'get pos'},
										autonomy={'done': Autonomy.Off},
										remapping={'xpos': 'X', 'ypos': 'Y', 'zpos': 'Z', 'yaw': 'zero', 'pitch': 'zero', 'roll': 'zero', 'pose': 'pose'})

			# x:208 y:31
			OperatableStateMachine.add('set zero',
										SetKey(Value=0),
										transitions={'done': 'if person'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'zero'})

			# x:293 y:752
			OperatableStateMachine.add('get pos',
										CalculationState(calculation=lambda x: x.position),
										transitions={'done': 'Look Head'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'pose', 'output_value': 'Position'})

			# x:263 y:119
			OperatableStateMachine.add('get pos obj',
										CalculationState(calculation=lambda x: x.position),
										transitions={'done': 'Look Entity'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Entity', 'output_value': 'Position'})

			# x:428 y:127
			OperatableStateMachine.add('Look Entity',
										LogState(text="Look Entity", severity=Logger.REPORT_HINT),
										transitions={'done': 'direction'},
										autonomy={'done': Autonomy.Off})

			# x:478 y:758
			OperatableStateMachine.add('Look Head',
										LogState(text="Look Head", severity=Logger.REPORT_HINT),
										transitions={'done': 'direction'},
										autonomy={'done': Autonomy.Off})

			# x:651 y:324
			OperatableStateMachine.add('limit yaw',
										CalculationState(calculation=lambda x: max(min(x, 1.5), -1.5)),
										transitions={'done': 'InvertPitch'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'yaw', 'output_value': 'yaw'})

			# x:53 y:389
			OperatableStateMachine.add('if face',
										CheckConditionState(predicate=lambda x: x.face.id != ""),
										transitions={'true': 'calc z', 'false': 'set z'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'Entity'})

			# x:244 y:405
			OperatableStateMachine.add('set z',
										SetKey(Value=1.4),
										transitions={'done': 'gen pose'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Z'})

			# x:797 y:563
			OperatableStateMachine.add('action_turn',
										self.use_behavior(action_turnSM, 'action_turn'),
										transitions={'finished': 'finished', 'failed': 'finished'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'rotation': 'yaw'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
