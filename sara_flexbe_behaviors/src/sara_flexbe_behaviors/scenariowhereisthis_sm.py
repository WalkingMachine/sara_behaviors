#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_behaviors.action_pass_door_sm import Action_Pass_DoorSM as sara_flexbe_behaviors__Action_Pass_DoorSM
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_behaviors.action_move_sm import Action_MoveSM as sara_flexbe_behaviors__Action_MoveSM
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_behaviors.action_ask_sm import Action_AskSM as sara_flexbe_behaviors__Action_AskSM
from sara_flexbe_states.sara_nlu_getObject import SaraNLUgetObject
from flexbe_states.calculation_state import CalculationState
from flexbe_states.flexible_check_condition_state import FlexibleCheckConditionState
from flexbe_states.flexible_calculation_state import FlexibleCalculationState
from flexbe_states.decision_state import DecisionState
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
		self.add_behavior(sara_flexbe_behaviors__Action_Pass_DoorSM, 'InitialEntrance/Action_Pass_Door')
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'GoToInformationPoint/Action_Move')
		self.add_behavior(sara_flexbe_behaviors__Action_AskSM, 'ListenForQuestion/Action_Ask')
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'ExecuteTheSequence/Action_Move')
		self.add_behavior(sara_flexbe_behaviors__Action_Pass_DoorSM, 'ExecuteTheSequence/Action_Pass_Door')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:

		# O 234 32 /NaviguateToIt
		# SequenceList = Tableau sous forme|n[instruction,argument]



	def create(self):
		# x:65 y:417, x:387 y:222
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.entranceDoorName = ""
		_state_machine.userdata.infoPointWaypoint = ""

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:70 y:220, x:661 y:49
		_sm_executethesequence_0 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['targetWaypoint', 'SequenceList'])

		with _sm_executethesequence_0:
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
										transitions={'true': 'SetArg', 'false': 'finished'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'index': 'index', 'SequenceList': 'SequenceList'})

			# x:441 y:295
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'ExecuteTheSequence/Action_Move'),
										transitions={'finished': 'nextIndex', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'arg'})

			# x:512 y:412
			OperatableStateMachine.add('SaySomething',
										SaraSay(sentence=lambda x: x[0], input_keys=["arg"], emotion=0, block=True),
										transitions={'done': 'nextIndex'},
										autonomy={'done': Autonomy.Off},
										remapping={'arg': 'arg'})

			# x:404 y:200
			OperatableStateMachine.add('Action_Pass_Door',
										self.use_behavior(sara_flexbe_behaviors__Action_Pass_DoorSM, 'ExecuteTheSequence/Action_Pass_Door'),
										transitions={'Done': 'nextIndex', 'Fail': 'failed'},
										autonomy={'Done': Autonomy.Inherit, 'Fail': Autonomy.Inherit},
										remapping={'DoorName': 'arg'})

			# x:123 y:248
			OperatableStateMachine.add('SetArg',
										FlexibleCalculationState(calculation=lambda x: x[1][x[0]][1], input_keys=["index","SequenceList"]),
										transitions={'done': 'SetActionName'},
										autonomy={'done': Autonomy.Off},
										remapping={'index': 'index', 'SequenceList': 'SequenceList', 'output_value': 'arg'})

			# x:106 y:355
			OperatableStateMachine.add('SetActionName',
										FlexibleCalculationState(calculation=lambda x: x[1][x[0]][0], input_keys=["index","SequenceList"]),
										transitions={'done': 'SelectAction'},
										autonomy={'done': Autonomy.Off},
										remapping={'index': 'index', 'SequenceList': 'SequenceList', 'output_value': 'actionName'})

			# x:320 y:349
			OperatableStateMachine.add('SelectAction',
										DecisionState(outcomes=["ask","passdoor","move"], conditions=lambda x: x),
										transitions={'ask': 'SaySomething', 'passdoor': 'Action_Pass_Door', 'move': 'Action_Move'},
										autonomy={'ask': Autonomy.Off, 'passdoor': Autonomy.Off, 'move': Autonomy.Off},
										remapping={'input_value': 'actionName'})


		# x:40 y:496
		_sm_whereisitandhowdoidothat_1 = OperatableStateMachine(outcomes=['finished'], input_keys=['targetObjectName'], output_keys=['targetWaypoint', 'SequenceList', 'targetObjectName'])

		with _sm_whereisitandhowdoidothat_1:
			# x:103 y:37
			OperatableStateMachine.add('ImThinking',
										SaraSay(sentence="Okay, give me a second to think about it", input_keys=[], emotion=1, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		# x:45 y:515, x:567 y:94
		_sm_listenforquestion_2 = OperatableStateMachine(outcomes=['finished', 'failed'], output_keys=['targetObjectName'])

		with _sm_listenforquestion_2:
			# x:70 y:37
			OperatableStateMachine.add('SetTheQuestion',
										SetKey(Value="I'm ready for your question."),
										transitions={'done': 'Action_Ask'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'question'})

			# x:241 y:253
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

			# x:64 y:323
			OperatableStateMachine.add('NLU',
										SaraNLUgetObject(),
										transitions={'understood': 'finished', 'not_understood': 'OopsIMisunderstood', 'fail': 'OopsIMisunderstood'},
										autonomy={'understood': Autonomy.Off, 'not_understood': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'sentence': 'answer', 'answer': 'targetObjectName'})


		# x:30 y:365, x:381 y:353
		_sm_gotoinformationpoint_3 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['infoPointWaypoint'])

		with _sm_gotoinformationpoint_3:
			# x:146 y:209
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'GoToInformationPoint/Action_Move'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'infoPointWaypoint'})


		# x:30 y:365, x:324 y:321
		_sm_initialentrance_4 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['entranceDoorName'])

		with _sm_initialentrance_4:
			# x:70 y:151
			OperatableStateMachine.add('Action_Pass_Door',
										self.use_behavior(sara_flexbe_behaviors__Action_Pass_DoorSM, 'InitialEntrance/Action_Pass_Door'),
										transitions={'Done': 'ImMovingToIt', 'Fail': 'failed'},
										autonomy={'Done': Autonomy.Inherit, 'Fail': Autonomy.Inherit},
										remapping={'DoorName': 'entranceDoorName'})

			# x:67 y:273
			OperatableStateMachine.add('ImMovingToIt',
										SaraSay(sentence="I'm moving to the Information Point", input_keys=[], emotion=1, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})



		with _state_machine:
			# x:126 y:32
			OperatableStateMachine.add('InitialEntrance',
										_sm_initialentrance_4,
										transitions={'finished': 'GoToInformationPoint', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'entranceDoorName': 'entranceDoorName'})

			# x:372 y:37
			OperatableStateMachine.add('GoToInformationPoint',
										_sm_gotoinformationpoint_3,
										transitions={'finished': 'ListenForQuestion', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'infoPointWaypoint': 'infoPointWaypoint'})

			# x:657 y:199
			OperatableStateMachine.add('ListenForQuestion',
										_sm_listenforquestion_2,
										transitions={'finished': 'WhereIsItAndHowDoIDoThat', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'targetObjectName': 'targetObjectName'})

			# x:379 y:379
			OperatableStateMachine.add('WhereIsItAndHowDoIDoThat',
										_sm_whereisitandhowdoidothat_1,
										transitions={'finished': 'ExecuteTheSequence'},
										autonomy={'finished': Autonomy.Inherit},
										remapping={'targetObjectName': 'targetObjectName', 'targetWaypoint': 'targetWaypoint', 'SequenceList': 'SequenceList'})

			# x:66 y:252
			OperatableStateMachine.add('ExecuteTheSequence',
										_sm_executethesequence_0,
										transitions={'finished': 'GoToInformationPoint', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'targetWaypoint': 'targetWaypoint', 'SequenceList': 'SequenceList'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
