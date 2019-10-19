#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_behaviors.action_ask_sm import Action_AskSM as sara_flexbe_behaviors__Action_AskSM
from sara_flexbe_states.sara_nlu_getRoom import SaraNLUgetRoom
from sara_flexbe_behaviors.action_pass_door_sm import Action_Pass_DoorSM as sara_flexbe_behaviors__Action_Pass_DoorSM
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_behaviors.action_move_sm import Action_MoveSM as sara_flexbe_behaviors__Action_MoveSM
from sara_flexbe_states.sara_nlu_getObject import SaraNLUgetObject
from sara_flexbe_states.WonderlandGetEntityVerbal import WonderlandGetEntityVerbal
from sara_flexbe_states.WonderlandGetEntityByID import WonderlandGetEntityByID
from sara_flexbe_behaviors.wonderlandgetroom_sm import WonderlandGetRoomSM as sara_flexbe_behaviors__WonderlandGetRoomSM
from flexbe_states.flexible_check_condition_state import FlexibleCheckConditionState
from sara_flexbe_states.TourGuide import TourGuide
from flexbe_states.log_key_state import LogKeyState
from flexbe_states.flexible_calculation_state import FlexibleCalculationState
from flexbe_states.decision_state import DecisionState
from flexbe_states.wait_state import WaitState
from sara_flexbe_behaviors.leftorright_sm import leftOrRightSM as sara_flexbe_behaviors__leftOrRightSM
from sara_flexbe_behaviors.action_point_at_sm import Action_point_atSM as sara_flexbe_behaviors__Action_point_atSM
from flexbe_states.check_condition_state import CheckConditionState
from sara_flexbe_states.continue_button import ContinueButton
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Fri Jul 05 2019
@author: Mongrain
'''
class ScenarioWhereIsThisSM(Behavior):
	'''
	Where is this Scenario for Stage 2 2019
	'''


	def __init__(self):
		super(ScenarioWhereIsThisSM, self).__init__()
		self.name = 'ScenarioWhereIsThis'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(sara_flexbe_behaviors__Action_AskSM, 'InitialEntrance/Action_Ask')
		self.add_behavior(sara_flexbe_behaviors__Action_Pass_DoorSM, 'InitialEntrance/Action_Pass_Door')
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'GoToInformationPoint/Action_Move')
		self.add_behavior(sara_flexbe_behaviors__Action_AskSM, 'ListenForQuestion/Action_Ask')
		self.add_behavior(sara_flexbe_behaviors__WonderlandGetRoomSM, 'WhereIsItAndHowDoIDoThat/WonderlandGetRoom')
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'ExecuteTheSequence/Action_Move')
		self.add_behavior(sara_flexbe_behaviors__Action_Pass_DoorSM, 'ExecuteTheSequence/Action_Pass_Door')
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'ExecuteTheSequence/Action_Move_toFinalWaypoint')
		self.add_behavior(sara_flexbe_behaviors__leftOrRightSM, 'FinalPresentation/leftOrRight')
		self.add_behavior(sara_flexbe_behaviors__Action_point_atSM, 'FinalPresentation/Action_point_at')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:

		# O 234 32 /NaviguateToIt
		# SequenceList = Tableau sous forme|n[instruction,argument]

		# O 540 13 /InitialEntrance
		# Le Information Point est inconnu à l'avance

		# O 460 396 /WhereIsItAndHowDoIDoThat
		# TODO: Condition state

		# O 396 80 /GoToInformationPoint
		# Au besoin, ajouter une state pour faire matcher les nomes de waypoints selon les rooms

		# O 272 111 /FinalPresentation
		# TODO:|nAjouter State à aniane pour get un nearby entitity et construire une phrase avec



	def create(self):
		# x:65 y:417, x:387 y:222
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.entranceDoorName = "door_1_entry"
		_state_machine.userdata.infoPointWaypoint = ""
		_state_machine.userdata.containers = ""

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:30 y:365
		_sm_targetisnotacontainerresponse_0 = OperatableStateMachine(outcomes=['finished'], input_keys=['targetObjectName', 'roomEntity', 'containerEntity'], output_keys=['roomName', 'targetWaypoint'])

		with _sm_targetisnotacontainerresponse_0:
			# x:70 y:56
			OperatableStateMachine.add('GetRoomName',
										CalculationState(calculation=lambda x: x.name),
										transitions={'done': 'GetContName'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'roomEntity', 'output_value': 'roomName'})

			# x:208 y:55
			OperatableStateMachine.add('GetContName',
										CalculationState(calculation=lambda x: x.name),
										transitions={'done': 'TheRoomIsTheWaypoint'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'containerEntity', 'output_value': 'containerName'})

			# x:478 y:214
			OperatableStateMachine.add('ItIsInThatRoomInsideThatCont',
										SaraSay(sentence=lambda x: "The "+x[1]+" is in the " + x[2] +" inside the "+x[0]+".", input_keys=["roomName","targetObjectName","containerName"], emotion=0, block=True),
										transitions={'done': 'TheRoomIsTheWaypoint'},
										autonomy={'done': Autonomy.Off},
										remapping={'roomName': 'roomName', 'targetObjectName': 'targetObjectName', 'containerName': 'containerName'})

			# x:144 y:388
			OperatableStateMachine.add('TheRoomIsTheWaypoint',
										CalculationState(calculation=lambda x: x),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'roomName', 'output_value': 'targetWaypoint'})


		# x:101 y:456
		_sm_targetisacontainerresponse_1 = OperatableStateMachine(outcomes=['finished'], input_keys=['targetObjectName', 'roomEntity'], output_keys=['roomName', 'targetWaypoint'])

		with _sm_targetisacontainerresponse_1:
			# x:70 y:38
			OperatableStateMachine.add('GetRoomName',
										CalculationState(calculation=lambda x: x.name),
										transitions={'done': 'TheRoomIsTheWaypoint'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'roomEntity', 'output_value': 'roomName'})

			# x:147 y:157
			OperatableStateMachine.add('ItIsInThatRoom',
										SaraSay(sentence=lambda x: "The "+x[0]+" is in the " + x[1] +".", input_keys=["roomName","targetObjectName"], emotion=0, block=True),
										transitions={'done': 'TheRoomIsTheWaypoint'},
										autonomy={'done': Autonomy.Off},
										remapping={'roomName': 'roomName', 'targetObjectName': 'targetObjectName'})

			# x:415 y:43
			OperatableStateMachine.add('TheRoomIsTheWaypoint',
										CalculationState(calculation=lambda x: x),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'roomName', 'output_value': 'targetWaypoint'})


		# x:442 y:555, x:260 y:443
		_sm_finalpresentation_2 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['targetObjectName', 'wonderlandEntity'])

		with _sm_finalpresentation_2:
			# x:593 y:212
			OperatableStateMachine.add('leftOrRight',
										self.use_behavior(sara_flexbe_behaviors__leftOrRightSM, 'FinalPresentation/leftOrRight'),
										transitions={'finished': 'ItsHere', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'object': 'targetObjectName'})

			# x:74 y:261
			OperatableStateMachine.add('Action_point_at',
										self.use_behavior(sara_flexbe_behaviors__Action_point_atSM, 'FinalPresentation/Action_point_at'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'targetPoint': 'entityPosition'})

			# x:102 y:135
			OperatableStateMachine.add('GetEntitysPos',
										CalculationState(calculation=lambda x: x.position),
										transitions={'done': 'has pos'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'wonderlandEntity', 'output_value': 'entityPosition'})

			# x:280 y:204
			OperatableStateMachine.add('has pos',
										CheckConditionState(predicate=lambda x: x.x or x.y or x.z),
										transitions={'true': 'Action_point_at', 'false': 'failed'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'entityPosition'})

			# x:530 y:377
			OperatableStateMachine.add('ItsHere',
										SaraSay(sentence="I'm going back to the information point", input_keys=[], emotion=0, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		# x:82 y:631, x:847 y:479
		_sm_executethesequence_3 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['targetWaypoint', 'SequenceList'])

		with _sm_executethesequence_3:
			# x:30 y:39
			OperatableStateMachine.add('SetZeroIndex',
										SetKey(Value=0),
										transitions={'done': 'StillActionsToDo'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'index'})

			# x:952 y:148
			OperatableStateMachine.add('nextIndex',
										CalculationState(calculation=lambda x: x+1),
										transitions={'done': 'StillActionsToDo'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'index', 'output_value': 'index'})

			# x:218 y:122
			OperatableStateMachine.add('StillActionsToDo',
										FlexibleCheckConditionState(predicate=lambda x: x[0] < len(x[1]), input_keys=["index","SequenceList"]),
										transitions={'true': 'SetArg', 'false': 'Action_Move_toFinalWaypoint'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'index': 'index', 'SequenceList': 'SequenceList'})

			# x:478 y:227
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'ExecuteTheSequence/Action_Move'),
										transitions={'finished': 'nextIndex', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'arg'})

			# x:493 y:309
			OperatableStateMachine.add('SaySomething',
										SaraSay(sentence=lambda x: x[0], input_keys=["arg"], emotion=0, block=True),
										transitions={'done': 'nextIndex'},
										autonomy={'done': Autonomy.Off},
										remapping={'arg': 'arg'})

			# x:468 y:155
			OperatableStateMachine.add('Action_Pass_Door',
										self.use_behavior(sara_flexbe_behaviors__Action_Pass_DoorSM, 'ExecuteTheSequence/Action_Pass_Door'),
										transitions={'Done': 'nextIndex', 'Fail': 'failed'},
										autonomy={'Done': Autonomy.Inherit, 'Fail': Autonomy.Inherit},
										remapping={'DoorName': 'arg'})

			# x:197 y:235
			OperatableStateMachine.add('SetArg',
										FlexibleCalculationState(calculation=lambda x: x[1][x[0]][1], input_keys=["index","SequenceList"]),
										transitions={'done': 'SetActionName'},
										autonomy={'done': Autonomy.Off},
										remapping={'index': 'index', 'SequenceList': 'SequenceList', 'output_value': 'arg'})

			# x:189 y:340
			OperatableStateMachine.add('SetActionName',
										FlexibleCalculationState(calculation=lambda x: x[1][x[0]][0], input_keys=["index","SequenceList"]),
										transitions={'done': 'SelectAction'},
										autonomy={'done': Autonomy.Off},
										remapping={'index': 'index', 'SequenceList': 'SequenceList', 'output_value': 'actionName'})

			# x:342 y:351
			OperatableStateMachine.add('SelectAction',
										DecisionState(outcomes=["say","move","passdoor","wait"], conditions=lambda x: x),
										transitions={'say': 'SaySomething', 'move': 'Action_Move', 'passdoor': 'Action_Pass_Door', 'wait': 'Wait'},
										autonomy={'say': Autonomy.Off, 'move': Autonomy.Off, 'passdoor': Autonomy.Off, 'wait': Autonomy.Off},
										remapping={'input_value': 'actionName'})

			# x:106 y:486
			OperatableStateMachine.add('Action_Move_toFinalWaypoint',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'ExecuteTheSequence/Action_Move_toFinalWaypoint'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'targetWaypoint'})

			# x:494 y:373
			OperatableStateMachine.add('Wait',
										WaitState(wait_time=1.0),
										transitions={'done': 'nextIndex'},
										autonomy={'done': Autonomy.Off})


		# x:254 y:666, x:1054 y:22
		_sm_whereisitandhowdoidothat_4 = OperatableStateMachine(outcomes=['finished', 'oopsNoObject'], input_keys=['targetObjectName', 'containers', 'informationPointRoomName'], output_keys=['targetWaypoint', 'SequenceList', 'wonderlandEntity'])

		with _sm_whereisitandhowdoidothat_4:
			# x:37 y:28
			OperatableStateMachine.add('ImThinking',
										SaraSay(sentence="Okay, give me a second to think about it", input_keys=[], emotion=1, block=True),
										transitions={'done': 'GetWonderlandEntity'},
										autonomy={'done': Autonomy.Off})

			# x:815 y:154
			OperatableStateMachine.add('IFailed',
										SaraSay(sentence=lambda x: "I'm sorry, I don't know where you can find " + x[0] +".", input_keys=["targetObjectName"], emotion=1, block=True),
										transitions={'done': 'oopsNoObject'},
										autonomy={'done': Autonomy.Off},
										remapping={'targetObjectName': 'targetObjectName'})

			# x:393 y:82
			OperatableStateMachine.add('GetWonderlandId',
										CalculationState(calculation=lambda x: x.wonderlandId),
										transitions={'done': 'log id'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'wonderlandEntity', 'output_value': 'wonderlandEntityId'})

			# x:175 y:31
			OperatableStateMachine.add('GetWonderlandEntity',
										WonderlandGetEntityVerbal(),
										transitions={'one': 'GetWonderlandId', 'multiple': 'get first', 'none': 'IFailed', 'error': 'IFailed'},
										autonomy={'one': Autonomy.Off, 'multiple': Autonomy.Off, 'none': Autonomy.Off, 'error': Autonomy.Off},
										remapping={'name': 'targetObjectName', 'containers': 'containers', 'entities': 'entities', 'firstEntity': 'wonderlandEntity'})

			# x:46 y:318
			OperatableStateMachine.add('GetWonderlandContainerEntity',
										WonderlandGetEntityByID(),
										transitions={'found': 'CheckIfContainer', 'not_found': 'IFailed', 'error': 'IFailed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off, 'error': Autonomy.Off},
										remapping={'id': 'containerId', 'entity': 'containerEntity', 'depth_position': 'depth_position', 'depth_waypoint': 'depth_waypoint'})

			# x:157 y:126
			OperatableStateMachine.add('WonderlandGetRoom',
										self.use_behavior(sara_flexbe_behaviors__WonderlandGetRoomSM, 'WhereIsItAndHowDoIDoThat/WonderlandGetRoom'),
										transitions={'finished': 'GetWonderlandRoomEntity', 'failed': 'IFailed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'EntityId': 'wonderlandEntityId', 'ContainerId': 'RoomId'})

			# x:276 y:252
			OperatableStateMachine.add('GetContainerId',
										CalculationState(calculation=lambda x: x.containerId),
										transitions={'done': 'GetWonderlandContainerEntity'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'wonderlandEntity', 'output_value': 'containerId'})

			# x:18 y:215
			OperatableStateMachine.add('GetWonderlandRoomEntity',
										WonderlandGetEntityByID(),
										transitions={'found': 'GetContainerId', 'not_found': 'IFailed', 'error': 'IFailed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off, 'error': Autonomy.Off},
										remapping={'id': 'RoomId', 'entity': 'roomEntity', 'depth_position': 'depth_position', 'depth_waypoint': 'depth_waypoint'})

			# x:28 y:422
			OperatableStateMachine.add('TargetIsAContainerResponse',
										_sm_targetisacontainerresponse_1,
										transitions={'finished': 'GetSequenceToDo'},
										autonomy={'finished': Autonomy.Inherit},
										remapping={'targetObjectName': 'targetObjectName', 'roomEntity': 'roomEntity', 'roomName': 'roomName', 'targetWaypoint': 'targetWaypoint'})

			# x:361 y:458
			OperatableStateMachine.add('TargetIsNotAContainerResponse',
										_sm_targetisnotacontainerresponse_0,
										transitions={'finished': 'GetSequenceToDo'},
										autonomy={'finished': Autonomy.Inherit},
										remapping={'targetObjectName': 'targetObjectName', 'roomEntity': 'roomEntity', 'containerEntity': 'containerEntity', 'roomName': 'roomName', 'targetWaypoint': 'targetWaypoint'})

			# x:256 y:376
			OperatableStateMachine.add('CheckIfContainer',
										FlexibleCheckConditionState(predicate=lambda x: x[0] == x[1], input_keys=["containerId","RoomId"]),
										transitions={'true': 'TargetIsAContainerResponse', 'false': 'TargetIsNotAContainerResponse'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'containerId': 'containerId', 'RoomId': 'RoomId'})

			# x:172 y:542
			OperatableStateMachine.add('GetSequenceToDo',
										TourGuide(),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'object': 'targetObjectName', 'startingRoom': 'informationPointRoomName', 'endingRoom': 'roomName', 'sequence': 'SequenceList'})

			# x:536 y:16
			OperatableStateMachine.add('get first',
										CalculationState(calculation=lambda x: x[0]),
										transitions={'done': 'GetWonderlandId'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'wonderlandEntity', 'output_value': 'wonderlandEntity'})

			# x:681 y:47
			OperatableStateMachine.add('log id',
										LogKeyState(text="{}", severity=Logger.REPORT_HINT),
										transitions={'done': 'WonderlandGetRoom'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'wonderlandEntityId'})


		# x:97 y:633, x:567 y:94
		_sm_listenforquestion_5 = OperatableStateMachine(outcomes=['finished', 'failed'], output_keys=['targetObjectName'])

		with _sm_listenforquestion_5:
			# x:70 y:37
			OperatableStateMachine.add('SetTheQuestion',
										SetKey(Value="I'm ready for your question."),
										transitions={'done': 'Action_Ask'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'question'})

			# x:252 y:331
			OperatableStateMachine.add('OopsIMisunderstood',
										SaraSay(sentence="I misunderstood, Sorry.", input_keys=[], emotion=3, block=True),
										transitions={'done': 'Action_Ask'},
										autonomy={'done': Autonomy.Off})

			# x:53 y:150
			OperatableStateMachine.add('Action_Ask',
										self.use_behavior(sara_flexbe_behaviors__Action_AskSM, 'ListenForQuestion/Action_Ask'),
										transitions={'finished': 'NLU', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'question': 'question', 'answer': 'answer'})

			# x:55 y:418
			OperatableStateMachine.add('NLU',
										SaraNLUgetObject(),
										transitions={'understood': 'finished', 'not_understood': 'OopsIMisunderstood', 'fail': 'OopsIMisunderstood'},
										autonomy={'understood': Autonomy.Off, 'not_understood': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'sentence': 'answer', 'answer': 'targetObjectName'})


		# x:152 y:486, x:368 y:492
		_sm_gotoinformationpoint_6 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['infoPointWaypoint', 'informationPointRoomName'])

		with _sm_gotoinformationpoint_6:
			# x:30 y:40
			OperatableStateMachine.add('ThisIsTheInfoPoint',
										CalculationState(calculation=lambda x: x),
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'informationPointRoomName', 'output_value': 'infoPointWaypoint'})

			# x:144 y:264
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'GoToInformationPoint/Action_Move'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'infoPointWaypoint'})


		# x:454 y:593, x:639 y:210
		_sm_initialentrance_7 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['entranceDoorName'], output_keys=['informationPointRoomName'])

		with _sm_initialentrance_7:
			# x:41 y:35
			OperatableStateMachine.add('ImReady',
										SaraSay(sentence="I'm ready for this challenge !", input_keys=[], emotion=3, block=True),
										transitions={'done': 'Action_Pass_Door'},
										autonomy={'done': Autonomy.Off})

			# x:69 y:213
			OperatableStateMachine.add('SetTheQuestion',
										SetKey(Value="Where do you want me to go?"),
										transitions={'done': 'Action_Ask'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'question'})

			# x:359 y:361
			OperatableStateMachine.add('OopsIMisunderstood',
										SaraSay(sentence="I misunderstood, Sorry.", input_keys=[], emotion=3, block=True),
										transitions={'done': 'Action_Ask'},
										autonomy={'done': Autonomy.Off})

			# x:216 y:246
			OperatableStateMachine.add('Action_Ask',
										self.use_behavior(sara_flexbe_behaviors__Action_AskSM, 'InitialEntrance/Action_Ask'),
										transitions={'finished': 'NLUGetRoom', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'question': 'question', 'answer': 'answer'})

			# x:136 y:384
			OperatableStateMachine.add('NLUGetRoom',
										SaraNLUgetRoom(),
										transitions={'understood': 'finished', 'not_understood': 'OopsIMisunderstood', 'fail': 'OopsIMisunderstood'},
										autonomy={'understood': Autonomy.Off, 'not_understood': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'sentence': 'answer', 'answer': 'informationPointRoomName'})

			# x:244 y:53
			OperatableStateMachine.add('Action_Pass_Door',
										self.use_behavior(sara_flexbe_behaviors__Action_Pass_DoorSM, 'InitialEntrance/Action_Pass_Door'),
										transitions={'Done': 'SetTheQuestion', 'Fail': 'failed'},
										autonomy={'Done': Autonomy.Inherit, 'Fail': Autonomy.Inherit},
										remapping={'DoorName': 'entranceDoorName'})



		with _state_machine:
			# x:5 y:55
			OperatableStateMachine.add('continue',
										ContinueButton(),
										transitions={'true': 'InitialEntrance', 'false': 'InitialEntrance'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off})

			# x:372 y:37
			OperatableStateMachine.add('GoToInformationPoint',
										_sm_gotoinformationpoint_6,
										transitions={'finished': 'ListenForQuestion', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'infoPointWaypoint': 'infoPointWaypoint', 'informationPointRoomName': 'informationPointRoomName'})

			# x:657 y:199
			OperatableStateMachine.add('ListenForQuestion',
										_sm_listenforquestion_5,
										transitions={'finished': 'WhereIsItAndHowDoIDoThat', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'targetObjectName': 'targetObjectName'})

			# x:379 y:379
			OperatableStateMachine.add('WhereIsItAndHowDoIDoThat',
										_sm_whereisitandhowdoidothat_4,
										transitions={'finished': 'ExecuteTheSequence', 'oopsNoObject': 'ListenForQuestion'},
										autonomy={'finished': Autonomy.Inherit, 'oopsNoObject': Autonomy.Inherit},
										remapping={'targetObjectName': 'targetObjectName', 'containers': 'containers', 'informationPointRoomName': 'informationPointRoomName', 'targetWaypoint': 'targetWaypoint', 'SequenceList': 'SequenceList', 'wonderlandEntity': 'wonderlandEntity'})

			# x:61 y:304
			OperatableStateMachine.add('ExecuteTheSequence',
										_sm_executethesequence_3,
										transitions={'finished': 'FinalPresentation', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'targetWaypoint': 'targetWaypoint', 'SequenceList': 'SequenceList'})

			# x:139 y:161
			OperatableStateMachine.add('FinalPresentation',
										_sm_finalpresentation_2,
										transitions={'finished': 'GoToInformationPoint', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'targetObjectName': 'targetObjectName', 'wonderlandEntity': 'wonderlandEntity'})

			# x:126 y:32
			OperatableStateMachine.add('InitialEntrance',
										_sm_initialentrance_7,
										transitions={'finished': 'GoToInformationPoint', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'entranceDoorName': 'entranceDoorName', 'informationPointRoomName': 'informationPointRoomName'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
