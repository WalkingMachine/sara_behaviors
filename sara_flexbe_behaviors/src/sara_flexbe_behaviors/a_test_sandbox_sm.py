#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.pose_gen_euler import GenPoseEuler
from sara_flexbe_behaviors.action_place_2_sm import Action_place_2SM as sara_flexbe_behaviors__Action_place_2SM
from sara_flexbe_states.TF_transform import TF_transformation
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu May 10 2018
@author: Philippe La Madeleine
'''
class ATestSandboxSM(Behavior):
	'''
	Une behavior pour faire des tests rapidement.
	'''


	def __init__(self):
		super(ATestSandboxSM, self).__init__()
		self.name = 'A Test Sandbox'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(sara_flexbe_behaviors__Action_place_2SM, 'Action_place_2')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:537 y:110, x:166 y:479
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.Pose1 = "PostGripPose"
		_state_machine.userdata.Pose2 = "IdlePose"
		_state_machine.userdata.actionList = [["Find", "bottle"], ["move", "kitchen"]]
		_state_machine.userdata.titre = "test"
		_state_machine.userdata.relative = False
		_state_machine.userdata.pitch = -0.8
		_state_machine.userdata.Action1 = ["move", "counter"]
		_state_machine.userdata.Action2 = ["move", "table"]
		_state_machine.userdata.pose = "Dining room"
		_state_machine.userdata.say1 = "say one"
		_state_machine.userdata.say2 = "say two"
		_state_machine.userdata.index = -1
		_state_machine.userdata.name = "person"
		_state_machine.userdata.name2 = "apple"
		_state_machine.userdata.nameFilter = ""
		_state_machine.userdata.waypointToCheckDict = {"bad_table":["bad_table"]}
		_state_machine.userdata.cleanupRoom = "bad_table"
		_state_machine.userdata.placedObjects = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:0 y:153
			OperatableStateMachine.add('GetDroppingPose',
										GenPoseEuler(x=0.7, y=-0.1, z=0.75, roll=0.0, pitch=0.0, yaw=0.0),
										transitions={'done': 'TF_transformation'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose': 'pos'})

			# x:330 y:118
			OperatableStateMachine.add('Action_place_2',
										self.use_behavior(sara_flexbe_behaviors__Action_place_2SM, 'Action_place_2'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pos': 'droppingPose'})

			# x:151 y:145
			OperatableStateMachine.add('TF_transformation',
										TF_transformation(in_ref="base_link", out_ref="map"),
										transitions={'done': 'Action_place_2', 'fail': 'Action_place_2'},
										autonomy={'done': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'in_pos': 'pos', 'out_pos': 'droppingPose'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
