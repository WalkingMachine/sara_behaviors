#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_behaviors.action_ask_sm import Action_AskSM as sara_flexbe_behaviors__Action_AskSM
from flexbe_states.decision_state import DecisionState
from sara_flexbe_behaviors.action_move_sm import Action_MoveSM as sara_flexbe_behaviors__Action_MoveSM
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.for_loop import ForLoop
from sara_flexbe_states.CheckMisplacedObjects import CheckMisplacedObjects
from sara_flexbe_states.sara_set_head_angle import SaraSetHeadAngle
from flexbe_states.wait_state import WaitState
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.list_entities_by_name import list_entities_by_name
from sara_flexbe_states.get_reachable_waypoint import Get_Reacheable_Waypoint
from sara_flexbe_behaviors.action_pick_sm import Action_pickSM as sara_flexbe_behaviors__Action_pickSM
from sara_flexbe_states.set_gripper_state import SetGripperState
from sara_flexbe_states.torque_reader import ReadTorque
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_states.moveit_move import MoveitMove
from sara_flexbe_states.pose_gen_euler import GenPoseEuler
from sara_flexbe_behaviors.action_place_sm import Action_placeSM as sara_flexbe_behaviors__Action_placeSM
from sara_flexbe_states.WonderlandGetEntityByID import WonderlandGetEntityByID
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Mar 11 2019
@author: Raphaël Duchaîne
'''
class Scenario_Housekeeper_CleanUp2SM(Behavior):
	'''
	Search items and put them at there place or in the trash can if the item is unknown
	'''


	def __init__(self):
		super(Scenario_Housekeeper_CleanUp2SM, self).__init__()
		self.name = 'Scenario_Housekeeper_CleanUp2'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(sara_flexbe_behaviors__Action_AskSM, 'EnterArena/Action_Ask')
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'GoToRoom/Action_Move')
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'PickMisplacedObject/Action_Move')
		self.add_behavior(sara_flexbe_behaviors__Action_pickSM, 'PickMisplacedObject/GrabMisplacedObject/Action_pick')
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'PutObjectInDesiredContainer/GotoDesiredContainer/Action_Move')
		self.add_behavior(sara_flexbe_behaviors__Action_placeSM, 'PutObjectInDesiredContainer/PutDownObject/Action_place')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
    
        # [/MANUAL_INIT]

		# Behavior comments:

		# O 663 249 /PickMisplacedObject
		# Va à l'objet trouvé et prend l'objet|n|nRappel: MisplacedObject contient la liste [entité originale, pseudo-entité wonderland]|n|nTODO:|nRecovery si on est pas capable de se rendre.

		# O 829 281 /PutObjectInDesiredContainer
		# Va au contenant désiré de l'objet et dépose l'objet à celui-ci|nSi elle echappe l'objet, elle le signale.|nTODO: Si elle ne peut pas se rendre a la destination ?

		# O 887 294 /CheckForMisplacedObjects
		# Vérifie la liste d'objet connus si il y en a qui ne sont pas à la bonne place.|nSi aucun n'est trouvé; SARA va regarder autour pour trouver des objets.|n|nAmélioration possible:|nDans ScanAround, faire aller à des Waypoints prédéterminés pour mieux voir.|nAjouter la question: Il reste tu des objets si yen a pas de trouvé et qu'on a moins de 5 objets de ramassés|n|nTODO:|n2e etape de recovery: Aller à des waypoints clés ET/OU containers.|nRajouter la segmentation pour objets inconnus aux points clés.

		# O 449 37 /EnterArena
		# SARA entre dans l'aréna et demande à l'opérateur dans quelle piece elle doir faire le ménage. Ensuite elle y va.|nNote:|nIl va falloir qu'il y aie des waypoint qui matche le nom de la pièce.|nTODO:|n- State qui fait le NLU pour retrouver le nom de la pièce dans la réponse.|n- Recovery si le nom ne correpond pas|n- Inititailisation (Acation Init)|n- Faire entrer le robot (ActionPassDoor)

		# O 875 394 
		# TODO:|nSaraSay àa chaque fois que le robot va bouger pour signaler à l'avance

		# O 430 83 /Loop
		# SARA retourne à la pièce à cleaner

		# O 353 125 /PickMisplacedObject/GrabMisplacedObject/DeusExPickRecovery
		# NOTE: noms des position de réception pour l'item à vérifier !

		# O 528 83 /CheckForMisplacedObjects/ScanAround
		# Liseter les entités en concurrent et checker si c'est des misplace. Lorsque Un est trouvé faire un interrupt

		# O 49 330 /PickMisplacedObject/GrabMisplacedObject/DeusExPickRecovery/ReceiveItem
		# Remplacer Moveit Par RunTrajectory|n|nfail si pas recus à close



	def create(self):
		# x:976 y:173, x:672 y:46
		_state_machine = OperatableStateMachine(outcomes=['done', 'failed'])
		_state_machine.userdata.nameFilter = ""
		_state_machine.userdata.roomQuestion = "what room shall i clean, master ?"
		_state_machine.userdata.waypointGenerationDistance = 0.5
		_state_machine.userdata.placeholder = ""

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

		# x:186 y:370
		_sm_deusexplacerecovery_0 = OperatableStateMachine(outcomes=['finished'], input_keys=['misplacedObject'])

		with _sm_deusexplacerecovery_0:
			# x:85 y:72
			OperatableStateMachine.add('getContainerId',
										CalculationState(calculation=lambda x: x[1].containerId),
										transitions={'done': 'getContainerEntity'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'misplacedObject', 'output_value': 'containerId'})

			# x:234 y:149
			OperatableStateMachine.add('getContainerEntity',
										WonderlandGetEntityByID(),
										transitions={'found': 'ItGoesThere', 'not_found': 'finished', 'error': 'finished'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off, 'error': Autonomy.Off},
										remapping={'id': 'containerId', 'entity': 'containerEntity', 'depth_position': 'depth_position', 'depth_waypoint': 'depth_waypoint'})

			# x:366 y:284
			OperatableStateMachine.add('ItGoesThere',
										SaraSay(sentence=lambda x: "Looks like I dropped "+str(x[0][0].name)+". Can you put it in the "+ x[1].name+"?", input_keys=[misplacedObject,containerEntity], emotion=0, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		# x:211 y:359
		_sm_cantgotodestination_1 = OperatableStateMachine(outcomes=['finished'])

		with _sm_cantgotodestination_1:
			# x:99 y:132
			OperatableStateMachine.add('meow',
										SaraSay(sentence=lambda x: "Meow.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		# x:632 y:527
		_sm_putdownobject_2 = OperatableStateMachine(outcomes=['done'], input_keys=['misplacedObject'])

		with _sm_putdownobject_2:
			# x:70 y:215
			OperatableStateMachine.add('GetDroppingPose',
										GenPoseEuler(x=0.3, y=0, z=1.2, roll=0.0, pitch=0.0, yaw=0.0),
										transitions={'done': 'Action_place'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose': 'droppingPose'})

			# x:269 y:215
			OperatableStateMachine.add('Action_place',
										self.use_behavior(sara_flexbe_behaviors__Action_placeSM, 'PutObjectInDesiredContainer/PutDownObject/Action_place'),
										transitions={'finished': 'done', 'failed': 'DeusExPlaceRecovery'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pos': 'droppingPose'})

			# x:592 y:127
			OperatableStateMachine.add('DeusExPlaceRecovery',
										_sm_deusexplacerecovery_0,
										transitions={'finished': 'done'},
										autonomy={'finished': Autonomy.Inherit},
										remapping={'misplacedObject': 'misplacedObject'})


		# x:518 y:44, x:531 y:152
		_sm_gotodesiredcontainer_3 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['misplacedObject'])

		with _sm_gotodesiredcontainer_3:
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


		# x:300 y:141, x:893 y:63
		_sm_receiveitem_4 = OperatableStateMachine(outcomes=['failed', 'success'])

		with _sm_receiveitem_4:
			# x:69 y:47
			OperatableStateMachine.add('opengripper',
										SetGripperState(width=0.25, effort=1),
										transitions={'object': 'setTarget1', 'no_object': 'setTarget1'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:280 y:263
			OperatableStateMachine.add('Torque_Reader',
										ReadTorque(watchdog=10, Joint="right_elbow_pitch_joint", Threshold=1, min_time=1),
										transitions={'threshold': 'close_gripper', 'watchdog': 'Torque_Reader', 'fail': 'failed'},
										autonomy={'threshold': Autonomy.Off, 'watchdog': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'torque': 'torque'})

			# x:668 y:149
			OperatableStateMachine.add('setTarget2',
										SetKey(Value="PostGripPose"),
										transitions={'done': 'Go_to_Pose'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'target'})

			# x:51 y:261
			OperatableStateMachine.add('Go_to_receive_bag_pose',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'Torque_Reader', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'target'})

			# x:450 y:274
			OperatableStateMachine.add('close_gripper',
										SetGripperState(width=0, effort=1),
										transitions={'object': 'thank you', 'no_object': 'failed'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:640 y:273
			OperatableStateMachine.add('thank you',
										SaraSay(sentence="Thank you", input_keys=[], emotion=1, block=True),
										transitions={'done': 'setTarget2'},
										autonomy={'done': Autonomy.Off})

			# x:50 y:141
			OperatableStateMachine.add('setTarget1',
										SetKey(Value="Help_me_carry"),
										transitions={'done': 'Go_to_receive_bag_pose'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'target'})

			# x:660 y:57
			OperatableStateMachine.add('Go_to_Pose',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'success', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'target'})


		# x:169 y:514, x:508 y:495
		_sm_deusexpickrecovery_5 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['misplacedObject'])

		with _sm_deusexpickrecovery_5:
			# x:81 y:50
			OperatableStateMachine.add('GimmeTheObjict',
										SaraSay(sentence=lambda x: "Could you give me the "+x[0][0].name+", please ?", input_keys=["misplacedObject"], emotion=0, block=True),
										transitions={'done': 'ReceiveItem'},
										autonomy={'done': Autonomy.Off},
										remapping={'misplacedObject': 'misplacedObject'})

			# x:213 y:130
			OperatableStateMachine.add('ReceiveItem',
										_sm_receiveitem_4,
										transitions={'failed': 'Oh fuck', 'success': 'finished'},
										autonomy={'failed': Autonomy.Inherit, 'success': Autonomy.Inherit})

			# x:355 y:262
			OperatableStateMachine.add('Oh fuck',
										SaraSay(sentence="Oh. Nevermind then.", input_keys=[], emotion=2, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})


		# x:623 y:609, x:1158 y:270
		_sm_grabmisplacedobject_6 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['misplacedObject'])

		with _sm_grabmisplacedobject_6:
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
										remapping={'objectID': 'misplacedObjectID', 'Entity': 'Entity'})

			# x:600 y:177
			OperatableStateMachine.add('DeusExPickRecovery',
										_sm_deusexpickrecovery_5,
										transitions={'finished': 'done', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'misplacedObject': 'misplacedObject'})


		# x:547 y:290
		_sm_scanaround_7 = OperatableStateMachine(outcomes=['done'], input_keys=['input_value'])

		with _sm_scanaround_7:
			# x:172 y:46
			OperatableStateMachine.add('center',
										SaraSetHeadAngle(pitch=0.1, yaw=0),
										transitions={'done': 'w2'},
										autonomy={'done': Autonomy.Off})

			# x:304 y:122
			OperatableStateMachine.add('right',
										SaraSetHeadAngle(pitch=0.1, yaw=-1.5),
										transitions={'done': 'w3'},
										autonomy={'done': Autonomy.Off})

			# x:165 y:187
			OperatableStateMachine.add('center2',
										SaraSetHeadAngle(pitch=0.1, yaw=0),
										transitions={'done': 'w4'},
										autonomy={'done': Autonomy.Off})

			# x:195 y:276
			OperatableStateMachine.add('w1',
										WaitState(wait_time=1),
										transitions={'done': 'center3'},
										autonomy={'done': Autonomy.Off})

			# x:309 y:49
			OperatableStateMachine.add('w2',
										WaitState(wait_time=4),
										transitions={'done': 'right'},
										autonomy={'done': Autonomy.Off})

			# x:308 y:187
			OperatableStateMachine.add('w3',
										WaitState(wait_time=4),
										transitions={'done': 'center2'},
										autonomy={'done': Autonomy.Off})

			# x:56 y:191
			OperatableStateMachine.add('w4',
										WaitState(wait_time=4),
										transitions={'done': 'left'},
										autonomy={'done': Autonomy.Off})

			# x:40 y:270
			OperatableStateMachine.add('left',
										SaraSetHeadAngle(pitch=0.1, yaw=1.5),
										transitions={'done': 'w1'},
										autonomy={'done': Autonomy.Off})

			# x:317 y:277
			OperatableStateMachine.add('center3',
										SaraSetHeadAngle(pitch=0.1, yaw=0),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off})


		# x:30 y:365, x:130 y:365
		_sm_nluplaceholder_8 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['answer'], output_keys=['room'])

		with _sm_nluplaceholder_8:
			# x:57 y:143
			OperatableStateMachine.add('placeHolder',
										DecisionState(outcomes=["done","failed"], conditions=lambda x:"done"),
										transitions={'done': 'done', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'input_value': 'answer'})


		# x:655 y:306
		_sm_putobjectindesiredcontainer_9 = OperatableStateMachine(outcomes=['finished'], input_keys=['misplacedObject', 'placeholder'])

		with _sm_putobjectindesiredcontainer_9:
			# x:138 y:153
			OperatableStateMachine.add('GotoDesiredContainer',
										_sm_gotodesiredcontainer_3,
										transitions={'done': 'PutDownObject', 'failed': 'CantGoToDestination'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'misplacedObject': 'misplacedObject'})

			# x:404 y:262
			OperatableStateMachine.add('PutDownObject',
										_sm_putdownobject_2,
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Inherit},
										remapping={'misplacedObject': 'misplacedObject'})

			# x:391 y:120
			OperatableStateMachine.add('CantGoToDestination',
										_sm_cantgotodestination_1,
										transitions={'finished': 'finished'},
										autonomy={'finished': Autonomy.Inherit})


		# x:609 y:528, x:593 y:240
		_sm_pickmisplacedobject_10 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['misplacedObject', 'waypointGenerationDistance'])

		with _sm_pickmisplacedobject_10:
			# x:82 y:71
			OperatableStateMachine.add('GetObjectPosition',
										CalculationState(calculation=lambda x: x[0].position),
										transitions={'done': 'FindAWay'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'misplacedObject', 'output_value': 'misplacedObjectPosition'})

			# x:65 y:330
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'PickMisplacedObject/Action_Move'),
										transitions={'finished': 'GrabMisplacedObject', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'misplacedObjectWaypoint'})

			# x:82 y:202
			OperatableStateMachine.add('FindAWay',
										Get_Reacheable_Waypoint(),
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose_in': 'misplacedObjectPosition', 'distance': 'waypointGenerationDistance', 'pose_out': 'misplacedObjectWaypoint'})

			# x:58 y:514
			OperatableStateMachine.add('GrabMisplacedObject',
										_sm_grabmisplacedobject_6,
										transitions={'done': 'finished', 'failed': 'failed'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'misplacedObject': 'misplacedObject'})


		# x:842 y:91, x:286 y:680
		_sm_checkformisplacedobjects_11 = OperatableStateMachine(outcomes=['noneLeft', 'found'], input_keys=['nameFilter'], output_keys=['misplacedObject'])

		with _sm_checkformisplacedobjects_11:
			# x:282 y:89
			OperatableStateMachine.add('ScanOnce',
										ForLoop(repeat=1),
										transitions={'do': 'ListEntities', 'end': 'noneLeft'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index'})

			# x:243 y:346
			OperatableStateMachine.add('CheckMisplacedObjects',
										CheckMisplacedObjects(position_tolerance=0.1, default_destination="bin"),
										transitions={'all_expected': 'ScanAround', 'unexpected': 'GetFirstElement'},
										autonomy={'all_expected': Autonomy.Off, 'unexpected': Autonomy.Off},
										remapping={'entities': 'entity_list', 'expected_objects': 'expected_objects', 'unexpected_objects': 'unexpected_objects'})

			# x:374 y:186
			OperatableStateMachine.add('ScanAround',
										_sm_scanaround_7,
										transitions={'done': 'ScanOnce'},
										autonomy={'done': Autonomy.Inherit},
										remapping={'input_value': 'nameFilter'})

			# x:259 y:579
			OperatableStateMachine.add('GetFirstElement',
										CalculationState(calculation=lambda x:x[0]),
										transitions={'done': 'found'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'entity_list', 'output_value': 'misplacedObject'})

			# x:125 y:184
			OperatableStateMachine.add('ListEntities',
										list_entities_by_name(frontality_level=0.5, distance_max=10),
										transitions={'found': 'CheckMisplacedObjects', 'none_found': 'ScanAround'},
										autonomy={'found': Autonomy.Off, 'none_found': Autonomy.Off},
										remapping={'name': 'nameFilter', 'entity_list': 'entity_list', 'number': 'number'})


		# x:130 y:465, x:230 y:465
		_sm_saydone_12 = OperatableStateMachine(outcomes=['done', 'failed'])

		with _sm_saydone_12:
			# x:140 y:157
			OperatableStateMachine.add('Looked all around the house',
										SaraSay(sentence="Bleh.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off})


		# x:130 y:465, x:377 y:315
		_sm_gotoroom_13 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['cleanupRoom'])

		with _sm_gotoroom_13:
			# x:78 y:124
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'GoToRoom/Action_Move'),
										transitions={'finished': 'done', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'cleanupRoom'})


		# x:364 y:525, x:395 y:172
		_sm_enterarena_14 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['roomQuestion'], output_keys=['cleanupRoom'])

		with _sm_enterarena_14:
			# x:108 y:67
			OperatableStateMachine.add('Action_Ask',
										self.use_behavior(sara_flexbe_behaviors__Action_AskSM, 'EnterArena/Action_Ask'),
										transitions={'finished': 'NLUplaceholder', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'question': 'roomQuestion', 'answer': 'roomAnswer'})

			# x:111 y:187
			OperatableStateMachine.add('NLUplaceholder',
										_sm_nluplaceholder_8,
										transitions={'done': 'done', 'failed': 'failed'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'answer': 'roomAnswer', 'room': 'cleanupRoom'})



		with _state_machine:
			# x:116 y:102
			OperatableStateMachine.add('EnterArena',
										_sm_enterarena_14,
										transitions={'done': 'GoToRoom', 'failed': 'failed'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'roomQuestion': 'roomQuestion', 'cleanupRoom': 'cleanupRoom'})

			# x:286 y:217
			OperatableStateMachine.add('GoToRoom',
										_sm_gotoroom_13,
										transitions={'done': 'CheckForMisplacedObjects', 'failed': 'failed'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'cleanupRoom': 'cleanupRoom'})

			# x:774 y:163
			OperatableStateMachine.add('sayDone',
										_sm_saydone_12,
										transitions={'done': 'done', 'failed': 'done'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:512 y:221
			OperatableStateMachine.add('CheckForMisplacedObjects',
										_sm_checkformisplacedobjects_11,
										transitions={'noneLeft': 'sayDone', 'found': 'PickMisplacedObject'},
										autonomy={'noneLeft': Autonomy.Inherit, 'found': Autonomy.Inherit},
										remapping={'nameFilter': 'nameFilter', 'misplacedObject': 'misplacedObject'})

			# x:509 y:379
			OperatableStateMachine.add('PickMisplacedObject',
										_sm_pickmisplacedobject_10,
										transitions={'finished': 'PutObjectInDesiredContainer', 'failed': 'GoToRoom'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'misplacedObject': 'misplacedObject', 'waypointGenerationDistance': 'waypointGenerationDistance'})

			# x:234 y:476
			OperatableStateMachine.add('PutObjectInDesiredContainer',
										_sm_putobjectindesiredcontainer_9,
										transitions={'finished': 'GoToRoom'},
										autonomy={'finished': Autonomy.Inherit},
										remapping={'misplacedObject': 'misplacedObject', 'placeholder': 'placeholder'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
