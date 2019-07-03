#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.decision_state import DecisionState
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_behaviors.action_move_sm import Action_MoveSM as sara_flexbe_behaviors__Action_MoveSM
from flexbe_states.check_condition_state import CheckConditionState
from flexbe_states.flexible_calculation_state import FlexibleCalculationState
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.for_loop_with_input import ForLoopWithInput
from flexbe_states.flexible_check_condition_state import FlexibleCheckConditionState
from flexbe_states.log_key_state import LogKeyState
from sara_flexbe_states.SetSegmentationRosParam import SetSegmentationRosParam
from sara_flexbe_states.list_entities_by_name import list_entities_by_name
from sara_flexbe_states.Filter import Filter
from sara_flexbe_states.CheckMisplacedObjects import CheckMisplacedObjects
from sara_flexbe_states.sara_set_head_angle import SaraSetHeadAngle
from flexbe_states.wait_state import WaitState
from sara_flexbe_behaviors.action_pick_sm import Action_pickSM as sara_flexbe_behaviors__Action_pickSM
from sara_flexbe_states.pose_gen_euler import GenPoseEuler
from sara_flexbe_states.torque_reader import ReadTorque
from sara_flexbe_states.set_gripper_state import SetGripperState
from sara_flexbe_states.run_trajectory import RunTrajectory
from sara_flexbe_states.sara_move_base import SaraMoveBase
from sara_flexbe_behaviors.action_place_2_sm import Action_place_2SM as sara_flexbe_behaviors__Action_place_2SM
from sara_flexbe_states.TF_transform import TF_transformation
from sara_flexbe_states.WonderlandGetEntityByID import WonderlandGetEntityByID
from sara_flexbe_behaviors.action_place_sm import Action_placeSM as sara_flexbe_behaviors__Action_placeSM
from sara_flexbe_behaviors.init_sequence_sm import Init_SequenceSM as sara_flexbe_behaviors__Init_SequenceSM
from sara_flexbe_states.sara_nlu_getRoom import SaraNLUgetRoom
from sara_flexbe_behaviors.action_pass_door_sm import Action_Pass_DoorSM as sara_flexbe_behaviors__Action_Pass_DoorSM
from sara_flexbe_states.for_loop import ForLoop
from sara_flexbe_states.get_speech import GetSpeech
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Mar 11 2019
@author: Raphaël Duchaîne
'''
class Scenario_Housekeeper_CleanUpSM(Behavior):
	'''
	Search items and put them at there place or in the trash can if the item is unknown
	'''


	def __init__(self):
		super(Scenario_Housekeeper_CleanUpSM, self).__init__()
		self.name = 'Scenario_Housekeeper_CleanUp'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'GoToRoom/Action_Move')
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'CheckForMisplacedObjects/CheckAtWaypoints/Action_Move')
		self.add_behavior(sara_flexbe_behaviors__Action_pickSM, 'PickMisplacedObject/GrabMisplacedObject/Action_pick')
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'PutObjectInDesiredContainer/GotoDesiredContainer/Action_Move')
		self.add_behavior(sara_flexbe_behaviors__Action_place_2SM, 'PutObjectInDesiredContainer/PutDownObject/Action_place_2')
		self.add_behavior(sara_flexbe_behaviors__Action_placeSM, 'PutObjectInDesiredContainer/CantGoToDestination/Action_place')
		self.add_behavior(sara_flexbe_behaviors__Init_SequenceSM, 'EnterArena/Init_Sequence')
		self.add_behavior(sara_flexbe_behaviors__Action_Pass_DoorSM, 'EnterArena/Action_Pass_Door')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:

		# O 83 226 /PickMisplacedObject
		# Va à l'objet trouvé et prend l'objet|n|nRappel: MisplacedObject contient la liste [entité originale, pseudo-entité wonderland]|n|nTODO:|nRecovery si on est pas capable de se rendre (demander de déagager l'espace??)

		# O 829 281 /PutObjectInDesiredContainer
		# Va au contenant désiré de l'objet et dépose l'objet à celui-ci|nSi elle echappe l'objet, elle le signale.|nTODO: Si elle ne peut pas se rendre a la destination ?

		# O 16 335 /CheckForMisplacedObjects
		# SARA va regarder autour pour trouver des objets.|nVérifie la liste d'objet connus si il y en a qui ne sont pas à la bonne place.|nSi aucun n'est trouvé après avoir regardé deux fois; SARA va tenter d'aller à des waypoints pré-déterminés dans la pièce.

		# O 971 172 /EnterArena
		# SARA entre dans l'aréna et demande à l'opérateur dans quelle piece elle doir faire le ménage. Ensuite elle y va.|nSi SARA n'a aucune réponse ou si le NLU ne retrace pas la reponse, SARA va redemander la question une seconde fois.|nNote:|nIl va falloir qu'il y aie des waypoint qui matche le nom de la pièce cleanupRoom.

		# O 682 23 
		# SARA entre dans l'aréna|nEnsuite elle va dans la pièce désignée par l'opérateur.|nUne fois en place, elle va vérifier autour pour des objets à ranger.|nEnsuite elle le prend et le met jusqu'à l'endroit qu'il doit aller.

		# O 430 83 /Loop
		# SARA retourne à la pièce à cleaner

		# O 353 125 /PickMisplacedObject/GrabMisplacedObject/DeusExPickRecovery
		# NOTE: noms des position de réception pour l'item à vérifier !

		# O 643 67 /CheckForMisplacedObjects/ScanAround
		# Lister les entités en concurrence et checker si misplaced. Lorsque Un est trouvé faire un interrupt

		# O 272 133 /PickMisplacedObject/GrabMisplacedObject/DeusExPickRecovery/ReceiveItem
		# Avons remplacé Moveit Par RunTrajectory|n|nPour fail si pas recus à close

		# O 632 11 /CheckForMisplacedObjects/CheckAtWaypoints
		# SARA va aller à un des waypints prédéfinis et va regarder autour pour trouver des objets.|nVérifie la liste d'objet connus si il y en a qui ne sont pas à la bonne place.|nSi aucun n'est trouvé après avoir regardé à chaque waypoint, SARA va semorfondre dans son impuissance de faire du ménage.

		# O 674 44 /PutObjectInDesiredContainer/CantGoToDestination
		# SARA est incapable de se rendre à la destination.|nEle dépose l'objet au sol et continue.

		# O 550 62 /GoToRoom
		# SARA goes the the room mentionned by the operator.|nIf its her first time it will be mentionned.

		# O 685 293 
		# ------------------|n----IMPORTANT-----|n------------------|n|nPeupler le WaypointToCheckDict pour chaque pièce de waypoints clés pour vérifier des objets.|n|nEXEMPLE:|n{"bedroom": ["bedroomWP1","bedroomWP2"], "kitchen": ["kitchenWP1","kitchenWP2"],|n"living area": ["living areaWP1","living areaWP2"], "hallway": ["hallwayWP1"]}|n|n|nS'assurer que ces wapoints existent dans RVIz

		# O 685 473 
		# Créer les waypoints wonderland: |n{"living room": ["lr1", "lr2","lr3","lr4","lr5","lr6"],|n"office": ["of1","of2","of3","of4"],|n"kitchen": ["ki1","ki2","ki3","ki4","ki5","ki6"],|n"bedroom": ["br1","br2","br3","br4","br5","br6"]}|n

		# O 492 556 /PutObjectInDesiredContainer/PutDownObject/DeusExPlaceRecovery
		# lambda x: "Looks like I dropped "+str(x[0][0].name)+". Can you put it in the "+ x[1].name+"?"



	def create(self):
		# x:69 y:457, x:779 y:169
		_state_machine = OperatableStateMachine(outcomes=['done', 'failed'])
		_state_machine.userdata.nameFilter = ""
		_state_machine.userdata.roomQuestion = "What room shall i clean?"
		_state_machine.userdata.waypointGenerationDistance = 0.6
		_state_machine.userdata.placeholder = ""
		_state_machine.userdata.doorName = "crowd"
		_state_machine.userdata.firstTimeInRoom = "yes"
		_state_machine.userdata.waypointToCheckDict = {"bad_table":["bad_table"],"living room": ["lr1", "lr2","lr3","lr4","lr5","lr6"], "office": ["of1","of2","of3","of4"], "kitchen": ["ki1","ki2","ki3","ki4","ki5","ki6"], "bedroom": ["br1","br2","br3","br4","br5","br6"]}
		_state_machine.userdata.placedObjects = 0
		_state_machine.userdata.misplacedObject = ""
		_state_machine.userdata.skipDoorEntrance = False
		_state_machine.userdata.cleanupRoom = "bad_table"

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:293 y:350, x:857 y:186
		_sm_ask_0 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['roomQuestion'], output_keys=['roomAnswer'])

		with _sm_ask_0:
			# x:79 y:95
			OperatableStateMachine.add('say question',
										SaraSay(sentence=lambda x: x[0], input_keys=["question"], emotion=0, block=True),
										transitions={'done': 'get answer'},
										autonomy={'done': Autonomy.Off},
										remapping={'question': 'roomQuestion'})

			# x:92 y:304
			OperatableStateMachine.add('get answer',
										GetSpeech(watchdog=10),
										transitions={'done': 'finished', 'nothing': 'retry ask', 'fail': 'retry ask'},
										autonomy={'done': Autonomy.Off, 'nothing': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'words': 'roomAnswer'})

			# x:345 y:202
			OperatableStateMachine.add('retry ask',
										ForLoop(repeat=2),
										transitions={'do': 'say not understand', 'end': 'say failed'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index'})

			# x:232 y:90
			OperatableStateMachine.add('say not understand',
										SaraSay(sentence="Sorry, I did not understand your answer.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'say question'},
										autonomy={'done': Autonomy.Off})

			# x:604 y:151
			OperatableStateMachine.add('say failed',
										SaraSay(sentence="Sorry, I can't understand your answer.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})


		# x:30 y:365, x:424 y:392
		_sm_nlu_1 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['roomAnswer'], output_keys=['cleanupRoom'])

		with _sm_nlu_1:
			# x:212 y:89
			OperatableStateMachine.add('NLU',
										SaraNLUgetRoom(),
										transitions={'understood': 'done', 'not_understood': 'failed', 'fail': 'failed'},
										autonomy={'understood': Autonomy.Off, 'not_understood': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'sentence': 'roomAnswer', 'answer': 'cleanupRoom'})


		# x:153 y:437
		_sm_deusexplacerecovery_2 = OperatableStateMachine(outcomes=['finished'], input_keys=['misplacedObject'])

		with _sm_deusexplacerecovery_2:
			# x:159 y:40
			OperatableStateMachine.add('getContainerId',
										CalculationState(calculation=lambda x: x[1].containerId),
										transitions={'done': 'getContainerEntity'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'misplacedObject', 'output_value': 'containerId'})

			# x:538 y:318
			OperatableStateMachine.add('ItGoesThere',
										SaraSay(sentence=lambda x: "Looks like I dropped the object. Can you put it in the "+ x[0].name+"?", input_keys=["containerEntity"], emotion=0, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'containerEntity': 'containerEntity'})

			# x:375 y:91
			OperatableStateMachine.add('getContainerEntity',
										WonderlandGetEntityByID(),
										transitions={'found': 'ItGoesThere', 'not_found': 'finished', 'error': 'finished'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off, 'error': Autonomy.Off},
										remapping={'id': 'containerId', 'entity': 'containerEntity', 'depth_position': 'depth_position', 'depth_waypoint': 'depth_waypoint'})


		# x:717 y:285
		_sm_cantgotodestination_3 = OperatableStateMachine(outcomes=['finished'], input_keys=['misplacedObject'])

		with _sm_cantgotodestination_3:
			# x:48 y:60
			OperatableStateMachine.add('getContainerId',
										CalculationState(calculation=lambda x: x[1].containerId),
										transitions={'done': 'getContainerEntity'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'misplacedObject', 'output_value': 'containerId'})

			# x:463 y:245
			OperatableStateMachine.add('Action_place',
										self.use_behavior(sara_flexbe_behaviors__Action_placeSM, 'PutObjectInDesiredContainer/CantGoToDestination/Action_place'),
										transitions={'finished': 'finished', 'failed': 'finished'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pos': 'droppingPose'})

			# x:26 y:149
			OperatableStateMachine.add('getContainerEntity',
										WonderlandGetEntityByID(),
										transitions={'found': 'ICantGetThere', 'not_found': 'ICantGetThereNCONT', 'error': 'ICantGetThereNCONT'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off, 'error': Autonomy.Off},
										remapping={'id': 'containerId', 'entity': 'containerEntity', 'depth_position': 'depth_position', 'depth_waypoint': 'depth_waypoint'})

			# x:249 y:176
			OperatableStateMachine.add('ICantGetThere',
										SaraSay(sentence=lambda x:"I can't find a way to "+str(x[0].name), input_keys=["containerEntity"], emotion=0, block=True),
										transitions={'done': 'GetDroppingPose'},
										autonomy={'done': Autonomy.Off},
										remapping={'containerEntity': 'containerEntity'})

			# x:247 y:114
			OperatableStateMachine.add('ICantGetThereNCONT',
										SaraSay(sentence="I can't find a way to the container", input_keys=[], emotion=0, block=True),
										transitions={'done': 'GetDroppingPose'},
										autonomy={'done': Autonomy.Off})

			# x:475 y:148
			OperatableStateMachine.add('GetDroppingPose',
										GenPoseEuler(x=0.4, y=0, z=0.3, roll=0.0, pitch=0.0, yaw=0.0),
										transitions={'done': 'Action_place'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose': 'droppingPose'})


		# x:632 y:527
		_sm_putdownobject_4 = OperatableStateMachine(outcomes=['done'], input_keys=['misplacedObject'])

		with _sm_putdownobject_4:
			# x:65 y:214
			OperatableStateMachine.add('GetDroppingPose_2',
										GenPoseEuler(x=0.8, y=-0.2, z=0.8, roll=0.0, pitch=0.0, yaw=0.0),
										transitions={'done': 'TF_transformation'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose': 'pos'})

			# x:433 y:292
			OperatableStateMachine.add('Action_place_2',
										self.use_behavior(sara_flexbe_behaviors__Action_place_2SM, 'PutObjectInDesiredContainer/PutDownObject/Action_place_2'),
										transitions={'finished': 'done', 'failed': 'DeusExPlaceRecovery'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pos': 'droppingPose'})

			# x:254 y:246
			OperatableStateMachine.add('TF_transformation',
										TF_transformation(in_ref="base_link", out_ref="map"),
										transitions={'done': 'Action_place_2', 'fail': 'DeusExPlaceRecovery'},
										autonomy={'done': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'in_pos': 'pos', 'out_pos': 'droppingPose'})

			# x:592 y:127
			OperatableStateMachine.add('DeusExPlaceRecovery',
										_sm_deusexplacerecovery_2,
										transitions={'finished': 'done'},
										autonomy={'finished': Autonomy.Inherit},
										remapping={'misplacedObject': 'misplacedObject'})


		# x:518 y:44, x:531 y:152
		_sm_gotodesiredcontainer_5 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['misplacedObject'])

		with _sm_gotodesiredcontainer_5:
			# x:86 y:79
			OperatableStateMachine.add('GetContainerWaypoint',
										CalculationState(calculation=lambda x:x[1].waypoint),
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'misplacedObject', 'output_value': 'targetWaypoint'})

			# x:275 y:79
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'PutObjectInDesiredContainer/GotoDesiredContainer/Action_Move'),
										transitions={'finished': 'done', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'targetWaypoint'})


		# x:374 y:392, x:86 y:765
		_sm_receiveitem_6 = OperatableStateMachine(outcomes=['failed', 'success'])

		with _sm_receiveitem_6:
			# x:67 y:28
			OperatableStateMachine.add('say push on gripper',
										SaraSay(sentence="Simply press it on my gripper.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'opengripper'},
										autonomy={'done': Autonomy.Off})

			# x:53 y:335
			OperatableStateMachine.add('Torque_Reader',
										ReadTorque(watchdog=10, Joint="right_elbow_pitch_joint", Threshold=1, min_time=1),
										transitions={'threshold': 'close_gripper', 'watchdog': 'close_gripper', 'fail': 'transport__Trajectory_2'},
										autonomy={'threshold': Autonomy.Off, 'watchdog': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'torque': 'torque'})

			# x:49 y:440
			OperatableStateMachine.add('close_gripper',
										SetGripperState(width=0, effort=1),
										transitions={'object': 'thank you', 'no_object': 'transport__Trajectory_2'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:45 y:541
			OperatableStateMachine.add('thank you',
										SaraSay(sentence="Thank you", input_keys=[], emotion=1, block=True),
										transitions={'done': 'transport__Trajectory'},
										autonomy={'done': Autonomy.Off})

			# x:52 y:233
			OperatableStateMachine.add('receive_bag__Trajectory',
										RunTrajectory(file="receive_bag", duration=0),
										transitions={'done': 'Torque_Reader'},
										autonomy={'done': Autonomy.Off})

			# x:31 y:626
			OperatableStateMachine.add('transport__Trajectory',
										RunTrajectory(file="transport", duration=0),
										transitions={'done': 'success'},
										autonomy={'done': Autonomy.Off})

			# x:69 y:120
			OperatableStateMachine.add('opengripper',
										SetGripperState(width=0.25, effort=1),
										transitions={'object': 'receive_bag__Trajectory', 'no_object': 'receive_bag__Trajectory'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:334 y:440
			OperatableStateMachine.add('transport__Trajectory_2',
										RunTrajectory(file="transport", duration=0),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})


		# x:171 y:527, x:563 y:423
		_sm_deusexpickrecovery_7 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['misplacedObject'])

		with _sm_deusexpickrecovery_7:
			# x:66 y:49
			OperatableStateMachine.add('posePlusEnArriere',
										GenPoseEuler(x=-0.2, y=0, z=0, roll=0, pitch=0, yaw=0),
										transitions={'done': 'moveBack'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose': 'pose'})

			# x:133 y:404
			OperatableStateMachine.add('ReceiveItem',
										_sm_receiveitem_6,
										transitions={'failed': 'Oh fuck', 'success': 'finished'},
										autonomy={'failed': Autonomy.Inherit, 'success': Autonomy.Inherit})

			# x:98 y:158
			OperatableStateMachine.add('moveBack',
										SaraMoveBase(reference="base_link"),
										transitions={'arrived': 'GimmeTheObject', 'failed': 'GimmeTheObject'},
										autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'pose'})

			# x:113 y:276
			OperatableStateMachine.add('GimmeTheObject',
										SaraSay(sentence=lambda x: "Could you give me the "+x[0][0].name+", please ?", input_keys=["misplacedObject"], emotion=0, block=True),
										transitions={'done': 'ReceiveItem'},
										autonomy={'done': Autonomy.Off},
										remapping={'misplacedObject': 'misplacedObject'})

			# x:370 y:405
			OperatableStateMachine.add('Oh fuck',
										SaraSay(sentence="Oh. Nevermind then.", input_keys=[], emotion=2, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})


		# x:631 y:390, x:1158 y:270
		_sm_grabmisplacedobject_8 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['misplacedObject'])

		with _sm_grabmisplacedobject_8:
			# x:72 y:35
			OperatableStateMachine.add('GetObjectId',
										CalculationState(calculation=lambda x: x[0].ID),
										transitions={'done': 'Action_pick'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'misplacedObject', 'output_value': 'misplacedObjectID'})

			# x:307 y:89
			OperatableStateMachine.add('oops',
										SaraSay(sentence="Oops. I dropped the object!", input_keys=[], emotion=5, block=True),
										transitions={'done': 'DeusExPickRecovery'},
										autonomy={'done': Autonomy.Off})

			# x:344 y:157
			OperatableStateMachine.add('oops_2',
										SaraSay(sentence="Oops. Seems I can't reach the object!", input_keys=[], emotion=3, block=True),
										transitions={'done': 'DeusExPickRecovery'},
										autonomy={'done': Autonomy.Off})

			# x:362 y:239
			OperatableStateMachine.add('oops_3',
										SaraSay(sentence="Oops. I can't see the object!", input_keys=[], emotion=3, block=True),
										transitions={'done': 'DeusExPickRecovery'},
										autonomy={'done': Autonomy.Off})

			# x:42 y:275
			OperatableStateMachine.add('Action_pick',
										self.use_behavior(sara_flexbe_behaviors__Action_pickSM, 'PickMisplacedObject/GrabMisplacedObject/Action_pick', default_keys=['Entity']),
										transitions={'success': 'done', 'unreachable': 'oops_2', 'not found': 'oops_3', 'dropped': 'oops'},
										autonomy={'success': Autonomy.Inherit, 'unreachable': Autonomy.Inherit, 'not found': Autonomy.Inherit, 'dropped': Autonomy.Inherit},
										remapping={'objectID': 'misplacedObjectID'})

			# x:600 y:177
			OperatableStateMachine.add('DeusExPickRecovery',
										_sm_deusexpickrecovery_7,
										transitions={'finished': 'done', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'misplacedObject': 'misplacedObject'})


		# x:30 y:458
		_sm_lookaround_9 = OperatableStateMachine(outcomes=['finished'])

		with _sm_lookaround_9:
			# x:57 y:262
			OperatableStateMachine.add('left',
										SaraSetHeadAngle(pitch=0.9, yaw=1),
										transitions={'done': 'w1'},
										autonomy={'done': Autonomy.Off})

			# x:206 y:372
			OperatableStateMachine.add('center2',
										SaraSetHeadAngle(pitch=0.9, yaw=0),
										transitions={'done': 'w4'},
										autonomy={'done': Autonomy.Off})

			# x:70 y:160
			OperatableStateMachine.add('w1',
										WaitState(wait_time=4),
										transitions={'done': 'center'},
										autonomy={'done': Autonomy.Off})

			# x:413 y:159
			OperatableStateMachine.add('w2',
										WaitState(wait_time=4),
										transitions={'done': 'right'},
										autonomy={'done': Autonomy.Off})

			# x:415 y:370
			OperatableStateMachine.add('w3',
										WaitState(wait_time=4),
										transitions={'done': 'center2'},
										autonomy={'done': Autonomy.Off})

			# x:215 y:156
			OperatableStateMachine.add('center',
										SaraSetHeadAngle(pitch=0.9, yaw=0),
										transitions={'done': 'w2'},
										autonomy={'done': Autonomy.Off})

			# x:221 y:476
			OperatableStateMachine.add('w4',
										WaitState(wait_time=4),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:394 y:262
			OperatableStateMachine.add('right',
										SaraSetHeadAngle(pitch=0.9, yaw=-1),
										transitions={'done': 'w3'},
										autonomy={'done': Autonomy.Off})


		# x:461 y:579
		_sm_listentities_10 = OperatableStateMachine(outcomes=['found'], input_keys=['nameFilter'], output_keys=['unexpected_objects'])

		with _sm_listentities_10:
			# x:123 y:82
			OperatableStateMachine.add('ListEntities',
										list_entities_by_name(frontality_level=0.5, distance_max=1.5),
										transitions={'found': 'remove persons', 'none_found': 'ListEntities'},
										autonomy={'found': Autonomy.Off, 'none_found': Autonomy.Off},
										remapping={'name': 'nameFilter', 'entity_list': 'entity_list', 'number': 'number'})

			# x:118 y:274
			OperatableStateMachine.add('remove persons',
										Filter(filter=lambda x: x.name != "person"),
										transitions={'done': 'check if zero'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_list': 'entity_list', 'output_list': 'entity_list'})

			# x:378 y:80
			OperatableStateMachine.add('check if zero',
										CheckConditionState(predicate=lambda x: len(x) == 0),
										transitions={'true': 'ListEntities', 'false': 'check wonderland'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'entity_list'})

			# x:382 y:366
			OperatableStateMachine.add('check wonderland',
										CheckMisplacedObjects(position_tolerance=0.5, default_destination="trash bin"),
										transitions={'all_expected': 'ListEntities', 'unexpected': 'found'},
										autonomy={'all_expected': Autonomy.Off, 'unexpected': Autonomy.Off},
										remapping={'entities': 'entity_list', 'expected_objects': 'expected_objects', 'unexpected_objects': 'unexpected_objects'})


		# x:30 y:458, x:130 y:458, x:230 y:458, x:330 y:458
		_sm_scanaround_11 = ConcurrencyContainer(outcomes=['found', 'not_found'], input_keys=['nameFilter'], output_keys=['unexpected_objects'], conditions=[
										('found', [('ListEntities', 'found')]),
										('not_found', [('LookAround', 'finished')])
										])

		with _sm_scanaround_11:
			# x:154 y:40
			OperatableStateMachine.add('ListEntities',
										_sm_listentities_10,
										transitions={'found': 'found'},
										autonomy={'found': Autonomy.Inherit},
										remapping={'nameFilter': 'nameFilter', 'unexpected_objects': 'unexpected_objects'})

			# x:261 y:111
			OperatableStateMachine.add('LookAround',
										_sm_lookaround_9,
										transitions={'finished': 'not_found'},
										autonomy={'finished': Autonomy.Inherit})


		# x:550 y:171, x:130 y:458
		_sm_scan_surface_12 = OperatableStateMachine(outcomes=['found', 'not_found'], input_keys=['nameFilter'], output_keys=['unexpected_objects'])

		with _sm_scan_surface_12:
			# x:41 y:40
			OperatableStateMachine.add('CheckForUnknownObjs',
										SetSegmentationRosParam(ValueTableSegmentation=True, ValueObjectSegmentation=True),
										transitions={'done': 'ScanAround'},
										autonomy={'done': Autonomy.Off})

			# x:28 y:283
			OperatableStateMachine.add('StopCheckingForUnknownObj',
										SetSegmentationRosParam(ValueTableSegmentation=False, ValueObjectSegmentation=False),
										transitions={'done': 'not_found'},
										autonomy={'done': Autonomy.Off})

			# x:64 y:151
			OperatableStateMachine.add('ScanAround',
										_sm_scanaround_11,
										transitions={'found': 'StopCheckingForUnknownObj_2', 'not_found': 'StopCheckingForUnknownObj'},
										autonomy={'found': Autonomy.Inherit, 'not_found': Autonomy.Inherit},
										remapping={'nameFilter': 'nameFilter', 'unexpected_objects': 'unexpected_objects'})

			# x:260 y:153
			OperatableStateMachine.add('StopCheckingForUnknownObj_2',
										SetSegmentationRosParam(ValueTableSegmentation=False, ValueObjectSegmentation=False),
										transitions={'done': 'found'},
										autonomy={'done': Autonomy.Off})


		# x:680 y:561, x:85 y:153, x:59 y:725
		_sm_checkatwaypoints_13 = OperatableStateMachine(outcomes=['found', 'noneFound', 'failed'], input_keys=['waypointToCheckDict', 'cleaningRoom', 'nameFilter'], output_keys=['misplacedObject'])

		with _sm_checkatwaypoints_13:
			# x:60 y:44
			OperatableStateMachine.add('GetNbOfWaypoints',
										FlexibleCalculationState(calculation=lambda x: len(x[1][x[0]]), input_keys=["cleaningRoom","waypointToCheckDict"]),
										transitions={'done': 'len'},
										autonomy={'done': Autonomy.Off},
										remapping={'cleaningRoom': 'cleaningRoom', 'waypointToCheckDict': 'waypointToCheckDict', 'output_value': 'lenWaypointDict'})

			# x:483 y:544
			OperatableStateMachine.add('GetFirstElement',
										CalculationState(calculation=lambda x:x[0]),
										transitions={'done': 'found'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'unexpected_objects', 'output_value': 'misplacedObject'})

			# x:35 y:461
			OperatableStateMachine.add('say check next',
										SaraSay(sentence=lambda x: "I'll check at the " + x[0], input_keys=["entity"], emotion=1, block=True),
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Off},
										remapping={'entity': 'waypointToGo'})

			# x:18 y:545
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'CheckForMisplacedObjects/CheckAtWaypoints/Action_Move'),
										transitions={'finished': 'scan surface', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'waypointToGo'})

			# x:218 y:142
			OperatableStateMachine.add('CheckAtEachLocation',
										ForLoopWithInput(repeat=10),
										transitions={'do': 'CheckIfLastLocationOfList', 'end': 'noneFound'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index_in': 'locationToGet', 'index_out': 'locationToGet'})

			# x:433 y:43
			OperatableStateMachine.add('StartLoop',
										SetKey(Value=-1),
										transitions={'done': 'CheckAtEachLocation'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'locationToGet'})

			# x:24 y:341
			OperatableStateMachine.add('GetLocation',
										FlexibleCalculationState(calculation=lambda x: x[1][x[2]][x[0]], input_keys=["index_out","waypointToCheckDict","cleaningRoom"]),
										transitions={'done': 'say check next'},
										autonomy={'done': Autonomy.Off},
										remapping={'index_out': 'locationToGet', 'waypointToCheckDict': 'waypointToCheckDict', 'cleaningRoom': 'cleaningRoom', 'output_value': 'waypointToGo'})

			# x:26 y:243
			OperatableStateMachine.add('CheckIfLastLocationOfList',
										FlexibleCheckConditionState(predicate=lambda x: x[0]-1 < x[1], input_keys=["lenWaypointDict","locationToGet"]),
										transitions={'true': 'noneFound', 'false': 'GetLocation'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'lenWaypointDict': 'lenWaypointDict', 'locationToGet': 'locationToGet'})

			# x:266 y:41
			OperatableStateMachine.add('len',
										LogKeyState(text='Qty of sub-waypoints: {}', severity=Logger.REPORT_HINT),
										transitions={'done': 'StartLoop'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'lenWaypointDict'})

			# x:287 y:544
			OperatableStateMachine.add('scan surface',
										_sm_scan_surface_12,
										transitions={'found': 'GetFirstElement', 'not_found': 'CheckAtEachLocation'},
										autonomy={'found': Autonomy.Inherit, 'not_found': Autonomy.Inherit},
										remapping={'nameFilter': 'nameFilter', 'unexpected_objects': 'unexpected_objects'})


		# x:709 y:520, x:850 y:66
		_sm_enterarena_14 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['roomQuestion', 'doorName', 'skipDoorEntrance'], output_keys=['cleanupRoom'])

		with _sm_enterarena_14:
			# x:77 y:28
			OperatableStateMachine.add('Init_Sequence',
										self.use_behavior(sara_flexbe_behaviors__Init_SequenceSM, 'EnterArena/Init_Sequence'),
										transitions={'finished': 'SkipEntrance', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:278 y:473
			OperatableStateMachine.add('NLU',
										_sm_nlu_1,
										transitions={'done': 'done', 'failed': 'Sorry'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'roomAnswer': 'roomAnswer', 'cleanupRoom': 'cleanupRoom'})

			# x:467 y:87
			OperatableStateMachine.add('Action_Pass_Door',
										self.use_behavior(sara_flexbe_behaviors__Action_Pass_DoorSM, 'EnterArena/Action_Pass_Door'),
										transitions={'Done': 'RetryOnce', 'Fail': 'failed'},
										autonomy={'Done': Autonomy.Inherit, 'Fail': Autonomy.Inherit},
										remapping={'DoorName': 'doorName'})

			# x:234 y:259
			OperatableStateMachine.add('RetryOnce',
										ForLoop(repeat=2),
										transitions={'do': 'Ask', 'end': 'failed'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index'})

			# x:295 y:354
			OperatableStateMachine.add('Sorry',
										SaraSay(sentence="Sorry, I misunderstood.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'RetryOnce'},
										autonomy={'done': Autonomy.Off})

			# x:213 y:119
			OperatableStateMachine.add('SkipEntrance',
										CheckConditionState(predicate=lambda x: x),
										transitions={'true': 'RetryOnce', 'false': 'Action_Pass_Door'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'skipDoorEntrance'})

			# x:51 y:354
			OperatableStateMachine.add('Ask',
										_sm_ask_0,
										transitions={'finished': 'log', 'failed': 'RetryOnce'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'roomQuestion': 'roomQuestion', 'roomAnswer': 'roomAnswer'})

			# x:133 y:492
			OperatableStateMachine.add('log',
										LogKeyState(text="Text :{}", severity=Logger.REPORT_HINT),
										transitions={'done': 'NLU'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'roomAnswer'})


		# x:736 y:312
		_sm_putobjectindesiredcontainer_15 = OperatableStateMachine(outcomes=['finished'], input_keys=['misplacedObject', 'placedObjects'], output_keys=['placedObjects'])

		with _sm_putobjectindesiredcontainer_15:
			# x:138 y:153
			OperatableStateMachine.add('GotoDesiredContainer',
										_sm_gotodesiredcontainer_5,
										transitions={'done': 'PutDownObject', 'failed': 'CantGoToDestination'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'misplacedObject': 'misplacedObject'})

			# x:277 y:313
			OperatableStateMachine.add('PutDownObject',
										_sm_putdownobject_4,
										transitions={'done': 'OneMoreObjectPlaced'},
										autonomy={'done': Autonomy.Inherit},
										remapping={'misplacedObject': 'misplacedObject'})

			# x:339 y:80
			OperatableStateMachine.add('CantGoToDestination',
										_sm_cantgotodestination_3,
										transitions={'finished': 'finished'},
										autonomy={'finished': Autonomy.Inherit},
										remapping={'misplacedObject': 'misplacedObject'})

			# x:468 y:381
			OperatableStateMachine.add('OneMoreObjectPlaced',
										CalculationState(calculation=lambda x: x+1),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'placedObjects', 'output_value': 'placedObjects'})


		# x:592 y:92, x:527 y:277
		_sm_pickmisplacedobject_16 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['misplacedObject', 'waypointGenerationDistance'])

		with _sm_pickmisplacedobject_16:
			# x:162 y:126
			OperatableStateMachine.add('GrabMisplacedObject',
										_sm_grabmisplacedobject_8,
										transitions={'done': 'finished', 'failed': 'failed'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'misplacedObject': 'misplacedObject'})


		# x:627 y:203, x:639 y:122, x:646 y:50
		_sm_checkformisplacedobjects_17 = OperatableStateMachine(outcomes=['noneLeft', 'found', 'failed'], input_keys=['nameFilter', 'waypointToCheckDict', 'cleaningRoom', 'placedObjects'], output_keys=['misplacedObject'])

		with _sm_checkformisplacedobjects_17:
			# x:71 y:41
			OperatableStateMachine.add('CheckIf5Placed',
										CheckConditionState(predicate=lambda x: x >= 5),
										transitions={'true': 'OkItsClean', 'false': 'CheckAtWaypoints'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'placedObjects'})

			# x:73 y:160
			OperatableStateMachine.add('OkItsClean',
										SaraSay(sentence="I cleaned the room!", input_keys=[], emotion=1, block=True),
										transitions={'done': 'noneLeft'},
										autonomy={'done': Autonomy.Off})

			# x:340 y:64
			OperatableStateMachine.add('CheckAtWaypoints',
										_sm_checkatwaypoints_13,
										transitions={'found': 'found', 'noneFound': 'OkItsClean', 'failed': 'failed'},
										autonomy={'found': Autonomy.Inherit, 'noneFound': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'waypointToCheckDict': 'waypointToCheckDict', 'cleaningRoom': 'cleaningRoom', 'nameFilter': 'nameFilter', 'misplacedObject': 'misplacedObject'})


		# x:644 y:459, x:651 y:336
		_sm_gotoroom_18 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['cleanupRoom', 'firstTimeInRoom'], output_keys=['firstTimeInRoom'])

		with _sm_gotoroom_18:
			# x:141 y:121
			OperatableStateMachine.add('IsItMyFirstTime',
										DecisionState(outcomes=["no", "yes"], conditions=lambda x: x),
										transitions={'no': 'GoingBackToTheRoom', 'yes': 'OkImGoingToTheRoom'},
										autonomy={'no': Autonomy.Off, 'yes': Autonomy.Off},
										remapping={'input_value': 'firstTimeInRoom'})

			# x:130 y:220
			OperatableStateMachine.add('GoingBackToTheRoom',
										SaraSay(sentence=lambda x: "I'm going back to the "+str(x[0])+".", input_keys=["cleanupRoom"], emotion=0, block=True),
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Off},
										remapping={'cleanupRoom': 'cleanupRoom'})

			# x:342 y:171
			OperatableStateMachine.add('OkImGoingToTheRoom',
										SaraSay(sentence=lambda x: "Okay, I'm going to the "+str(x[0])+".", input_keys=["cleanupRoom"], emotion=0, block=True),
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Off},
										remapping={'cleanupRoom': 'cleanupRoom'})

			# x:330 y:448
			OperatableStateMachine.add('IWentThere',
										SetKey(Value="no"),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'firstTimeInRoom'})

			# x:320 y:326
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'GoToRoom/Action_Move'),
										transitions={'finished': 'IWentThere', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'cleanupRoom'})



		with _state_machine:
			# x:245 y:149
			OperatableStateMachine.add('GoToRoom',
										_sm_gotoroom_18,
										transitions={'done': 'CheckForMisplacedObjects', 'failed': 'failed'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'cleanupRoom': 'cleanupRoom', 'firstTimeInRoom': 'firstTimeInRoom'})

			# x:7 y:307
			OperatableStateMachine.add('CheckForMisplacedObjects',
										_sm_checkformisplacedobjects_17,
										transitions={'noneLeft': 'done', 'found': 'PickMisplacedObject', 'failed': 'failed'},
										autonomy={'noneLeft': Autonomy.Inherit, 'found': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'nameFilter': 'nameFilter', 'waypointToCheckDict': 'waypointToCheckDict', 'cleaningRoom': 'cleanupRoom', 'placedObjects': 'placedObjects', 'misplacedObject': 'misplacedObject'})

			# x:232 y:497
			OperatableStateMachine.add('PickMisplacedObject',
										_sm_pickmisplacedobject_16,
										transitions={'finished': 'PutObjectInDesiredContainer', 'failed': 'GoToRoom'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'misplacedObject': 'misplacedObject', 'waypointGenerationDistance': 'waypointGenerationDistance'})

			# x:442 y:337
			OperatableStateMachine.add('PutObjectInDesiredContainer',
										_sm_putobjectindesiredcontainer_15,
										transitions={'finished': 'GoToRoom'},
										autonomy={'finished': Autonomy.Inherit},
										remapping={'misplacedObject': 'misplacedObject', 'placedObjects': 'placedObjects'})

			# x:247 y:42
			OperatableStateMachine.add('EnterArena',
										_sm_enterarena_14,
										transitions={'done': 'GoToRoom', 'failed': 'failed'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'roomQuestion': 'roomQuestion', 'doorName': 'doorName', 'skipDoorEntrance': 'skipDoorEntrance', 'cleanupRoom': 'cleanupRoom'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
