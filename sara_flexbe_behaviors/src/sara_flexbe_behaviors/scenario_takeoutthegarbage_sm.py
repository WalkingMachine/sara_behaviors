#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_behaviors.init_sequence_sm import Init_SequenceSM as sara_flexbe_behaviors__Init_SequenceSM
from sara_flexbe_behaviors.action_move_sm import Action_MoveSM as sara_flexbe_behaviors__Action_MoveSM
from sara_flexbe_states.set_gripper_state import SetGripperState
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.run_trajectory import RunTrajectory
from sara_flexbe_behaviors.action_takebag_sm import Action_TakeBagSM as sara_flexbe_behaviors__Action_TakeBagSM
from sara_flexbe_states.GetClosestObstacle import GetClosestObstacle
from sara_flexbe_states.get_reachable_waypoint import Get_Reacheable_Waypoint
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_states.TF_transform import TF_transformation
from sara_flexbe_states.for_loop import ForLoop
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon May 13 2019
@author: Quentin Gaillot
'''
class Scenario_TakeOutTheGarbageSM(Behavior):
	'''
	Scenario 2019 for Take out the garbage, House keeper
	'''


	def __init__(self):
		super(Scenario_TakeOutTheGarbageSM, self).__init__()
		self.name = 'Scenario_TakeOutTheGarbage'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(sara_flexbe_behaviors__Init_SequenceSM, 'First bin/Init_Sequence')
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'First bin/go to drop the bag/Action_Move')
		self.add_behavior(sara_flexbe_behaviors__Action_TakeBagSM, 'First bin/Action_TakeBag')
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'First bin/go to bin/Action_Move')
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'First bin/find the bin/Action_Move')
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'second bin/go to bin/Action_Move')
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'second bin/find the bin/Action_Move')
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'second bin/go to drop the bag/Action_Move')
		self.add_behavior(sara_flexbe_behaviors__Action_TakeBagSM, 'second bin/Action_TakeBag')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:

		# O 55 98 /First bin/find the bin
		# mettre le bras en haut

		# O 355 118 /First bin/get the bag/trajectory down with torque limit/torque control
		# faire une state toggle du controller manager|n



	def create(self):
		# x:910 y:782, x:907 y:184
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.bin1Waypoint = "bin1"
		_state_machine.userdata.bin2Waypoint = "bin2"
		_state_machine.userdata.bin1Height = "1"
		_state_machine.userdata.bin2Height = "1"
		_state_machine.userdata.dropzoneWaypoint = "dropzone"

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:30 y:458, x:130 y:458
		_sm_go_to_drop_the_bag_0 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['dropzoneWaypoint'])

		with _sm_go_to_drop_the_bag_0:
			# x:62 y:32
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'second bin/go to drop the bag/Action_Move'),
										transitions={'finished': 'open the gripper', 'failed': 'say cant go to drop zone'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'dropzoneWaypoint'})

			# x:75 y:181
			OperatableStateMachine.add('open the gripper',
										SetGripperState(width=0.1, effort=1),
										transitions={'object': 'finished', 'no_object': 'finished'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:285 y:72
			OperatableStateMachine.add('say cant go to drop zone',
										SaraSay(sentence="I am not able to go to the drop zone. I will put the bag here and go to the second bin.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'open the gripper'},
										autonomy={'done': Autonomy.Off})


		# x:30 y:458, x:130 y:458
		_sm_find_the_bin_1 = OperatableStateMachine(outcomes=['finished', 'failed'])

		with _sm_find_the_bin_1:
			# x:89 y:168
			OperatableStateMachine.add('find closest obstacle point',
										GetClosestObstacle(topic="/scan", maximumDistance=2),
										transitions={'done': 'pose form lidar to map'},
										autonomy={'done': Autonomy.Off},
										remapping={'Angle': 'Angle', 'distance': 'distance', 'position': 'detectedObstacle'})

			# x:90 y:493
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'second bin/find the bin/Action_Move'),
										transitions={'finished': 'redo ajustements de la position', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'poseToBin'})

			# x:91 y:395
			OperatableStateMachine.add('get waypoint',
										Get_Reacheable_Waypoint(),
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose_in': 'detectedBin', 'distance': 'distanceToBin', 'pose_out': 'poseToBin'})

			# x:103 y:312
			OperatableStateMachine.add('set distance to bin',
										SetKey(Value=0.5),
										transitions={'done': 'get waypoint'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'distanceToBin'})

			# x:101 y:244
			OperatableStateMachine.add('pose form lidar to map',
										TF_transformation(in_ref="front_hokuyo_link", out_ref="map"),
										transitions={'done': 'set distance to bin', 'fail': 'failed'},
										autonomy={'done': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'in_pos': 'detectedObstacle', 'out_pos': 'detectedBin'})

			# x:80 y:598
			OperatableStateMachine.add('redo ajustements de la position',
										ForLoop(repeat=2),
										transitions={'do': 'Action_Move', 'end': 'finished'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index'})


		# x:30 y:458, x:130 y:458
		_sm_go_to_bin_2 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['bin2Waypoint'])

		with _sm_go_to_bin_2:
			# x:254 y:199
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'second bin/go to bin/Action_Move'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'bin2Waypoint'})


		# x:1146 y:606, x:1141 y:452
		_sm_find_the_bin_3 = OperatableStateMachine(outcomes=['finished', 'failed'])

		with _sm_find_the_bin_3:
			# x:89 y:168
			OperatableStateMachine.add('find closest obstacle point',
										GetClosestObstacle(topic="/scan", maximumDistance=2),
										transitions={'done': 'pose form lidar to map'},
										autonomy={'done': Autonomy.Off},
										remapping={'Angle': 'Angle', 'distance': 'distance', 'position': 'detectedObstacle'})

			# x:90 y:493
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'First bin/find the bin/Action_Move'),
										transitions={'finished': 'redo ajustements de la position', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'poseToBin'})

			# x:91 y:395
			OperatableStateMachine.add('get waypoint',
										Get_Reacheable_Waypoint(),
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose_in': 'detectedBin', 'distance': 'distanceToBin', 'pose_out': 'poseToBin'})

			# x:103 y:312
			OperatableStateMachine.add('set distance to bin',
										SetKey(Value=0.5),
										transitions={'done': 'get waypoint'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'distanceToBin'})

			# x:101 y:244
			OperatableStateMachine.add('pose form lidar to map',
										TF_transformation(in_ref="front_hokuyo_link", out_ref="map"),
										transitions={'done': 'set distance to bin', 'fail': 'failed'},
										autonomy={'done': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'in_pos': 'detectedObstacle', 'out_pos': 'detectedBin'})

			# x:80 y:598
			OperatableStateMachine.add('redo ajustements de la position',
										ForLoop(repeat=2),
										transitions={'do': 'Action_Move', 'end': 'finished'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index'})


		# x:573 y:546, x:622 y:92
		_sm_go_to_bin_4 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['bin1Waypoint'])

		with _sm_go_to_bin_4:
			# x:254 y:199
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'First bin/go to bin/Action_Move'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'bin1Waypoint'})


		# x:788 y:451, x:808 y:125
		_sm_go_to_drop_the_bag_5 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['dropzoneWaypoint'])

		with _sm_go_to_drop_the_bag_5:
			# x:62 y:32
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'First bin/go to drop the bag/Action_Move'),
										transitions={'finished': 'pose pour drop bag', 'failed': 'say cant go to drop zone'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'dropzoneWaypoint'})

			# x:72 y:281
			OperatableStateMachine.add('open the gripper',
										SetGripperState(width=0.1, effort=1),
										transitions={'object': 'finished', 'no_object': 'finished'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:285 y:72
			OperatableStateMachine.add('say cant go to drop zone',
										SaraSay(sentence="I am not able to go to the drop zone. I will put the bag here and go to the second bin.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'pose pour drop bag'},
										autonomy={'done': Autonomy.Off})

			# x:77 y:193
			OperatableStateMachine.add('pose pour drop bag',
										RunTrajectory(file="poubelle_depose", duration=8),
										transitions={'done': 'open the gripper'},
										autonomy={'done': Autonomy.Off})


		# x:946 y:467, x:907 y:75
		_sm_second_bin_6 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['bin2Waypoint', 'bin2Height', 'dropzoneWaypoint'])

		with _sm_second_bin_6:
			# x:150 y:33
			OperatableStateMachine.add('go to bin',
										_sm_go_to_bin_2,
										transitions={'finished': 'find the bin', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'bin2Waypoint': 'bin2Waypoint'})

			# x:149 y:164
			OperatableStateMachine.add('find the bin',
										_sm_find_the_bin_1,
										transitions={'finished': 'Action_TakeBag', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:135 y:430
			OperatableStateMachine.add('go to drop the bag',
										_sm_go_to_drop_the_bag_0,
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'dropzoneWaypoint': 'dropzoneWaypoint'})

			# x:136 y:288
			OperatableStateMachine.add('Action_TakeBag',
										self.use_behavior(sara_flexbe_behaviors__Action_TakeBagSM, 'second bin/Action_TakeBag'),
										transitions={'finished': 'go to drop the bag', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})


		# x:776 y:624, x:717 y:53
		_sm_first_bin_7 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['bin1Waypoint', 'bin1Height', 'dropzoneWaypoint'])

		with _sm_first_bin_7:
			# x:57 y:26
			OperatableStateMachine.add('Init_Sequence',
										self.use_behavior(sara_flexbe_behaviors__Init_SequenceSM, 'First bin/Init_Sequence'),
										transitions={'finished': 'go to bin', 'failed': 'go to bin'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:267 y:432
			OperatableStateMachine.add('go to drop the bag',
										_sm_go_to_drop_the_bag_5,
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'dropzoneWaypoint': 'dropzoneWaypoint'})

			# x:257 y:288
			OperatableStateMachine.add('Action_TakeBag',
										self.use_behavior(sara_flexbe_behaviors__Action_TakeBagSM, 'First bin/Action_TakeBag'),
										transitions={'finished': 'go to drop the bag', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:275 y:35
			OperatableStateMachine.add('go to bin',
										_sm_go_to_bin_4,
										transitions={'finished': 'find the bin', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'bin1Waypoint': 'bin1Waypoint'})

			# x:286 y:164
			OperatableStateMachine.add('find the bin',
										_sm_find_the_bin_3,
										transitions={'finished': 'Action_TakeBag', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})



		with _state_machine:
			# x:277 y:63
			OperatableStateMachine.add('First bin',
										_sm_first_bin_7,
										transitions={'finished': 'second bin', 'failed': 'try second bin'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'bin1Waypoint': 'bin1Waypoint', 'bin1Height': 'bin1Height', 'dropzoneWaypoint': 'dropzoneWaypoint'})

			# x:331 y:381
			OperatableStateMachine.add('second bin',
										_sm_second_bin_6,
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'bin2Waypoint': 'bin2Waypoint', 'bin2Height': 'bin2Height', 'dropzoneWaypoint': 'dropzoneWaypoint'})

			# x:444 y:195
			OperatableStateMachine.add('try second bin',
										SaraSay(sentence="I failed to take out the garbage from the first bin but I will try the second bin.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'second bin'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
