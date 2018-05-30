#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_action_look_at_face')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.Get_direction_to_point import Get_direction_to_point
from sara_flexbe_states.sara_set_head_angle_key import SaraSetHeadAngleKey
from flexbe_states.check_condition_state import CheckConditionState
from sara_flexbe_states.pose_gen_euler_key import GenPoseEulerKey
from sara_flexbe_states.SetKey import SetKey
from flexbe_states.log_state import LogState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu Apr 26 2018
@author: Veronica Romero
'''
class action_look_at_faceSM(Behavior):
	'''
	Moves Sara's head towards the face of an entity
	'''


	def __init__(self):
		super(action_look_at_faceSM, self).__init__()
		self.name = 'action_look_at_face'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
        
        # [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:721 y:497, x:513 y:416
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['Entity'])
		_state_machine.userdata.Entity = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


		with _state_machine:
			# x:54 y:28
			OperatableStateMachine.add('ExtractPos',
										CalculationState(calculation=lambda x: x.position),
										transitions={'done': 'if person'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Entity', 'output_value': 'Position'})

			# x:471 y:323
			OperatableStateMachine.add('direction',
										Get_direction_to_point(frame_origin="base_link", frame_reference="head_link"),
										transitions={'done': 'InvertPitch', 'fail': 'failed'},
										autonomy={'done': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'targetPoint': 'Position', 'yaw': 'yaw', 'pitch': 'pitch'})

			# x:675 y:322
			OperatableStateMachine.add('InvertPitch',
										CalculationState(calculation=lambda x: -x),
										transitions={'done': 'Head'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'pitch', 'output_value': 'pitch'})

			# x:665 y:406
			OperatableStateMachine.add('Head',
										SaraSetHeadAngleKey(),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'yaw': 'yaw', 'pitch': 'pitch'})

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
										transitions={'done': 'calc z'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Entity', 'output_value': 'Y'})

			# x:63 y:362
			OperatableStateMachine.add('calc z',
										CalculationState(calculation=lambda x: x.face.boundingBox.Center.z),
										transitions={'done': 'set zero'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Entity', 'output_value': 'Z'})

			# x:50 y:522
			OperatableStateMachine.add('gen pose',
										GenPoseEulerKey(),
										transitions={'done': 'get pos'},
										autonomy={'done': Autonomy.Off},
										remapping={'xpos': 'X', 'ypos': 'Y', 'zpos': 'Z', 'yaw': 'zero', 'pitch': 'zero', 'roll': 'zero', 'pose': 'pose'})

			# x:76 y:441
			OperatableStateMachine.add('set zero',
										SetKey(Value=0),
										transitions={'done': 'gen pose'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'zero'})

			# x:231 y:519
			OperatableStateMachine.add('get pos',
										CalculationState(calculation=lambda x: x.position),
										transitions={'done': 'Look Head'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'pose', 'output_value': 'Position'})

			# x:261 y:151
			OperatableStateMachine.add('get pos obj',
										CalculationState(calculation=lambda x: x.position),
										transitions={'done': 'Look Entity'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Entity', 'output_value': 'Position'})

			# x:446 y:183
			OperatableStateMachine.add('Look Entity',
										LogState(text="Look Entity", severity=Logger.REPORT_HINT),
										transitions={'done': 'direction'},
										autonomy={'done': Autonomy.Off})

			# x:297 y:340
			OperatableStateMachine.add('Look Head',
										LogState(text="Look Head", severity=Logger.REPORT_HINT),
										transitions={'done': 'direction'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
