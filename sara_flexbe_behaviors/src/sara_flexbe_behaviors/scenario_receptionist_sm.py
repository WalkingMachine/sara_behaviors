#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_behaviors.action_move_sm import Action_MoveSM as sara_flexbe_behaviors__Action_MoveSM
from sara_flexbe_states.for_loop import ForLoop
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.door_detector import DoorDetector
from sara_flexbe_behaviors.action_findperson_sm import Action_findPersonSM as sara_flexbe_behaviors__Action_findPersonSM
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_states.sara_nlu_receptionist import SaraNLUreceptionist
from sara_flexbe_behaviors.action_ask_sm import Action_AskSM as sara_flexbe_behaviors__Action_AskSM
from flexbe_states.flexible_check_condition_state import FlexibleCheckConditionState
from flexbe_states.calculation_state import CalculationState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sat Apr 27 2019
@author: Quentin Gaillot
'''
class Scenario_ReceptionistSM(Behavior):
	'''
	Scenario receptionist 2019 (Party Host)
	'''


	def __init__(self):
		super(Scenario_ReceptionistSM, self).__init__()
		self.name = 'Scenario_Receptionist'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'welcome Guest1/Action_Move')
		self.add_behavior(sara_flexbe_behaviors__Action_findPersonSM, 'welcome Guest1/Action_findPerson')
		self.add_behavior(sara_flexbe_behaviors__Action_AskSM, 'welcome Guest1/Action_Ask')
		self.add_behavior(sara_flexbe_behaviors__Action_AskSM, 'welcome Guest1/Action_Ask_2')
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'Guide G1 and introduice people/Action_Move')
		self.add_behavior(sara_flexbe_behaviors__Action_findPersonSM, 'Guide G1 and introduice people/Action_findPerson')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:

		# ! 60 458 /Guide G1 and introduice people
		# Faire une state ou behavior qui retourne une place ou s'assoir



	def create(self):
		# x:870 y:688, x:860 y:224
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.personAlreadyInLocation = "living room"
		_state_machine.userdata.personAlreadyInName = "John"
		_state_machine.userdata.personAlreadyInDrink = "coke"
		_state_machine.userdata.entranceLocation = "front door"

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:1159 y:605, x:1149 y:31
		_sm_guide_g1_and_introduice_people_0 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['personAlreadyInLocation', 'personAlreadyInName', 'personAlreadyInDrink', 'Guest1Drink', 'Guest1Name', 'Guest1Entity'], output_keys=['personAlreadyInEntity'])

		with _sm_guide_g1_and_introduice_people_0:
			# x:65 y:25
			OperatableStateMachine.add('say follow me to the right place',
										SaraSay(sentence=lambda x: "Please follow me to the x[0].", input_keys=["personAlreadyInLocation"], emotion=0, block=True),
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Off},
										remapping={'personAlreadyInLocation': 'personAlreadyInLocation'})

			# x:68 y:85
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'Guide G1 and introduice people/Action_Move'),
										transitions={'finished': 'Action_findPerson', 'failed': 'retry guide to location'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'personAlreadyInLocation'})

			# x:409 y:25
			OperatableStateMachine.add('retry guide to location',
										ForLoop(repeat=2),
										transitions={'do': 'Action_Move', 'end': 'say cannot reach destination'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index'})

			# x:585 y:26
			OperatableStateMachine.add('say cannot reach destination',
										SaraSay(sentence="I cannot reach the destination.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'set personAlreadyInEntity to unknown'},
										autonomy={'done': Autonomy.Off})

			# x:68 y:158
			OperatableStateMachine.add('Action_findPerson',
										self.use_behavior(sara_flexbe_behaviors__Action_findPersonSM, 'Guide G1 and introduice people/Action_findPerson', default_keys=['className']),
										transitions={'done': 'check if found entity is not the same as guest1 entity', 'pas_done': 'retry find person'},
										autonomy={'done': Autonomy.Inherit, 'pas_done': Autonomy.Inherit},
										remapping={'className': 'className', 'entity': 'foundEntity'})

			# x:355 y:162
			OperatableStateMachine.add('retry find person',
										ForLoop(repeat=2),
										transitions={'do': 'Action_findPerson', 'end': 'say cannot find personAlreadyIn'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index3'})

			# x:527 y:154
			OperatableStateMachine.add('say cannot find personAlreadyIn',
										SaraSay(sentence=lambda x: "I can not find"+x[0]+" but I will continue the scenario.", input_keys=["personAlreadyInName"], emotion=0, block=True),
										transitions={'done': 'set personAlreadyInEntity to unknown and continue'},
										autonomy={'done': Autonomy.Off},
										remapping={'personAlreadyInName': 'personAlreadyInName'})

			# x:33 y:241
			OperatableStateMachine.add('check if found entity is not the same as guest1 entity',
										FlexibleCheckConditionState(predicate=lambda x: x[0].ID == x[1].ID, input_keys=["foundEntity", "Guest1Entity"]),
										transitions={'true': 'retry find person', 'false': 'transfert foundEntity in personAlreadyInEntity'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'foundEntity': 'foundEntity', 'Guest1Entity': 'Guest1Entity'})

			# x:782 y:21
			OperatableStateMachine.add('set personAlreadyInEntity to unknown',
										SetKey(Value="unknown"),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'personAlreadyInEntity'})

			# x:40 y:310
			OperatableStateMachine.add('transfert foundEntity in personAlreadyInEntity',
										CalculationState(calculation=lambda x: x),
										transitions={'done': 'introduice G1 to person already in'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'foundEntity', 'output_value': 'personAlreadyInEntity'})

			# x:50 y:376
			OperatableStateMachine.add('introduice G1 to person already in',
										SaraSay(sentence=lambda x: "Hello "+x[0]+", here is a new guest who is named "+x[2]+" and love to drink "+x[3]+". "+x[2]+", I would like to introduice you "+x[0]+" and his favorite drink is "+x[1]+".", input_keys=["personAlreadyInName", "personAlreadyInDrink","Guest1Name","Guest1Drink"], emotion=0, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'personAlreadyInName': 'personAlreadyInName', 'personAlreadyInDrink': 'personAlreadyInDrink', 'Guest1Name': 'Guest1Name', 'Guest1Drink': 'Guest1Drink'})

			# x:505 y:237
			OperatableStateMachine.add('set personAlreadyInEntity to unknown and continue',
										SetKey(Value="unknown"),
										transitions={'done': 'introduice G1 to person already in'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'personAlreadyInEntity'})


		# x:30 y:458, x:130 y:458
		_sm_welcome_and_intruduce_guest2_1 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['Guest1Drink', 'personAlreadyInName', 'personAlreadyInDrink', 'personAlreadyInLocation', 'entranceLocation', 'Guest1Name', 'Guest1Entity'], output_keys=['Guest2Drink', 'Guest2Name'])

		with _sm_welcome_and_intruduce_guest2_1:
			# x:30 y:40
			OperatableStateMachine.add('say3',
										SaraSay(sentence="say", input_keys=[], emotion=0, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		# x:863 y:856, x:1249 y:152
		_sm_welcome_guest1_2 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['entranceLocation'], output_keys=['Guest1Drink', 'Guest1Name', 'Guest1Entity'])

		with _sm_welcome_guest1_2:
			# x:95 y:34
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'welcome Guest1/Action_Move'),
										transitions={'finished': 'say help to open the door', 'failed': 'retry moving'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'entranceLocation'})

			# x:294 y:35
			OperatableStateMachine.add('retry moving',
										ForLoop(repeat=2),
										transitions={'do': 'Action_Move', 'end': 'say cannot do task'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index'})

			# x:555 y:161
			OperatableStateMachine.add('say cannot do task',
										SaraSay(sentence="I failed to do my task.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'set G1 name to unknown'},
										autonomy={'done': Autonomy.Off})

			# x:109 y:212
			OperatableStateMachine.add('check if door is open',
										DoorDetector(timeout=12),
										transitions={'done': 'Action_findPerson', 'failed': 'retry opening door'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

			# x:100 y:131
			OperatableStateMachine.add('say help to open the door',
										SaraSay(sentence="Can someone help me and open this door?", input_keys=[], emotion=0, block=True),
										transitions={'done': 'check if door is open'},
										autonomy={'done': Autonomy.Off})

			# x:275 y:163
			OperatableStateMachine.add('retry opening door',
										ForLoop(repeat=1),
										transitions={'do': 'say help to open the door', 'end': 'say cannot do task'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index'})

			# x:104 y:294
			OperatableStateMachine.add('Action_findPerson',
										self.use_behavior(sara_flexbe_behaviors__Action_findPersonSM, 'welcome Guest1/Action_findPerson', default_keys=['className']),
										transitions={'done': 'introduice receptionist robot', 'pas_done': 'say cannot do task'},
										autonomy={'done': Autonomy.Inherit, 'pas_done': Autonomy.Inherit},
										remapping={'className': 'className', 'entity': 'Guest1Entity'})

			# x:699 y:156
			OperatableStateMachine.add('set G1 name to unknown',
										SetKey(Value="unknown"),
										transitions={'done': 'set G1 drink to unknown'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Guest1Name'})

			# x:865 y:155
			OperatableStateMachine.add('set G1 drink to unknown',
										SetKey(Value="unknown"),
										transitions={'done': 'set G1 entity to unknown'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Guest1Drink'})

			# x:1040 y:156
			OperatableStateMachine.add('set G1 entity to unknown',
										SetKey(Value="unknown"),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Guest1Entity'})

			# x:113 y:374
			OperatableStateMachine.add('introduice receptionist robot',
										SaraSay(sentence="Hello, I am receptionist robot.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'set question name G1'},
										autonomy={'done': Autonomy.Off})

			# x:324 y:510
			OperatableStateMachine.add('say continue scenario',
										SaraSay(sentence="I will continue the scenario with your name as unknown.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'set name G1 to unknown'},
										autonomy={'done': Autonomy.Off})

			# x:99 y:594
			OperatableStateMachine.add('nlu receptionist for name G1',
										SaraNLUreceptionist(),
										transitions={'understood': 'set question drink G1', 'fail': 'say continue scenario'},
										autonomy={'understood': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'sentence': 'answerNameG1', 'answer': 'Guest1Name'})

			# x:103 y:503
			OperatableStateMachine.add('Action_Ask',
										self.use_behavior(sara_flexbe_behaviors__Action_AskSM, 'welcome Guest1/Action_Ask'),
										transitions={'finished': 'nlu receptionist for name G1', 'failed': 'say continue scenario'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'question': 'questionNameG1', 'answer': 'answerNameG1'})

			# x:110 y:439
			OperatableStateMachine.add('set question name G1',
										SetKey(Value="What is your name?"),
										transitions={'done': 'Action_Ask'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'questionNameG1'})

			# x:319 y:582
			OperatableStateMachine.add('set name G1 to unknown',
										SetKey(Value="unknown"),
										transitions={'done': 'set question drink G1'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Guest1Name'})

			# x:102 y:733
			OperatableStateMachine.add('Action_Ask_2',
										self.use_behavior(sara_flexbe_behaviors__Action_AskSM, 'welcome Guest1/Action_Ask_2'),
										transitions={'finished': 'nlu receptionist for drink G1', 'failed': 'say continue scenario after drinkG1 failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'question': 'questionDrinkG1', 'answer': 'answerDrinkG1'})

			# x:118 y:657
			OperatableStateMachine.add('set question drink G1',
										SetKey(Value="What is your favorite drink?"),
										transitions={'done': 'Action_Ask_2'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'questionDrinkG1'})

			# x:104 y:827
			OperatableStateMachine.add('nlu receptionist for drink G1',
										SaraNLUreceptionist(),
										transitions={'understood': 'finished', 'fail': 'say continue scenario after drinkG1 failed'},
										autonomy={'understood': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'sentence': 'answerDrinkG1', 'answer': 'Guest1Drink'})

			# x:325 y:706
			OperatableStateMachine.add('say continue scenario after drinkG1 failed',
										SaraSay(sentence="I will continue the scenario with your favorite drink as unknown.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'set drink G1 to unknown'},
										autonomy={'done': Autonomy.Off})

			# x:350 y:781
			OperatableStateMachine.add('set drink G1 to unknown',
										SetKey(Value="unknown"),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Guest1Drink'})



		with _state_machine:
			# x:171 y:33
			OperatableStateMachine.add('welcome Guest1',
										_sm_welcome_guest1_2,
										transitions={'finished': 'Guide G1 and introduice people', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'entranceLocation': 'entranceLocation', 'Guest1Drink': 'Guest1Drink', 'Guest1Name': 'Guest1Name', 'Guest1Entity': 'Guest1Entity'})

			# x:152 y:656
			OperatableStateMachine.add('Welcome and intruduce Guest2',
										_sm_welcome_and_intruduce_guest2_1,
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'Guest1Drink': 'Guest1Drink', 'personAlreadyInName': 'personAlreadyInName', 'personAlreadyInDrink': 'personAlreadyInDrink', 'personAlreadyInLocation': 'personAlreadyInLocation', 'entranceLocation': 'entranceLocation', 'Guest1Name': 'Guest1Name', 'Guest1Entity': 'Guest1Entity', 'Guest2Drink': 'Guest2Drink', 'Guest2Name': 'Guest2Name'})

			# x:227 y:165
			OperatableStateMachine.add('Guide G1 and introduice people',
										_sm_guide_g1_and_introduice_people_0,
										transitions={'finished': 'Welcome and intruduce Guest2', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'personAlreadyInLocation': 'personAlreadyInLocation', 'personAlreadyInName': 'personAlreadyInName', 'personAlreadyInDrink': 'personAlreadyInDrink', 'Guest1Drink': 'Guest1Drink', 'Guest1Name': 'Guest1Name', 'Guest1Entity': 'Guest1Entity', 'personAlreadyInEntity': 'personAlreadyInEntity'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
