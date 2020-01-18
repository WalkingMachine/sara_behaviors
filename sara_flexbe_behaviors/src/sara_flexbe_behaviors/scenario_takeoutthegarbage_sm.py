#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.continue_button import ContinueButton
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_behaviors.init_sequence_sm import Init_SequenceSM as Init_SequenceSM
from sara_flexbe_behaviors.action_move_sm import Action_MoveSM as Action_MoveSM
from sara_flexbe_states.run_trajectory import RunTrajectory
from sara_flexbe_states.set_gripper_state import SetGripperState
from sara_flexbe_behaviors.action_takebag_sm import Action_TakeBagSM as Action_TakeBagSM

from sara_flexbe_states.get_reachable_waypoint import Get_Reacheable_Waypoint
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_states.TF_transform import TF_transformation
from sara_flexbe_states.for_loop import ForLoop
from sara_flexbe_states.GetClosestObstacle import GetClosestObstacle
from sara_flexbe_states.sara_set_head_angle import SaraSetHeadAngle
from sara_flexbe_states.sara_move_base import SaraMoveBase
from sara_flexbe_behaviors.action_pass_door_sm import Action_Pass_DoorSM as Action_Pass_DoorSM

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
		self.add_behavior(Init_SequenceSM, 'second bin/Init_Sequence')
		self.add_behavior(Action_MoveSM, 'second bin/go to drop the bag/Action_Move')
		self.add_behavior(Action_TakeBagSM, 'second bin/Action_TakeBag')
		self.add_behavior(Action_MoveSM, 'second bin/go to bin/Action_Move')
		self.add_behavior(Init_SequenceSM, 'First bin/Init_Sequence')
		self.add_behavior(Action_TakeBagSM, 'First bin/Action_TakeBag')
		self.add_behavior(Action_MoveSM, 'First bin/go to bin/Action_Move')
		self.add_behavior(Action_MoveSM, 'First bin/go to drop the bag/Action_Move')
		self.add_behavior(Action_Pass_DoorSM, 'Action_Pass_Door')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:

		# O 120 37 /First bin/find the bin
		# mettre le bras en haut

		# O 355 118 /First bin/get the bag/trajectory down with torque limit/torque control
		# faire une state toggle du controller manager|n



	def create(self):
		# x:738 y:371, x:736 y:220
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.bin1Waypoint = "trash bin"
		_state_machine.userdata.bin2Waypoint = "trash bin 2"
		_state_machine.userdata.bin1Height = "1"
		_state_machine.userdata.bin2Height = "1"
		_state_machine.userdata.dropzone1Waypoint = "dropZone"
		_state_machine.userdata.dropzone2Waypoint = "dropZone"
		_state_machine.userdata.DoorName = "door_1_entry"
		_state_machine.userdata.exit_door = "door_2_exit"

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:810 y:644, x:808 y:125
		_sm_go_to_drop_the_bag_0 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['dropzoneWaypoint', 'exit_door'])

		with _sm_go_to_drop_the_bag_0:
			# x:84 y:36
			OperatableStateMachine.add('say drop',
										SaraSay(sentence="I will go and drop this bag in the drop zone.", input_keys=[], emotion=0, block=False),
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Off})

			# x:66 y:598
			OperatableStateMachine.add('open the gripper',
										SetGripperState(width=0.1, effort=1),
										transitions={'object': 'go to pose transport', 'no_object': 'go to pose transport'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:341 y:469
			OperatableStateMachine.add('say cant go to drop zone',
										SaraSay(sentence="I am not able to go to the drop zone. I will put the bag here and go to the second bin.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'run depose sac'},
										autonomy={'done': Autonomy.Off})

			# x:74 y:490
			OperatableStateMachine.add('run depose sac',
										RunTrajectory(file="poubelle_depose", duration=10),
										transitions={'done': 'open the gripper'},
										autonomy={'done': Autonomy.Off})

			# x:69 y:726
			OperatableStateMachine.add('go to pose transport',
										RunTrajectory(file="transport", duration=0),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:76 y:386
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(Action_MoveSM, 'First bin/go to drop the bag/Action_Move'),
										transitions={'finished': 'run depose sac', 'failed': 'say cant go to drop zone'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'dropzoneWaypoint'})


		# x:570 y:519, x:575 y:330
		_sm_find_the_bin_1 = OperatableStateMachine(outcomes=['finished', 'failed'])

		with _sm_find_the_bin_0:
			# x:89 y:62
			OperatableStateMachine.add('place arm',
										RunTrajectory(file="poubelle_init", duration=0),
										transitions={'done': 'leve la tete'},
										autonomy={'done': Autonomy.Off})

			# x:268 y:410
			OperatableStateMachine.add('get waypoint',
										Get_Reacheable_Waypoint(),
										transitions={'done': 'move'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose_in': 'detectedBin', 'distance': 'distanceToBin', 'pose_out': 'poseToBin'})

			# x:293 y:326
			OperatableStateMachine.add('set distance to bin',
										SetKey(Value=0.5),
										transitions={'done': 'get waypoint'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'distanceToBin'})

			# x:278 y:238
			OperatableStateMachine.add('pose form lidar to map',
										TF_transformation(in_ref="front_hokuyo_link", out_ref="map"),
										transitions={'done': 'set distance to bin', 'fail': 'failed'},
										autonomy={'done': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'in_pos': 'detectedObstacle', 'out_pos': 'detectedBin'})

			# x:80 y:598
			OperatableStateMachine.add('redo ajustements de la position',
										ForLoop(repeat=2),
										transitions={'do': 'find closest obstacle point', 'end': 'finished'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index'})

			# x:89 y:168
			OperatableStateMachine.add('find closest obstacle point',
										GetClosestObstacle(topic="/scan", maximumDistance=2),
										transitions={'done': 'pose form lidar to map'},
										autonomy={'done': Autonomy.Off},
										remapping={'Angle': 'Angle', 'distance': 'distance', 'position': 'detectedObstacle'})

			# x:288 y:104
			OperatableStateMachine.add('leve la tete',
										SaraSetHeadAngle(pitch=0, yaw=0),
										transitions={'done': 'find closest obstacle point'},
										autonomy={'done': Autonomy.Off})

			# x:285 y:504
			OperatableStateMachine.add('move',
										SaraMoveBase(reference="map"),
										transitions={'arrived': 'redo ajustements de la position', 'failed': 'finished'},
										autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'poseToBin'})


		# x:30 y:365, x:130 y:365
		_sm_go_to_bin_1 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['bin2Waypoint'])

		with _sm_go_to_bin_1:
			# x:59 y:100
			OperatableStateMachine.add('bras sur le cote',
										RunTrajectory(file="poubelle_transport", duration=0),
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Off})

			# x:254 y:199
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(Action_MoveSM, 'First bin/go to bin/Action_Move'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'bin1Waypoint'})

			# x:86 y:104
			OperatableStateMachine.add('bras sur le cote',
										RunTrajectory(file="poubelle_transport", duration=0),
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Off})


		# x:810 y:644, x:808 y:125
		_sm_go_to_drop_the_bag_4 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['dropzoneWaypoint', 'exit_door'])

		with _sm_go_to_drop_the_bag_4:
			# x:84 y:36
			OperatableStateMachine.add('say drop',
										SaraSay(sentence="I will go and drop this bag in the drop zone.", input_keys=[], emotion=0, block=False),
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Off})

			# x:66 y:598
			OperatableStateMachine.add('open the gripper',
										SetGripperState(width=0.1, effort=1),
										transitions={'object': 'go to pose transport', 'no_object': 'go to pose transport'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:341 y:469
			OperatableStateMachine.add('say cant go to drop zone',
										SaraSay(sentence="I am not able to go to the drop zone. I will put the bag here and go to the second bin.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'run depose sac'},
										autonomy={'done': Autonomy.Off})

			# x:74 y:490
			OperatableStateMachine.add('run depose sac',
										RunTrajectory(file="poubelle_depose", duration=10),
										transitions={'done': 'open the gripper'},
										autonomy={'done': Autonomy.Off})

			# x:69 y:726
			OperatableStateMachine.add('go to pose transport',
										RunTrajectory(file="transport", duration=0),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:76 y:386
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'First bin/go to drop the bag/Action_Move'),
										transitions={'finished': 'run depose sac', 'failed': 'say cant go to drop zone'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'dropzoneWaypoint'})


		# x:570 y:519, x:575 y:330
		_sm_find_the_bin_5 = OperatableStateMachine(outcomes=['finished', 'failed'])

		with _sm_find_the_bin_5:
			# x:89 y:62
			OperatableStateMachine.add('place arm',
										RunTrajectory(file="poubelle_init", duration=0),
										transitions={'done': 'leve la tete'},
										autonomy={'done': Autonomy.Off})

			# x:270 y:378
			OperatableStateMachine.add('get waypoint',
										Get_Reacheable_Waypoint(),
										transitions={'done': 'move'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose_in': 'detectedBin', 'distance': 'distanceToBin', 'pose_out': 'poseToBin'})

			# x:296 y:284
			OperatableStateMachine.add('set distance to bin',
										SetKey(Value=0.5),
										transitions={'done': 'get waypoint'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'distanceToBin'})

			# x:278 y:201
			OperatableStateMachine.add('pose form lidar to map',
										TF_transformation(in_ref="front_hokuyo_link", out_ref="map"),
										transitions={'done': 'set distance to bin', 'fail': 'failed'},
										autonomy={'done': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'in_pos': 'detectedObstacle', 'out_pos': 'detectedBin'})

			# x:80 y:514
			OperatableStateMachine.add('redo ajustements de la position',
										ForLoop(repeat=2),
										transitions={'do': 'find closest obstacle point', 'end': 'finished'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index'})

			# x:87 y:129
			OperatableStateMachine.add('find closest obstacle point',
										GetClosestObstacle(topic="/scan", maximumDistance=2),
										transitions={'done': 'pose form lidar to map'},
										autonomy={'done': Autonomy.Off},
										remapping={'Angle': 'Angle', 'distance': 'distance', 'position': 'detectedObstacle'})

			# x:288 y:77
			OperatableStateMachine.add('leve la tete',
										SaraSetHeadAngle(pitch=0, yaw=0),
										transitions={'done': 'find closest obstacle point'},
										autonomy={'done': Autonomy.Off})

			# x:287 y:464
			OperatableStateMachine.add('move',
										SaraMoveBase(reference="map"),
										transitions={'arrived': 'redo ajustements de la position', 'failed': 'finished'},
										autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'poseToBin'})

		# x:30 y:365, x:130 y:365
		_sm_go_to_bin_4 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['bin2Waypoint'])

		with _sm_go_to_bin_4:
			# x:59 y:100
			OperatableStateMachine.add('bras sur le cote',
										RunTrajectory(file="poubelle_transport", duration=0),
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Off})

			# x:254 y:199
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(Action_MoveSM, 'second bin/go to bin/Action_Move'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'bin2Waypoint'})


		# x:418 y:580, x:694 y:339
		_sm_go_to_drop_the_bag_5 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['dropzoneWaypoint', 'exit_door'])

		with _sm_go_to_drop_the_bag_5:
			# x:65 y:215
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(Action_MoveSM, 'second bin/go to drop the bag/Action_Move'),
										transitions={'finished': 'run depose sac', 'failed': 'say cant go to drop zone'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'dropzoneWaypoint'})

			# x:385 y:324
			OperatableStateMachine.add('say cant go to drop zone',
										SaraSay(sentence="I am not able to go to the drop zone. I will put the bag here.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'run depose sac'},
										autonomy={'done': Autonomy.Off})

			# x:76 y:340
			OperatableStateMachine.add('run depose sac',
										RunTrajectory(file="poubelle_depose", duration=10),
										transitions={'done': 'open the gripper'},
										autonomy={'done': Autonomy.Off})

			# x:74 y:505
			OperatableStateMachine.add('go to pose transport',
										RunTrajectory(file="transport", duration=0),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:74 y:426
			OperatableStateMachine.add('open the gripper',
										SetGripperState(width=0.1, effort=1),
										transitions={'object': 'go to pose transport', 'no_object': 'go to pose transport'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})


		# x:704 y:599, x:717 y:53
		_sm_first_bin_6 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['bin1Waypoint', 'bin1Height', 'dropzoneWaypoint', 'exit_door'])


		with _sm_second_bin_6:
			# x:57 y:26
			OperatableStateMachine.add('Init_Sequence',
										self.use_behavior(Init_SequenceSM, 'First bin/Init_Sequence'),
										transitions={'finished': 'go to bin', 'failed': 'go to bin'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:267 y:432
			OperatableStateMachine.add('go to drop the bag',
										_sm_go_to_drop_the_bag_2,
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'dropzoneWaypoint': 'dropzoneWaypoint', 'exit_door': 'exit_door'})

			# x:257 y:346
			OperatableStateMachine.add('Action_TakeBag',
										self.use_behavior(Action_TakeBagSM, 'First bin/Action_TakeBag'),
										transitions={'finished': 'go to drop the bag', 'failed': 'Missed It once'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:275 y:35
			OperatableStateMachine.add('go to bin',
										_sm_go_to_bin_1,
										transitions={'finished': 'find the bin', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'bin2Waypoint': 'bin2Waypoint'})

			# x:286 y:164
			OperatableStateMachine.add('find the bin',
										_sm_find_the_bin_0,
										transitions={'finished': 'Try twice', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:298 y:254
			OperatableStateMachine.add('Try twice',
										ForLoop(repeat=1),
										transitions={'do': 'Action_TakeBag', 'end': 'failed'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index'})

			# x:102 y:262
			OperatableStateMachine.add('Missed It once',
										SaraSay(sentence="I will try one more time.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'Try twice'},
										autonomy={'done': Autonomy.Off})


		# x:704 y:599, x:717 y:53
		_sm_first_bin_7 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['bin1Waypoint', 'bin1Height', 'dropzoneWaypoint', 'exit_door'])

		with _sm_first_bin_7:
			# x:57 y:26
			OperatableStateMachine.add('Init_Sequence',
										self.use_behavior(Init_SequenceSM, 'second bin/Init_Sequence'),
										transitions={'finished': 'go to bin', 'failed': 'go to bin'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:257 y:329
			OperatableStateMachine.add('Action_TakeBag',
										self.use_behavior(Action_TakeBagSM, 'second bin/Action_TakeBag'),
										transitions={'finished': 'go to drop the bag', 'failed': 'Missed It once'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:286 y:164
			OperatableStateMachine.add('find the bin',
										_sm_find_the_bin_5,
										transitions={'finished': 'Try twice', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:292 y:234
			OperatableStateMachine.add('Try twice',
										ForLoop(repeat=1),
										transitions={'do': 'Action_TakeBag', 'end': 'failed'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index'})

			# x:102 y:262
			OperatableStateMachine.add('Missed It once',
										SaraSay(sentence="I will try one more time.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'Try twice'},
										autonomy={'done': Autonomy.Off})

			# x:267 y:432
			OperatableStateMachine.add('go to drop the bag',
										_sm_go_to_drop_the_bag_4,
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'dropzoneWaypoint': 'dropzoneWaypoint', 'exit_door': 'exit_door'})

			# x:275 y:35
			OperatableStateMachine.add('go to bin',
										_sm_go_to_bin_3,
										transitions={'finished': 'find the bin', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'bin1Waypoint': 'bin1Waypoint'})



		with _state_machine:
			# x:277 y:63
			OperatableStateMachine.add('First bin',
										_sm_first_bin_7,
										transitions={'finished': 'say take second bag', 'failed': 'try second bin'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'bin1Waypoint': 'bin1Waypoint', 'bin1Height': 'bin1Height', 'dropzoneWaypoint': 'dropzone1Waypoint', 'exit_door': 'exit_door'})

			# x:485 y:201
			OperatableStateMachine.add('try second bin',
										SaraSay(sentence="I failed to take out the garbage from the first bin but I will try the second bin.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'second bin'},
										autonomy={'done': Autonomy.Off})

			# x:267 y:199
			OperatableStateMachine.add('say take second bag',
										SaraSay(sentence="Good! I will now get rid of the second bag.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'second bin'},
										autonomy={'done': Autonomy.Off})

			# x:267 y:376
			OperatableStateMachine.add('second bin',
										_sm_second_bin_6,
										transitions={'finished': 'say end', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'bin2Waypoint': 'bin2Waypoint', 'bin2Height': 'bin2Height', 'dropzoneWaypoint': 'dropzone2Waypoint', 'exit_door': 'exit_door'})

			# x:94 y:153
			OperatableStateMachine.add('IllManageSomehow',
										SaraSay(sentence="Hmmm. This is a hard door to pass...", input_keys=[], emotion=0, block=True),
										transitions={'done': 'First bin'},
										autonomy={'done': Autonomy.Off})

			# x:65 y:53
			OperatableStateMachine.add('Action_Pass_Door',
										self.use_behavior(Action_Pass_DoorSM, 'Action_Pass_Door'),
										transitions={'Done': 'First bin', 'Fail': 'IllManageSomehow'},
										autonomy={'Done': Autonomy.Inherit, 'Fail': Autonomy.Inherit},
										remapping={'DoorName': 'DoorName'})

			# x:15 y:242
			OperatableStateMachine.add('button',
										ContinueButton(),
										transitions={'true': 'Action_Pass_Door', 'false': 'Action_Pass_Door'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off})

			# x:512 y:389
			OperatableStateMachine.add('say end',
										SaraSay(sentence="Yay! I have completed this task.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
