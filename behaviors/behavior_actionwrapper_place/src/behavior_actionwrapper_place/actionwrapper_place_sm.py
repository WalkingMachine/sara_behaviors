#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_actionwrapper_place')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.GetRosParam import GetRosParam
from sara_flexbe_states.sara_say_key import SaraSayKey
from behavior_action_place.action_place_sm import Action_placeSM
from sara_flexbe_states.pose_gen_euler import GenPoseEuler
from sara_flexbe_states.TF_transform import TF_transformation
from flexbe_states.check_condition_state import CheckConditionState
from sara_flexbe_states.sara_say import SaraSay
from flexbe_states.flexible_calculation_state import FlexibleCalculationState
from flexbe_states.log_state import LogState
from flexbe_states.log_key_state import LogKeyState
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

		# O 281 11 
		# Place|n1- where to put the object

		# O 995 164 
		# Chercher un objet de type container (le plus proche?) et se deplacer la bas



	def create(self):
		# x:620 y:593, x:661 y:130, x:656 y:30
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'critical_fail'], input_keys=['Action'])
		_state_machine.userdata.Action = ["Place", "table"]

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


		with _state_machine:
			# x:44 y:28
			OperatableStateMachine.add('gripper contain',
										GetRosParam(ParamName="behavior/GripperContent"),
										transitions={'done': 'if contain something', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'Value': 'content'})

			# x:41 y:387
			OperatableStateMachine.add('say place object',
										SaraSayKey(Format=lambda x: x, emotion=1, block=True),
										transitions={'done': 'genPoseArm'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'sentence'})

			# x:66 y:744
			OperatableStateMachine.add('Action_place',
										self.use_behavior(Action_placeSM, 'Action_place'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pos': 'MapPosition'})

			# x:44 y:470
			OperatableStateMachine.add('genPoseArm',
										GenPoseEuler(x=0.75, y=-0.1, z=0.8, roll=0, pitch=0, yaw=0),
										transitions={'done': 'referential from robot to map'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose': 'position'})

			# x:26 y:554
			OperatableStateMachine.add('referential from robot to map',
										TF_transformation(in_ref="base_link", out_ref="map"),
										transitions={'done': 'log pose', 'fail': 'log tf error'},
										autonomy={'done': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'in_pos': 'position', 'out_pos': 'MapPosition'})

			# x:39 y:118
			OperatableStateMachine.add('if contain something',
										CheckConditionState(predicate=lambda x: x != ''),
										transitions={'true': 'cond', 'false': 'say nothing in gripper'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'content'})

			# x:268 y:113
			OperatableStateMachine.add('say nothing in gripper',
										SaraSay(sentence="It seems I have nothing in my gripper", emotion=1, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:29 y:297
			OperatableStateMachine.add('construction phrase',
										FlexibleCalculationState(calculation=lambda x: "I will place this "+str(x[0])+" on the "+str(x[1][1]), input_keys=["content", "Action"]),
										transitions={'done': 'say place object'},
										autonomy={'done': Autonomy.Off},
										remapping={'content': 'content', 'Action': 'Action', 'output_value': 'sentence'})

			# x:1077 y:204
			OperatableStateMachine.add('say place it this place',
										SaraSayKey(Format=lambda x: "I will place this "+x+" right there.", emotion=1, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'content'})

			# x:37 y:211
			OperatableStateMachine.add('cond',
										CheckConditionState(predicate=lambda x: x[1] != ''),
										transitions={'true': 'construction phrase', 'false': 'failed'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'Action'})

			# x:257 y:413
			OperatableStateMachine.add('log tf error',
										LogState(text="tf error", severity=Logger.REPORT_HINT),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:66 y:638
			OperatableStateMachine.add('log pose',
										LogKeyState(text="the placement pose will be: {}", severity=Logger.REPORT_HINT),
										transitions={'done': 'Action_place'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'MapPosition'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
