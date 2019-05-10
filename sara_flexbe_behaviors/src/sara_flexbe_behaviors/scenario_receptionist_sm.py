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
from sara_flexbe_states.GetAttribute import GetAttribute
from flexbe_states.flexible_check_condition_state import FlexibleCheckConditionState
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.GetEmptyChair import GetEmptyChair
from sara_flexbe_behaviors.action_point_at_sm import Action_point_atSM as sara_flexbe_behaviors__Action_point_atSM
from sara_flexbe_behaviors.action_findpersonbyid_sm import Action_findPersonByIDSM as sara_flexbe_behaviors__Action_findPersonByIDSM
from flexbe_states.check_condition_state import CheckConditionState
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
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'Welcome Guest2/Action_Move')
		self.add_behavior(sara_flexbe_behaviors__Action_findPersonSM, 'Welcome Guest2/Action_findPerson')
		self.add_behavior(sara_flexbe_behaviors__Action_AskSM, 'Welcome Guest2/Action_Ask')
		self.add_behavior(sara_flexbe_behaviors__Action_AskSM, 'Welcome Guest2/Action_Ask_2')
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'Guide G1 and introduice people/Action_Move')
		self.add_behavior(sara_flexbe_behaviors__Action_findPersonSM, 'Guide G1 and introduice people/Action_findPerson')
		self.add_behavior(sara_flexbe_behaviors__Action_point_atSM, 'Guide G1 and introduice people/Action_point_at')
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'Guide G2 and introduice people/Action_Move')
		self.add_behavior(sara_flexbe_behaviors__Action_findPersonByIDSM, 'Guide G2 and introduice people/Action_findPersonByID')
		self.add_behavior(sara_flexbe_behaviors__Action_findPersonByIDSM, 'Guide G2 and introduice people/Action_findPersonByID_2')
		self.add_behavior(sara_flexbe_behaviors__Action_point_atSM, 'Guide G2 and introduice people/Action_point_at')
		self.add_behavior(sara_flexbe_behaviors__Action_point_atSM, 'Guide G2 and introduice people/Action_point_at_2')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:847 y:612, x:844 y:143
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.personAlreadyInLocation = "living room"
		_state_machine.userdata.personAlreadyInName = "John"
		_state_machine.userdata.personAlreadyInDrink = "coke"
		_state_machine.userdata.entranceLocation = "door"

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:1141 y:693, x:1133 y:101
		_sm_guide_g2_and_introduice_people_0 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['personAlreadyInLocation', 'personAlreadyInName', 'personAlreadyInDrink', 'Guest1Drink', 'Guest1Name', 'Guest1ID', 'personAlreadyInID', 'Guest2Drink', 'Guest2Name'])

		with _sm_guide_g2_and_introduice_people_0:
			# x:65 y:25
			OperatableStateMachine.add('say follow me to the right place',
										SaraSay(sentence=lambda x: "Please follow me to the"+ x[0] +".", input_keys=["personAlreadyInLocation"], emotion=0, block=True),
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Off},
										remapping={'personAlreadyInLocation': 'personAlreadyInLocation'})

			# x:68 y:85
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'Guide G2 and introduice people/Action_Move'),
										transitions={'finished': 'introduce new guest G2', 'failed': 'retry guide to location'},
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

			# x:782 y:21
			OperatableStateMachine.add('set personAlreadyInEntity to unknown',
										SetKey(Value="unknown"),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'personAlreadyInEntity'})

			# x:66 y:214
			OperatableStateMachine.add('Action_findPersonByID',
										self.use_behavior(sara_flexbe_behaviors__Action_findPersonByIDSM, 'Guide G2 and introduice people/Action_findPersonByID', default_keys=['className']),
										transitions={'found': 'get position of guest1Entity', 'not_found': 'say not found G1 but say his name and drink'},
										autonomy={'found': Autonomy.Inherit, 'not_found': Autonomy.Inherit},
										remapping={'className': 'className', 'personID': 'Guest1ID', 'personEntity': 'Guest1Entity'})

			# x:346 y:221
			OperatableStateMachine.add('say not found G1 but say his name and drink',
										SaraSay(sentence=lambda x: "I can not find "+x[0]+" but his favorite drink is "+x[1]+".", input_keys=["Guest1Name", "Guest1Drink"], emotion=0, block=True),
										transitions={'done': 'check if person already in is known aka ID not 0'},
										autonomy={'done': Autonomy.Off},
										remapping={'Guest1Name': 'Guest1Name', 'Guest1Drink': 'Guest1Drink'})

			# x:86 y:426
			OperatableStateMachine.add('say G1 details',
										SaraSay(sentence=lambda x: "Here is "+x[0]+" and his favorite drink is "+x[1]+".", input_keys=["Guest1Name", "Guest1Drink"], emotion=0, block=True),
										transitions={'done': 'check if person already in is known aka ID not 0'},
										autonomy={'done': Autonomy.Off},
										remapping={'Guest1Name': 'Guest1Name', 'Guest1Drink': 'Guest1Drink'})

			# x:45 y:500
			OperatableStateMachine.add('check if person already in is known aka ID not 0',
										CheckConditionState(predicate=lambda x: x != 0),
										transitions={'true': 'Action_findPersonByID_2', 'false': 'say not/cannot found person already in but say name/drink'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'personAlreadyInID'})

			# x:363 y:574
			OperatableStateMachine.add('say not/cannot found person already in but say name/drink',
										SaraSay(sentence=lambda x: "I can not find "+x[0]+" but his favorite drink is "+x[1]+".", input_keys=["personAlreadyInName", "personAlreadyInDrink"], emotion=0, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'personAlreadyInName': 'personAlreadyInName', 'personAlreadyInDrink': 'personAlreadyInDrink'})

			# x:73 y:148
			OperatableStateMachine.add('introduce new guest G2',
										SaraSay(sentence=lambda x: "Here is a new guest. His name is "+x[0]+" and his favorite drink is "+x[1]+".", input_keys=["Guest2Name", "Guest2Drink"], emotion=0, block=True),
										transitions={'done': 'Action_findPersonByID'},
										autonomy={'done': Autonomy.Off},
										remapping={'Guest2Name': 'Guest2Name', 'Guest2Drink': 'Guest2Drink'})

			# x:66 y:566
			OperatableStateMachine.add('Action_findPersonByID_2',
										self.use_behavior(sara_flexbe_behaviors__Action_findPersonByIDSM, 'Guide G2 and introduice people/Action_findPersonByID_2', default_keys=['className']),
										transitions={'found': 'get person already in position', 'not_found': 'say not/cannot found person already in but say name/drink'},
										autonomy={'found': Autonomy.Inherit, 'not_found': Autonomy.Inherit},
										remapping={'className': 'className', 'personID': 'personAlreadyInID', 'personEntity': 'personAlreadyInEntity'})

			# x:64 y:798
			OperatableStateMachine.add('say details person already in',
										SaraSay(sentence=lambda x: "Here is "+x[0]+" and his favorite drink is "+x[1]+".", input_keys=["personAlreadyInName", "personAlreadyInDrink"], emotion=0, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'personAlreadyInName': 'personAlreadyInName', 'personAlreadyInDrink': 'personAlreadyInDrink'})

			# x:65 y:285
			OperatableStateMachine.add('get position of guest1Entity',
										GetAttribute(attributes=["position"]),
										transitions={'done': 'Action_point_at'},
										autonomy={'done': Autonomy.Off},
										remapping={'object': 'Guest1Entity', 'position': 'Guest1Position'})

			# x:73 y:346
			OperatableStateMachine.add('Action_point_at',
										self.use_behavior(sara_flexbe_behaviors__Action_point_atSM, 'Guide G2 and introduice people/Action_point_at'),
										transitions={'finished': 'say G1 details', 'failed': 'say cannot point guest1 for guest2'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'targetPoint': 'Guest1Position'})

			# x:388 y:360
			OperatableStateMachine.add('say cannot point guest1 for guest2',
										SaraSay(sentence=lambda x: "I can not point to "+x[0]+" but his favorite drink is "+x[1]+".", input_keys=["Guest1Name", "Guest1Drink"], emotion=0, block=True),
										transitions={'done': 'check if person already in is known aka ID not 0'},
										autonomy={'done': Autonomy.Off},
										remapping={'Guest1Name': 'Guest1Name', 'Guest1Drink': 'Guest1Drink'})

			# x:70 y:636
			OperatableStateMachine.add('get person already in position',
										GetAttribute(attributes=["position"]),
										transitions={'done': 'Action_point_at_2'},
										autonomy={'done': Autonomy.Off},
										remapping={'object': 'personAlreadyInEntity', 'position': 'personAlreadyInPosition'})

			# x:72 y:711
			OperatableStateMachine.add('Action_point_at_2',
										self.use_behavior(sara_flexbe_behaviors__Action_point_atSM, 'Guide G2 and introduice people/Action_point_at_2'),
										transitions={'finished': 'say details person already in', 'failed': 'say cannot point to personalreadyin for G2'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'targetPoint': 'personAlreadyInPosition'})

			# x:328 y:677
			OperatableStateMachine.add('say cannot point to personalreadyin for G2',
										SaraSay(sentence=lambda x: "I can not point to "+x[0]+" but his favorite drink is "+x[1]+".", input_keys=["personAlreadyInName","personAlreadyInDrink"], emotion=0, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'personAlreadyInName': 'personAlreadyInName', 'personAlreadyInDrink': 'personAlreadyInDrink'})


		# x:1125 y:673, x:1146 y:27
		_sm_guide_g1_and_introduice_people_1 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['personAlreadyInLocation', 'personAlreadyInName', 'personAlreadyInDrink', 'Guest1Drink', 'Guest1Name', 'Guest1ID'], output_keys=['personAlreadyInID'])

		with _sm_guide_g1_and_introduice_people_1:
			# x:65 y:25
			OperatableStateMachine.add('say follow me to the right place',
										SaraSay(sentence=lambda x: "Please follow me to the "+x[0]+".", input_keys=["personAlreadyInLocation"], emotion=0, block=True),
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
										transitions={'done': 'from entity to ID', 'pas_done': 'retry find person'},
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

			# x:28 y:297
			OperatableStateMachine.add('check if found entity is not the same as guest1 entity',
										FlexibleCheckConditionState(predicate=lambda x: x[0] == x[1], input_keys=["foundEntity", "Guest1Entity"]),
										transitions={'true': 'retry find person', 'false': 'transfert foundEntity in personAlreadyInEntity'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'foundEntity': 'foundID', 'Guest1Entity': 'Guest1ID'})

			# x:782 y:21
			OperatableStateMachine.add('set personAlreadyInEntity to unknown',
										SetKey(Value=0),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'personAlreadyInID'})

			# x:37 y:365
			OperatableStateMachine.add('transfert foundEntity in personAlreadyInEntity',
										CalculationState(calculation=lambda x: x),
										transitions={'done': 'introduice G1 to person already in'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'foundID', 'output_value': 'personAlreadyInID'})

			# x:54 y:430
			OperatableStateMachine.add('introduice G1 to person already in',
										SaraSay(sentence=lambda x: "Hello "+x[0]+". Here is a new guest. His name is "+x[2]+" and love to drink "+x[3]+". "+x[2]+", I would like to introduice you "+x[0]+" and his favorite drink is "+x[1]+".", input_keys=["personAlreadyInName", "personAlreadyInDrink","Guest1Name","Guest1Drink"], emotion=0, block=True),
										transitions={'done': 'find empty chair for G1'},
										autonomy={'done': Autonomy.Off},
										remapping={'personAlreadyInName': 'personAlreadyInName', 'personAlreadyInDrink': 'personAlreadyInDrink', 'Guest1Name': 'Guest1Name', 'Guest1Drink': 'Guest1Drink'})

			# x:505 y:237
			OperatableStateMachine.add('set personAlreadyInEntity to unknown and continue',
										SetKey(Value="unknown"),
										transitions={'done': 'introduice G1 to person already in'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'personAlreadyInID'})

			# x:67 y:498
			OperatableStateMachine.add('find empty chair for G1',
										GetEmptyChair(),
										transitions={'done': 'get the entity to point Point', 'nothing_found': 'say cannot find empty chair'},
										autonomy={'done': Autonomy.Off, 'nothing_found': Autonomy.Off},
										remapping={'output_entity': 'emptyChair'})

			# x:62 y:648
			OperatableStateMachine.add('Action_point_at',
										self.use_behavior(sara_flexbe_behaviors__Action_point_atSM, 'Guide G1 and introduice people/Action_point_at'),
										transitions={'finished': 'say sit there', 'failed': 'say cannot point'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'targetPoint': 'chairPoint'})

			# x:62 y:575
			OperatableStateMachine.add('get the entity to point Point',
										GetAttribute(attributes=["position"]),
										transitions={'done': 'Action_point_at'},
										autonomy={'done': Autonomy.Off},
										remapping={'object': 'emptyChair', 'position': 'chairPoint'})

			# x:290 y:499
			OperatableStateMachine.add('say cannot find empty chair',
										SaraSay(sentence=lambda x: "I can not find a place for you to sit. Please, "+x[0]+", choose the one you prefere.", input_keys=["Guest1Name"], emotion=0, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'Guest1Name': 'Guest1Name'})

			# x:80 y:721
			OperatableStateMachine.add('say sit there',
										SaraSay(sentence=lambda x: x[0]+", you can sit there.", input_keys=["Guest1Name"], emotion=0, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'Guest1Name': 'Guest1Name'})

			# x:338 y:624
			OperatableStateMachine.add('say cannot point',
										SaraSay(sentence=lambda x: x[0]+", there is a place to sit for you but I can not point it.", input_keys=["Guest1Name"], emotion=0, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'Guest1Name': 'Guest1Name'})

			# x:83 y:235
			OperatableStateMachine.add('from entity to ID',
										GetAttribute(attributes=["ID"]),
										transitions={'done': 'check if found entity is not the same as guest1 entity'},
										autonomy={'done': Autonomy.Off},
										remapping={'object': 'foundEntity', 'ID': 'foundID'})


		# x:1010 y:784, x:1204 y:163
		_sm_welcome_guest2_2 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['entranceLocation'], output_keys=['Guest2Drink', 'Guest2Name', 'Guest2ID'])

		with _sm_welcome_guest2_2:
			# x:95 y:34
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'Welcome Guest2/Action_Move'),
										transitions={'finished': 'say help to open the door G2', 'failed': 'retry moving G2'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'entranceLocation'})

			# x:294 y:35
			OperatableStateMachine.add('retry moving G2',
										ForLoop(repeat=2),
										transitions={'do': 'Action_Move', 'end': 'say cannot do task G2'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index'})

			# x:555 y:161
			OperatableStateMachine.add('say cannot do task G2',
										SaraSay(sentence="I failed to do my task.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'set G2 name to unknown'},
										autonomy={'done': Autonomy.Off})

			# x:109 y:212
			OperatableStateMachine.add('check if door is open G2',
										DoorDetector(timeout=12),
										transitions={'done': 'Action_findPerson', 'failed': 'retry opening door G2'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

			# x:100 y:131
			OperatableStateMachine.add('say help to open the door G2',
										SaraSay(sentence="Can someone help me and open this door?", input_keys=[], emotion=0, block=True),
										transitions={'done': 'check if door is open G2'},
										autonomy={'done': Autonomy.Off})

			# x:275 y:163
			OperatableStateMachine.add('retry opening door G2',
										ForLoop(repeat=1),
										transitions={'do': 'say help to open the door G2', 'end': 'say cannot do task G2'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index'})

			# x:106 y:272
			OperatableStateMachine.add('Action_findPerson',
										self.use_behavior(sara_flexbe_behaviors__Action_findPersonSM, 'Welcome Guest2/Action_findPerson', default_keys=['className']),
										transitions={'done': 'get the ID for G2', 'pas_done': 'say cannot do task G2'},
										autonomy={'done': Autonomy.Inherit, 'pas_done': Autonomy.Inherit},
										remapping={'className': 'className', 'entity': 'Guest2Entity'})

			# x:699 y:156
			OperatableStateMachine.add('set G2 name to unknown',
										SetKey(Value="unknown"),
										transitions={'done': 'set G2 drink to unknown'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Guest2Name'})

			# x:865 y:155
			OperatableStateMachine.add('set G2 drink to unknown',
										SetKey(Value="unknown"),
										transitions={'done': 'set G2 ID to 0'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Guest2Drink'})

			# x:1023 y:153
			OperatableStateMachine.add('set G2 ID to 0',
										SetKey(Value=0),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Guest2ID'})

			# x:90 y:398
			OperatableStateMachine.add('introduice receptionist robot G2',
										SaraSay(sentence="Hello, I am the receptionist robot.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'set question name G2'},
										autonomy={'done': Autonomy.Off})

			# x:324 y:510
			OperatableStateMachine.add('say continue scenario G2',
										SaraSay(sentence="I will continue the scenario with your name as unknown.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'set name G2 to unknown'},
										autonomy={'done': Autonomy.Off})

			# x:95 y:608
			OperatableStateMachine.add('nlu receptionist for name G2',
										SaraNLUreceptionist(),
										transitions={'understood': 'set question drink G2', 'fail': 'say continue scenario G2'},
										autonomy={'understood': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'sentence': 'answerNameG2', 'answer': 'Guest2Name'})

			# x:110 y:459
			OperatableStateMachine.add('set question name G2',
										SetKey(Value="What is your name?"),
										transitions={'done': 'Action_Ask'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'questionNameG2'})

			# x:319 y:582
			OperatableStateMachine.add('set name G2 to unknown',
										SetKey(Value="unknown"),
										transitions={'done': 'set question drink G2'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Guest2Name'})

			# x:107 y:674
			OperatableStateMachine.add('set question drink G2',
										SetKey(Value="What is your favorite drink?"),
										transitions={'done': 'Action_Ask_2'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'questionDrinkG2'})

			# x:97 y:829
			OperatableStateMachine.add('nlu receptionist for drink G2',
										SaraNLUreceptionist(),
										transitions={'understood': 'finished', 'fail': 'say continue scenario after drinkG2 failed'},
										autonomy={'understood': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'sentence': 'answerDrinkG2', 'answer': 'Guest2Drink'})

			# x:325 y:706
			OperatableStateMachine.add('say continue scenario after drinkG2 failed',
										SaraSay(sentence="I will continue the scenario with your favorite drink as unknown.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'set drink G2 to unknown'},
										autonomy={'done': Autonomy.Off})

			# x:350 y:781
			OperatableStateMachine.add('set drink G2 to unknown',
										SetKey(Value="unknown"),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Guest2Drink'})

			# x:101 y:534
			OperatableStateMachine.add('Action_Ask',
										self.use_behavior(sara_flexbe_behaviors__Action_AskSM, 'Welcome Guest2/Action_Ask'),
										transitions={'finished': 'nlu receptionist for name G2', 'failed': 'say continue scenario G2'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'question': 'questionNameG2', 'answer': 'answerNameG2'})

			# x:97 y:743
			OperatableStateMachine.add('Action_Ask_2',
										self.use_behavior(sara_flexbe_behaviors__Action_AskSM, 'Welcome Guest2/Action_Ask_2'),
										transitions={'finished': 'nlu receptionist for drink G2', 'failed': 'say continue scenario after drinkG2 failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'question': 'questionDrinkG2', 'answer': 'answerDrinkG2'})

			# x:124 y:336
			OperatableStateMachine.add('get the ID for G2',
										GetAttribute(attributes=["ID"]),
										transitions={'done': 'introduice receptionist robot G2'},
										autonomy={'done': Autonomy.Off},
										remapping={'object': 'Guest2Entity', 'ID': 'Guest2ID'})


		# x:863 y:856, x:1249 y:152
		_sm_welcome_guest1_3 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['entranceLocation'], output_keys=['Guest1Drink', 'Guest1Name', 'Guest1ID'])

		with _sm_welcome_guest1_3:
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

			# x:106 y:277
			OperatableStateMachine.add('Action_findPerson',
										self.use_behavior(sara_flexbe_behaviors__Action_findPersonSM, 'welcome Guest1/Action_findPerson', default_keys=['className']),
										transitions={'done': 'get Guest1 ID', 'pas_done': 'say cannot do task'},
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
										transitions={'done': 'set G1 ID to 0'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Guest1Drink'})

			# x:1040 y:156
			OperatableStateMachine.add('set G1 ID to 0',
										SetKey(Value=0),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Guest1ID'})

			# x:106 y:401
			OperatableStateMachine.add('introduice receptionist robot',
										SaraSay(sentence="Hello, I am the receptionist robot.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'set question name G1'},
										autonomy={'done': Autonomy.Off})

			# x:331 y:563
			OperatableStateMachine.add('say continue scenario',
										SaraSay(sentence="I will continue the scenario with your name as unknown.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'set name G1 to unknown'},
										autonomy={'done': Autonomy.Off})

			# x:104 y:619
			OperatableStateMachine.add('nlu receptionist for name G1',
										SaraNLUreceptionist(),
										transitions={'understood': 'set question drink G1', 'fail': 'say continue scenario'},
										autonomy={'understood': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'sentence': 'answerNameG1', 'answer': 'Guest1Name'})

			# x:120 y:538
			OperatableStateMachine.add('Action_Ask',
										self.use_behavior(sara_flexbe_behaviors__Action_AskSM, 'welcome Guest1/Action_Ask'),
										transitions={'finished': 'nlu receptionist for name G1', 'failed': 'say continue scenario'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'question': 'questionNameG1', 'answer': 'answerNameG1'})

			# x:119 y:466
			OperatableStateMachine.add('set question name G1',
										SetKey(Value="What is your name?"),
										transitions={'done': 'Action_Ask'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'questionNameG1'})

			# x:322 y:630
			OperatableStateMachine.add('set name G1 to unknown',
										SetKey(Value="unknown"),
										transitions={'done': 'set question drink G1'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Guest1Name'})

			# x:109 y:756
			OperatableStateMachine.add('Action_Ask_2',
										self.use_behavior(sara_flexbe_behaviors__Action_AskSM, 'welcome Guest1/Action_Ask_2'),
										transitions={'finished': 'nlu receptionist for drink G1', 'failed': 'say continue scenario after drinkG1 failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'question': 'questionDrinkG1', 'answer': 'answerDrinkG1'})

			# x:121 y:685
			OperatableStateMachine.add('set question drink G1',
										SetKey(Value="What is your favorite drink?"),
										transitions={'done': 'Action_Ask_2'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'questionDrinkG1'})

			# x:103 y:836
			OperatableStateMachine.add('nlu receptionist for drink G1',
										SaraNLUreceptionist(),
										transitions={'understood': 'finished', 'fail': 'say continue scenario after drinkG1 failed'},
										autonomy={'understood': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'sentence': 'answerDrinkG1', 'answer': 'Guest1Drink'})

			# x:315 y:729
			OperatableStateMachine.add('say continue scenario after drinkG1 failed',
										SaraSay(sentence="I will continue the scenario with your favorite drink as unknown.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'set drink G1 to unknown'},
										autonomy={'done': Autonomy.Off})

			# x:355 y:799
			OperatableStateMachine.add('set drink G1 to unknown',
										SetKey(Value="unknown"),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Guest1Drink'})

			# x:126 y:342
			OperatableStateMachine.add('get Guest1 ID',
										GetAttribute(attributes=["ID"]),
										transitions={'done': 'introduice receptionist robot'},
										autonomy={'done': Autonomy.Off},
										remapping={'object': 'Guest1Entity', 'ID': 'Guest1ID'})



		with _state_machine:
			# x:162 y:21
			OperatableStateMachine.add('welcome Guest1',
										_sm_welcome_guest1_3,
										transitions={'finished': 'Guide G1 and introduice people', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'entranceLocation': 'entranceLocation', 'Guest1Drink': 'Guest1Drink', 'Guest1Name': 'Guest1Name', 'Guest1ID': 'Guest1ID'})

			# x:446 y:320
			OperatableStateMachine.add('Welcome Guest2',
										_sm_welcome_guest2_2,
										transitions={'finished': 'Guide G2 and introduice people', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'entranceLocation': 'entranceLocation', 'Guest2Drink': 'Guest2Drink', 'Guest2Name': 'Guest2Name', 'Guest2ID': 'Guest2ID'})

			# x:338 y:171
			OperatableStateMachine.add('Guide G1 and introduice people',
										_sm_guide_g1_and_introduice_people_1,
										transitions={'finished': 'Welcome Guest2', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'personAlreadyInLocation': 'personAlreadyInLocation', 'personAlreadyInName': 'personAlreadyInName', 'personAlreadyInDrink': 'personAlreadyInDrink', 'Guest1Drink': 'Guest1Drink', 'Guest1Name': 'Guest1Name', 'Guest1ID': 'Guest1ID', 'personAlreadyInID': 'personAlreadyInID'})

			# x:306 y:573
			OperatableStateMachine.add('Guide G2 and introduice people',
										_sm_guide_g2_and_introduice_people_0,
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'personAlreadyInLocation': 'personAlreadyInLocation', 'personAlreadyInName': 'personAlreadyInName', 'personAlreadyInDrink': 'personAlreadyInDrink', 'Guest1Drink': 'Guest1Drink', 'Guest1Name': 'Guest1Name', 'Guest1ID': 'Guest1ID', 'personAlreadyInID': 'personAlreadyInID', 'Guest2Drink': 'Guest2Drink', 'Guest2Name': 'Guest2Name'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
