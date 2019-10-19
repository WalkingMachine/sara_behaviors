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
from sara_flexbe_states.for_loop import ForLoop
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_behaviors.action_findperson_sm import Action_findPersonSM as sara_flexbe_behaviors__Action_findPersonSM
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_states.GetAttribute import GetAttribute
from sara_flexbe_states.sara_nlu_receptionist import SaraNLUreceptionist
from sara_flexbe_behaviors.action_ask_sm import Action_AskSM as sara_flexbe_behaviors__Action_AskSM
from sara_flexbe_states.KeepLookingAt import KeepLookingAt
from flexbe_states.calculation_state import CalculationState
from flexbe_states.wait_state import WaitState
from sara_flexbe_states.run_trajectory import RunTrajectory
from flexbe_states.flexible_check_condition_state import FlexibleCheckConditionState
from sara_flexbe_behaviors.action_point_at_sm import Action_point_atSM as sara_flexbe_behaviors__Action_point_atSM
from sara_flexbe_states.WonderlandGetEntityByID import WonderlandGetEntityByID
from sara_flexbe_behaviors.action_findpersonbyid_sm import Action_findPersonByIDSM as sara_flexbe_behaviors__Action_findPersonByIDSM
from flexbe_states.check_condition_state import CheckConditionState
from sara_flexbe_states.GetEmptyChair import GetEmptyChair
from sara_flexbe_states.FilterKey import FilterKey
from sara_flexbe_states.list_entities_by_name import list_entities_by_name
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
		self.add_behavior(sara_flexbe_behaviors__Init_SequenceSM, 'Init_Sequence')
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'Welcome Guest2/Action_Move')
		self.add_behavior(sara_flexbe_behaviors__Action_findPersonSM, 'Welcome Guest2/Action_findPerson')
		self.add_behavior(sara_flexbe_behaviors__Action_AskSM, 'Welcome Guest2/Ask name and drink while keep looking at person/Ask name and drink/Action_Ask')
		self.add_behavior(sara_flexbe_behaviors__Action_AskSM, 'Welcome Guest2/Ask name and drink while keep looking at person/Ask name and drink/Action_Ask_2')
		self.add_behavior(sara_flexbe_behaviors__Action_findPersonSM, 'Welcome Guest2/Action_findPerson_2')
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'Guide G1 and introduice people/move to the place/Action_Move')
		self.add_behavior(sara_flexbe_behaviors__Action_findPersonSM, 'Guide G1 and introduice people/Find person already in/Action_findPerson')
		self.add_behavior(sara_flexbe_behaviors__Action_point_atSM, 'Guide G1 and introduice people/point person already in/Action_point_at_2')
		self.add_behavior(sara_flexbe_behaviors__Action_point_atSM, 'Guide G1 and introduice people/find and point empty chair/Action_point_at')
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'Guide G2 and introduice people/navigate to the place/Action_Move')
		self.add_behavior(sara_flexbe_behaviors__Action_findPersonByIDSM, 'Guide G2 and introduice people/Action_findPersonByID')
		self.add_behavior(sara_flexbe_behaviors__Action_findPersonByIDSM, 'Guide G2 and introduice people/Action_findPersonByID_2')
		self.add_behavior(sara_flexbe_behaviors__Action_point_atSM, 'Guide G2 and introduice people/Point G1/Action_point_at')
		self.add_behavior(sara_flexbe_behaviors__Action_point_atSM, 'Guide G2 and introduice people/Point person already in/Action_point_at_2')
		self.add_behavior(sara_flexbe_behaviors__Action_point_atSM, 'Guide G2 and introduice people/find and point empty chair/Action_point_at')
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'welcome Guest1/Action_Move')
		self.add_behavior(sara_flexbe_behaviors__Action_AskSM, 'welcome Guest1/Ask name and drink while keep looking at person/Ask name and drink/Action_Ask')
		self.add_behavior(sara_flexbe_behaviors__Action_AskSM, 'welcome Guest1/Ask name and drink while keep looking at person/Ask name and drink/Action_Ask_2')
		self.add_behavior(sara_flexbe_behaviors__Action_findPersonSM, 'welcome Guest1/Action_findPerson')
		self.add_behavior(sara_flexbe_behaviors__Action_findPersonSM, 'welcome Guest1/Action_findPerson_2')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:847 y:612, x:844 y:143
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.personAlreadyInLocation = "livingRoom"
		_state_machine.userdata.personAlreadyInName = "John"
		_state_machine.userdata.personAlreadyInDrink = "coke"
		_state_machine.userdata.entranceLocation = "entrance"

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:30 y:458, x:130 y:458
		_sm_keep_looking_at_person_0 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['personID'])

		with _sm_keep_looking_at_person_0:
			# x:78 y:160
			OperatableStateMachine.add('keep looking at the person',
										KeepLookingAt(),
										transitions={'failed': 'keep looking at the person'},
										autonomy={'failed': Autonomy.Off},
										remapping={'ID': 'personID'})


		# x:262 y:691, x:823 y:297
		_sm_ask_name_and_drink_1 = OperatableStateMachine(outcomes=['finished', 'failed'], output_keys=['Guest1Name', 'Guest1Drink'])

		with _sm_ask_name_and_drink_1:
			# x:73 y:62
			OperatableStateMachine.add('introduice receptionist robot',
										SaraSay(sentence="Hello, I am the receptionist robot.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'set question name G1'},
										autonomy={'done': Autonomy.Off})

			# x:411 y:201
			OperatableStateMachine.add('say continue scenario',
										SaraSay(sentence="I will continue the scenario with your name as unknown.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'set name G1 to unknown'},
										autonomy={'done': Autonomy.Off})

			# x:62 y:274
			OperatableStateMachine.add('nlu receptionist for name G1',
										SaraNLUreceptionist(),
										transitions={'understood': 'set question drink G1', 'fail': 'say continue scenario'},
										autonomy={'understood': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'sentence': 'answerNameG1', 'answer': 'Guest1Name'})

			# x:80 y:192
			OperatableStateMachine.add('Action_Ask',
										self.use_behavior(sara_flexbe_behaviors__Action_AskSM, 'welcome Guest1/Ask name and drink while keep looking at person/Ask name and drink/Action_Ask'),
										transitions={'finished': 'nlu receptionist for name G1', 'failed': 'say continue scenario'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'question': 'questionNameG1', 'answer': 'answerNameG1'})

			# x:90 y:130
			OperatableStateMachine.add('set question name G1',
										SetKey(Value="What is your name?"),
										transitions={'done': 'Action_Ask'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'questionNameG1'})

			# x:397 y:285
			OperatableStateMachine.add('set name G1 to unknown',
										SetKey(Value="unknown"),
										transitions={'done': 'set question drink G1'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Guest1Name'})

			# x:68 y:427
			OperatableStateMachine.add('Action_Ask_2',
										self.use_behavior(sara_flexbe_behaviors__Action_AskSM, 'welcome Guest1/Ask name and drink while keep looking at person/Ask name and drink/Action_Ask_2'),
										transitions={'finished': 'nlu receptionist for drink G1', 'failed': 'say continue scenario after drinkG1 failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'question': 'questionDrinkG1', 'answer': 'answerDrinkG1'})

			# x:72 y:352
			OperatableStateMachine.add('set question drink G1',
										SetKey(Value="What is your favorite drink?"),
										transitions={'done': 'Action_Ask_2'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'questionDrinkG1'})

			# x:358 y:411
			OperatableStateMachine.add('say continue scenario after drinkG1 failed',
										SaraSay(sentence="I will continue the scenario with your favorite drink as unknown.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'set drink G1 to unknown'},
										autonomy={'done': Autonomy.Off})

			# x:410 y:497
			OperatableStateMachine.add('set drink G1 to unknown',
										SetKey(Value="unknown"),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Guest1Drink'})

			# x:59 y:509
			OperatableStateMachine.add('nlu receptionist for drink G1',
										SaraNLUreceptionist(),
										transitions={'understood': 'finished', 'fail': 'say continue scenario after drinkG1 failed'},
										autonomy={'understood': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'sentence': 'answerDrinkG1', 'answer': 'Guest1Drink'})


		# x:491 y:77, x:485 y:125, x:478 y:215, x:470 y:273, x:677 y:101, x:670 y:143
		_sm_ask_name_and_drink_while_keep_looking_at_person_2 = ConcurrencyContainer(outcomes=['finished', 'failed'], input_keys=['personID'], output_keys=['Guest1Name', 'Guest1Drink'], conditions=[
										('finished', [('Ask name and drink', 'finished')]),
										('finished', [('keep looking at person', 'finished')]),
										('failed', [('Ask name and drink', 'failed')]),
										('failed', [('keep looking at person', 'failed')])
										])

		with _sm_ask_name_and_drink_while_keep_looking_at_person_2:
			# x:87 y:23
			OperatableStateMachine.add('Ask name and drink',
										_sm_ask_name_and_drink_1,
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'Guest1Name': 'Guest1Name', 'Guest1Drink': 'Guest1Drink'})

			# x:91 y:220
			OperatableStateMachine.add('keep looking at person',
										_sm_keep_looking_at_person_0,
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'personID': 'personID'})


		# x:632 y:289
		_sm_replace_arm_2_3 = OperatableStateMachine(outcomes=['finished'], input_keys=['Guest2Name'])

		with _sm_replace_arm_2_3:
			# x:53 y:274
			OperatableStateMachine.add('position bras en repos si fail',
										RunTrajectory(file="repos", duration=0),
										transitions={'done': 'wait5'},
										autonomy={'done': Autonomy.Off})

			# x:271 y:277
			OperatableStateMachine.add('wait5',
										WaitState(wait_time=5),
										transitions={'done': 'say cannot point'},
										autonomy={'done': Autonomy.Off})

			# x:398 y:284
			OperatableStateMachine.add('say cannot point',
										SaraSay(sentence=lambda x: x[0]+", there is a place to sit for you but I can not point it.", input_keys=["Guest2Name"], emotion=0, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'Guest2Name': 'Guest2Name'})


		# x:653 y:93
		_sm_replace_arm_4 = OperatableStateMachine(outcomes=['done'], input_keys=['Guest2Name'])

		with _sm_replace_arm_4:
			# x:30 y:65
			OperatableStateMachine.add('position bras en repos si fail_2',
										RunTrajectory(file="repos", duration=0),
										transitions={'done': 'wait5_2'},
										autonomy={'done': Autonomy.Off})

			# x:247 y:62
			OperatableStateMachine.add('wait5_2',
										WaitState(wait_time=5),
										transitions={'done': 'say cannot find empty chair'},
										autonomy={'done': Autonomy.Off})

			# x:360 y:40
			OperatableStateMachine.add('say cannot find empty chair',
										SaraSay(sentence=lambda x: "I can not find a place for you to sit. Please, "+x[0]+", choose the one you prefere.", input_keys=["Guest2Name"], emotion=0, block=True),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off},
										remapping={'Guest2Name': 'Guest2Name'})


		# x:30 y:458, x:130 y:458, x:230 y:458
		_sm_find_and_point_empty_chair_5 = OperatableStateMachine(outcomes=['nothing_found', 'finished', 'failed'])

		with _sm_find_and_point_empty_chair_5:
			# x:44 y:40
			OperatableStateMachine.add('find empty chair for G1',
										GetEmptyChair(),
										transitions={'done': 'get the entity to point Point', 'nothing_found': 'nothing_found'},
										autonomy={'done': Autonomy.Off, 'nothing_found': Autonomy.Off},
										remapping={'output_entity': 'emptyChair'})

			# x:30 y:168
			OperatableStateMachine.add('Action_point_at',
										self.use_behavior(sara_flexbe_behaviors__Action_point_atSM, 'Guide G2 and introduice people/find and point empty chair/Action_point_at'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'targetPoint': 'chairPoint'})

			# x:36 y:107
			OperatableStateMachine.add('get the entity to point Point',
										GetAttribute(attributes=["position"]),
										transitions={'done': 'Action_point_at'},
										autonomy={'done': Autonomy.Off},
										remapping={'object': 'emptyChair', 'position': 'chairPoint'})


		# x:30 y:458, x:130 y:458
		_sm_point_person_already_in_6 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['personAlreadyInEntity'])

		with _sm_point_person_already_in_6:
			# x:30 y:40
			OperatableStateMachine.add('get person already in position',
										GetAttribute(attributes=["position"]),
										transitions={'done': 'Action_point_at_2'},
										autonomy={'done': Autonomy.Off},
										remapping={'object': 'personAlreadyInEntity', 'position': 'personAlreadyInPosition'})

			# x:39 y:102
			OperatableStateMachine.add('Action_point_at_2',
										self.use_behavior(sara_flexbe_behaviors__Action_point_atSM, 'Guide G2 and introduice people/Point person already in/Action_point_at_2'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'targetPoint': 'personAlreadyInPosition'})


		# x:30 y:458, x:130 y:458
		_sm_point_g1_7 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['Guest1Entity'])

		with _sm_point_g1_7:
			# x:30 y:40
			OperatableStateMachine.add('get position of guest1Entity',
										GetAttribute(attributes=["position"]),
										transitions={'done': 'Action_point_at'},
										autonomy={'done': Autonomy.Off},
										remapping={'object': 'Guest1Entity', 'position': 'Guest1Position'})

			# x:38 y:101
			OperatableStateMachine.add('Action_point_at',
										self.use_behavior(sara_flexbe_behaviors__Action_point_atSM, 'Guide G2 and introduice people/Point G1/Action_point_at'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'targetPoint': 'Guest1Position'})


		# x:30 y:458, x:130 y:458
		_sm_navigate_to_the_place_8 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['Guest2Name', 'personAlreadyInLocation'])

		with _sm_navigate_to_the_place_8:
			# x:40 y:40
			OperatableStateMachine.add('say follow me to the right place',
										SaraSay(sentence=lambda x: "Thank you, "+x[0]+". Please follow me to the"+ x[1] +".", input_keys=["Guest2Name","personAlreadyInLocation"], emotion=0, block=True),
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Off},
										remapping={'Guest2Name': 'Guest2Name', 'personAlreadyInLocation': 'personAlreadyInLocation'})

			# x:30 y:102
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'Guide G2 and introduice people/navigate to the place/Action_Move'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'personAlreadyInLocation'})


		# x:531 y:137
		_sm_replace_arm_2_9 = OperatableStateMachine(outcomes=['finished'], input_keys=['Guest1Name'])

		with _sm_replace_arm_2_9:
			# x:30 y:144
			OperatableStateMachine.add('position bras en repos si fail',
										RunTrajectory(file="repos", duration=0),
										transitions={'done': 'wait5'},
										autonomy={'done': Autonomy.Off})

			# x:230 y:133
			OperatableStateMachine.add('wait5',
										WaitState(wait_time=5),
										transitions={'done': 'say cannot point'},
										autonomy={'done': Autonomy.Off})

			# x:362 y:131
			OperatableStateMachine.add('say cannot point',
										SaraSay(sentence=lambda x: x[0]+", there is a place to sit for you but I can not point it.", input_keys=["Guest1Name"], emotion=0, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'Guest1Name': 'Guest1Name'})


		# x:580 y:102
		_sm_replace_arm_10 = OperatableStateMachine(outcomes=['done'], input_keys=['Guest1Name'])

		with _sm_replace_arm_10:
			# x:39 y:42
			OperatableStateMachine.add('position bras en repos si fail_2',
										RunTrajectory(file="repos", duration=0),
										transitions={'done': 'wait5_2'},
										autonomy={'done': Autonomy.Off})

			# x:229 y:41
			OperatableStateMachine.add('wait5_2',
										WaitState(wait_time=5),
										transitions={'done': 'say cannot find empty chair'},
										autonomy={'done': Autonomy.Off})

			# x:343 y:40
			OperatableStateMachine.add('say cannot find empty chair',
										SaraSay(sentence=lambda x: "I can not find a place for you to sit. Please, "+x[0]+", choose the one you prefere.", input_keys=["Guest1Name"], emotion=0, block=True),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off},
										remapping={'Guest1Name': 'Guest1Name'})


		# x:773 y:40, x:722 y:533, x:790 y:199
		_sm_find_and_point_empty_chair_11 = OperatableStateMachine(outcomes=['nothing_found', 'finished', 'failed'])

		with _sm_find_and_point_empty_chair_11:
			# x:87 y:40
			OperatableStateMachine.add('key couch',
										SetKey(Value=39),
										transitions={'done': 'get couch'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'couchID'})

			# x:92 y:514
			OperatableStateMachine.add('get the entity to point Point',
										GetAttribute(attributes=["position"]),
										transitions={'done': 'Action_point_at'},
										autonomy={'done': Autonomy.Off},
										remapping={'object': 'entity', 'position': 'chairPoint'})

			# x:101 y:124
			OperatableStateMachine.add('get couch',
										WonderlandGetEntityByID(),
										transitions={'found': 'get the entity to point Point', 'not_found': 'nothing_found', 'error': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off, 'error': Autonomy.Off},
										remapping={'id': 'couchID', 'entity': 'entity', 'depth_position': 'depth_position', 'depth_waypoint': 'depth_waypoint'})

			# x:101 y:605
			OperatableStateMachine.add('Action_point_at',
										self.use_behavior(sara_flexbe_behaviors__Action_point_atSM, 'Guide G1 and introduice people/find and point empty chair/Action_point_at'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'targetPoint': 'chairPoint'})


		# x:30 y:458, x:130 y:458
		_sm_point_person_already_in_12 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['foundEntity'])

		with _sm_point_person_already_in_12:
			# x:57 y:40
			OperatableStateMachine.add('get point of personAlreadyIn',
										GetAttribute(attributes=["position"]),
										transitions={'done': 'Action_point_at_2'},
										autonomy={'done': Autonomy.Off},
										remapping={'object': 'foundEntity', 'position': 'personAlreadyInPosition'})

			# x:30 y:99
			OperatableStateMachine.add('Action_point_at_2',
										self.use_behavior(sara_flexbe_behaviors__Action_point_atSM, 'Guide G1 and introduice people/point person already in/Action_point_at_2'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'targetPoint': 'personAlreadyInPosition'})


		# x:130 y:458, x:471 y:379
		_sm_find_person_already_in_13 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['Guest1ID'], output_keys=['foundEntity', 'personAlreadyInID'])

		with _sm_find_person_already_in_13:
			# x:70 y:40
			OperatableStateMachine.add('Action_findPerson',
										self.use_behavior(sara_flexbe_behaviors__Action_findPersonSM, 'Guide G1 and introduice people/Find person already in/Action_findPerson', default_keys=['className']),
										transitions={'done': 'from entity to ID', 'pas_done': 'retry find person'},
										autonomy={'done': Autonomy.Inherit, 'pas_done': Autonomy.Inherit},
										remapping={'className': 'className', 'entity': 'foundEntity'})

			# x:272 y:62
			OperatableStateMachine.add('retry find person',
										ForLoop(repeat=2),
										transitions={'do': 'Action_findPerson', 'end': 'failed'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index3'})

			# x:30 y:179
			OperatableStateMachine.add('check if found entity is not the same as guest1 entity',
										FlexibleCheckConditionState(predicate=lambda x: x[0] == x[1], input_keys=["foundEntity", "Guest1Entity"]),
										transitions={'true': 'retry find person', 'false': 'transfert foundEntity in personAlreadyInEntity'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'foundEntity': 'foundID', 'Guest1Entity': 'Guest1ID'})

			# x:39 y:247
			OperatableStateMachine.add('transfert foundEntity in personAlreadyInEntity',
										CalculationState(calculation=lambda x: x),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'foundID', 'output_value': 'personAlreadyInID'})

			# x:85 y:117
			OperatableStateMachine.add('from entity to ID',
										GetAttribute(attributes=["ID"]),
										transitions={'done': 'check if found entity is not the same as guest1 entity'},
										autonomy={'done': Autonomy.Off},
										remapping={'object': 'foundEntity', 'ID': 'foundID'})


		# x:30 y:458, x:130 y:458
		_sm_move_to_the_place_14 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['Guest1Name', 'personAlreadyInLocation'])

		with _sm_move_to_the_place_14:
			# x:37 y:40
			OperatableStateMachine.add('say follow me to the right place',
										SaraSay(sentence=lambda x: "Thank you, "+x[0]+". Please follow me to the "+x[1]+".", input_keys=["Guest1Name", "personAlreadyInLocation"], emotion=0, block=True),
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Off},
										remapping={'Guest1Name': 'Guest1Name', 'personAlreadyInLocation': 'personAlreadyInLocation'})

			# x:40 y:142
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'Guide G1 and introduice people/move to the place/Action_Move'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'personAlreadyInLocation'})


		# x:30 y:458, x:130 y:458
		_sm_keep_looking_at_person_15 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['personID'])

		with _sm_keep_looking_at_person_15:
			# x:78 y:160
			OperatableStateMachine.add('keep looking at the person',
										KeepLookingAt(),
										transitions={'failed': 'keep looking at the person'},
										autonomy={'failed': Autonomy.Off},
										remapping={'ID': 'personID'})


		# x:173 y:620, x:469 y:632
		_sm_ask_name_and_drink_16 = OperatableStateMachine(outcomes=['finished', 'failed'], output_keys=['Guest2Name', 'Guest2Drink'])

		with _sm_ask_name_and_drink_16:
			# x:73 y:62
			OperatableStateMachine.add('introduice receptionist robot',
										SaraSay(sentence="Hello, I am the receptionist robot.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'set question name G1'},
										autonomy={'done': Autonomy.Off})

			# x:411 y:201
			OperatableStateMachine.add('say continue scenario',
										SaraSay(sentence="I will continue the scenario with your name as unknown.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'set name G1 to unknown'},
										autonomy={'done': Autonomy.Off})

			# x:62 y:274
			OperatableStateMachine.add('nlu receptionist for name G1',
										SaraNLUreceptionist(),
										transitions={'understood': 'set question drink G1', 'fail': 'say continue scenario'},
										autonomy={'understood': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'sentence': 'answerNameG2', 'answer': 'Guest2Name'})

			# x:80 y:192
			OperatableStateMachine.add('Action_Ask',
										self.use_behavior(sara_flexbe_behaviors__Action_AskSM, 'Welcome Guest2/Ask name and drink while keep looking at person/Ask name and drink/Action_Ask'),
										transitions={'finished': 'nlu receptionist for name G1', 'failed': 'say continue scenario'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'question': 'questionNameG2', 'answer': 'answerNameG2'})

			# x:90 y:130
			OperatableStateMachine.add('set question name G1',
										SetKey(Value="What is your name?"),
										transitions={'done': 'Action_Ask'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'questionNameG2'})

			# x:397 y:285
			OperatableStateMachine.add('set name G1 to unknown',
										SetKey(Value="unknown"),
										transitions={'done': 'set question drink G1'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Guest2Name'})

			# x:68 y:427
			OperatableStateMachine.add('Action_Ask_2',
										self.use_behavior(sara_flexbe_behaviors__Action_AskSM, 'Welcome Guest2/Ask name and drink while keep looking at person/Ask name and drink/Action_Ask_2'),
										transitions={'finished': 'nlu receptionist for drink G1', 'failed': 'say continue scenario after drinkG1 failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'question': 'questionDrinkG2', 'answer': 'answerDrinkG2'})

			# x:72 y:352
			OperatableStateMachine.add('set question drink G1',
										SetKey(Value="What is your favorite drink?"),
										transitions={'done': 'Action_Ask_2'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'questionDrinkG2'})

			# x:358 y:411
			OperatableStateMachine.add('say continue scenario after drinkG1 failed',
										SaraSay(sentence="I will continue the scenario with your favorite drink as unknown.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'set drink G1 to unknown'},
										autonomy={'done': Autonomy.Off})

			# x:410 y:497
			OperatableStateMachine.add('set drink G1 to unknown',
										SetKey(Value="unknown"),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Guest2Drink'})

			# x:59 y:509
			OperatableStateMachine.add('nlu receptionist for drink G1',
										SaraNLUreceptionist(),
										transitions={'understood': 'finished', 'fail': 'say continue scenario after drinkG1 failed'},
										autonomy={'understood': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'sentence': 'answerDrinkG2', 'answer': 'Guest2Drink'})


		# x:30 y:458, x:130 y:458, x:230 y:458, x:330 y:458, x:430 y:458, x:530 y:458
		_sm_ask_name_and_drink_while_keep_looking_at_person_17 = ConcurrencyContainer(outcomes=['finished', 'failed'], input_keys=['personID'], output_keys=['Guest2Name', 'Guest2Drink'], conditions=[
										('finished', [('Ask name and drink', 'finished')]),
										('finished', [('keep looking at person', 'finished')]),
										('failed', [('Ask name and drink', 'failed')]),
										('failed', [('keep looking at person', 'failed')])
										])

		with _sm_ask_name_and_drink_while_keep_looking_at_person_17:
			# x:59 y:120
			OperatableStateMachine.add('Ask name and drink',
										_sm_ask_name_and_drink_16,
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'Guest2Name': 'Guest2Name', 'Guest2Drink': 'Guest2Drink'})

			# x:341 y:91
			OperatableStateMachine.add('keep looking at person',
										_sm_keep_looking_at_person_15,
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'personID': 'personID'})


		# x:863 y:856, x:1410 y:152
		_sm_welcome_guest1_18 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['entranceLocation'], output_keys=['Guest1Drink', 'Guest1Name', 'Guest1ID'])

		with _sm_welcome_guest1_18:
			# x:95 y:34
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'welcome Guest1/Action_Move'),
										transitions={'finished': 'wait 2', 'failed': 'retry moving'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'entranceLocation'})

			# x:294 y:35
			OperatableStateMachine.add('retry moving',
										ForLoop(repeat=2),
										transitions={'do': 'Action_Move', 'end': 'say cannot do task'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index'})

			# x:747 y:148
			OperatableStateMachine.add('say cannot do task',
										SaraSay(sentence="I failed to do my task.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'set G1 name to unknown'},
										autonomy={'done': Autonomy.Off})

			# x:885 y:145
			OperatableStateMachine.add('set G1 name to unknown',
										SetKey(Value="unknown"),
										transitions={'done': 'set G1 drink to unknown'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Guest1Name'})

			# x:1051 y:146
			OperatableStateMachine.add('set G1 drink to unknown',
										SetKey(Value="unknown"),
										transitions={'done': 'set G1 ID to 0'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Guest1Drink'})

			# x:1226 y:145
			OperatableStateMachine.add('set G1 ID to 0',
										SetKey(Value=0),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Guest1ID'})

			# x:33 y:473
			OperatableStateMachine.add('Ask name and drink while keep looking at person',
										_sm_ask_name_and_drink_while_keep_looking_at_person_2,
										transitions={'finished': 'Action_findPerson_2', 'failed': 'Ask name and drink while keep looking at person'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'personID': 'personID', 'Guest1Name': 'Guest1Name', 'Guest1Drink': 'Guest1Drink'})

			# x:69 y:261
			OperatableStateMachine.add('Action_findPerson',
										self.use_behavior(sara_flexbe_behaviors__Action_findPersonSM, 'welcome Guest1/Action_findPerson', default_keys=['className']),
										transitions={'done': 'get Guest1 ID', 'pas_done': 'say cannot do task'},
										autonomy={'done': Autonomy.Inherit, 'pas_done': Autonomy.Inherit},
										remapping={'className': 'className', 'entity': 'personEntity'})

			# x:84 y:385
			OperatableStateMachine.add('get Guest1 ID',
										GetAttribute(attributes=["ID"]),
										transitions={'done': 'Ask name and drink while keep looking at person'},
										autonomy={'done': Autonomy.Off},
										remapping={'object': 'personEntity', 'ID': 'personID'})

			# x:114 y:587
			OperatableStateMachine.add('Action_findPerson_2',
										self.use_behavior(sara_flexbe_behaviors__Action_findPersonSM, 'welcome Guest1/Action_findPerson_2', default_keys=['className']),
										transitions={'done': 'get Guest1 ID_2', 'pas_done': 'put previous ID in Guest1ID'},
										autonomy={'done': Autonomy.Inherit, 'pas_done': Autonomy.Inherit},
										remapping={'className': 'className', 'entity': 'Guest1Entity'})

			# x:135 y:777
			OperatableStateMachine.add('get Guest1 ID_2',
										GetAttribute(attributes=["ID"]),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'object': 'Guest1Entity', 'ID': 'Guest1ID'})

			# x:316 y:666
			OperatableStateMachine.add('put previous ID in Guest1ID',
										CalculationState(calculation=lambda x: x),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'personID', 'output_value': 'Guest1ID'})

			# x:96 y:138
			OperatableStateMachine.add('wait 2',
										WaitState(wait_time=2),
										transitions={'done': 'Action_findPerson'},
										autonomy={'done': Autonomy.Off})


		# x:1370 y:761, x:1133 y:101
		_sm_guide_g2_and_introduice_people_19 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['personAlreadyInLocation', 'personAlreadyInName', 'personAlreadyInDrink', 'Guest1Drink', 'Guest1Name', 'Guest1ID', 'personAlreadyInID', 'Guest2Drink', 'Guest2Name', 'Guest2ID'])

		with _sm_guide_g2_and_introduice_people_19:
			# x:56 y:32
			OperatableStateMachine.add('navigate to the place',
										_sm_navigate_to_the_place_8,
										transitions={'finished': 'introduce new guest G2', 'failed': 'retry guide to location'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'Guest2Name': 'Guest2Name', 'personAlreadyInLocation': 'personAlreadyInLocation'})

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

			# x:50 y:158
			OperatableStateMachine.add('Action_findPersonByID',
										self.use_behavior(sara_flexbe_behaviors__Action_findPersonByIDSM, 'Guide G2 and introduice people/Action_findPersonByID', default_keys=['className']),
										transitions={'found': 'Point G1', 'not_found': 'say not found G1 but say his name and drink'},
										autonomy={'found': Autonomy.Inherit, 'not_found': Autonomy.Inherit},
										remapping={'className': 'className', 'personID': 'Guest1ID', 'personEntity': 'Guest1Entity'})

			# x:327 y:186
			OperatableStateMachine.add('say not found G1 but say his name and drink',
										SaraSay(sentence=lambda x: "I can not find "+x[0]+" but his favorite drink is "+x[1]+".", input_keys=["Guest1Name", "Guest1Drink"], emotion=0, block=True),
										transitions={'done': 'replace arm before check personalreadyin'},
										autonomy={'done': Autonomy.Off},
										remapping={'Guest1Name': 'Guest1Name', 'Guest1Drink': 'Guest1Drink'})

			# x:68 y:296
			OperatableStateMachine.add('say G1 details',
										SaraSay(sentence=lambda x: "Here is "+x[0]+" and his favorite drink is "+x[1]+".", input_keys=["Guest1Name", "Guest1Drink"], emotion=0, block=True),
										transitions={'done': 'replace arm before check personalreadyin'},
										autonomy={'done': Autonomy.Off},
										remapping={'Guest1Name': 'Guest1Name', 'Guest1Drink': 'Guest1Drink'})

			# x:20 y:413
			OperatableStateMachine.add('check if person already in is known aka ID not 0',
										CheckConditionState(predicate=lambda x: x != 0),
										transitions={'true': 'Action_findPersonByID_2', 'false': 'set key for filter'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'personAlreadyInID'})

			# x:476 y:638
			OperatableStateMachine.add('say not/cannot found person already in but say name/drink',
										SaraSay(sentence=lambda x: "I can not find "+x[0]+" but his favorite drink is "+x[1]+".", input_keys=["personAlreadyInName", "personAlreadyInDrink"], emotion=0, block=True),
										transitions={'done': 'find and point empty chair'},
										autonomy={'done': Autonomy.Off},
										remapping={'personAlreadyInName': 'personAlreadyInName', 'personAlreadyInDrink': 'personAlreadyInDrink'})

			# x:57 y:97
			OperatableStateMachine.add('introduce new guest G2',
										SaraSay(sentence=lambda x: "Hey everyone. Here is a new guest. His name is "+x[0]+" and his favorite drink is "+x[1]+".", input_keys=["Guest2Name", "Guest2Drink"], emotion=0, block=True),
										transitions={'done': 'Action_findPersonByID'},
										autonomy={'done': Autonomy.Off},
										remapping={'Guest2Name': 'Guest2Name', 'Guest2Drink': 'Guest2Drink'})

			# x:56 y:476
			OperatableStateMachine.add('Action_findPersonByID_2',
										self.use_behavior(sara_flexbe_behaviors__Action_findPersonByIDSM, 'Guide G2 and introduice people/Action_findPersonByID_2', default_keys=['className']),
										transitions={'found': 'Point person already in', 'not_found': 'set key for filter'},
										autonomy={'found': Autonomy.Inherit, 'not_found': Autonomy.Inherit},
										remapping={'className': 'className', 'personID': 'personAlreadyInID', 'personEntity': 'personAlreadyInEntity'})

			# x:85 y:798
			OperatableStateMachine.add('say details person already in',
										SaraSay(sentence=lambda x: "Here is "+x[0]+". His is favorite drink is "+x[1]+".", input_keys=["personAlreadyInName", "personAlreadyInDrink"], emotion=0, block=True),
										transitions={'done': 'find and point empty chair'},
										autonomy={'done': Autonomy.Off},
										remapping={'personAlreadyInName': 'personAlreadyInName', 'personAlreadyInDrink': 'personAlreadyInDrink'})

			# x:388 y:360
			OperatableStateMachine.add('say cannot point guest1 for guest2',
										SaraSay(sentence=lambda x: "I can not point to "+x[0]+" but his favorite drink is "+x[1]+".", input_keys=["Guest1Name", "Guest1Drink"], emotion=0, block=True),
										transitions={'done': 'replace arm before check personalreadyin'},
										autonomy={'done': Autonomy.Off},
										remapping={'Guest1Name': 'Guest1Name', 'Guest1Drink': 'Guest1Drink'})

			# x:518 y:708
			OperatableStateMachine.add('say cannot point to personalreadyin for G2',
										SaraSay(sentence=lambda x: "I can not point to "+x[0]+" but his favorite drink is "+x[1]+".", input_keys=["personAlreadyInName","personAlreadyInDrink"], emotion=0, block=True),
										transitions={'done': 'find and point empty chair'},
										autonomy={'done': Autonomy.Off},
										remapping={'personAlreadyInName': 'personAlreadyInName', 'personAlreadyInDrink': 'personAlreadyInDrink'})

			# x:68 y:226
			OperatableStateMachine.add('Point G1',
										_sm_point_g1_7,
										transitions={'finished': 'say G1 details', 'failed': 'say cannot point guest1 for guest2'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'Guest1Entity': 'Guest1Entity'})

			# x:409 y:25
			OperatableStateMachine.add('retry guide to location',
										ForLoop(repeat=2),
										transitions={'do': 'navigate to the place', 'end': 'say cannot reach destination'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index'})

			# x:86 y:710
			OperatableStateMachine.add('Point person already in',
										_sm_point_person_already_in_6,
										transitions={'finished': 'say details person already in', 'failed': 'say cannot point to personalreadyin for G2'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'personAlreadyInEntity': 'personAlreadyInEntity'})

			# x:800 y:836
			OperatableStateMachine.add('say sit there',
										SaraSay(sentence=lambda x: x[0]+", you can sit there.", input_keys=["Guest1Name"], emotion=0, block=True),
										transitions={'done': 'position repos bras_2'},
										autonomy={'done': Autonomy.Off},
										remapping={'Guest1Name': 'Guest1Name'})

			# x:974 y:835
			OperatableStateMachine.add('position repos bras_2',
										RunTrajectory(file="repos", duration=0),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:544 y:812
			OperatableStateMachine.add('find and point empty chair',
										_sm_find_and_point_empty_chair_5,
										transitions={'nothing_found': 'replace arm', 'finished': 'say sit there', 'failed': 'replace arm 2'},
										autonomy={'nothing_found': Autonomy.Inherit, 'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:911 y:675
			OperatableStateMachine.add('replace arm',
										_sm_replace_arm_4,
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Inherit},
										remapping={'Guest2Name': 'Guest2Name'})

			# x:909 y:742
			OperatableStateMachine.add('replace arm 2',
										_sm_replace_arm_2_3,
										transitions={'finished': 'finished'},
										autonomy={'finished': Autonomy.Inherit},
										remapping={'Guest2Name': 'Guest2Name'})

			# x:28 y:353
			OperatableStateMachine.add('replace arm before check personalreadyin',
										RunTrajectory(file="repos", duration=0),
										transitions={'done': 'check if person already in is known aka ID not 0'},
										autonomy={'done': Autonomy.Off})

			# x:465 y:492
			OperatableStateMachine.add('filter the list',
										FilterKey(filter_function=lambda x: x[0].name == "person" and x[0].ID != x[1] and x[0].ID != x[2], input_keys=["entity_list", "Guest1ID", "Guest2ID"]),
										transitions={'not_empty': 'take first entity', 'empty': 'say not/cannot found person already in but say name/drink'},
										autonomy={'not_empty': Autonomy.Off, 'empty': Autonomy.Off},
										remapping={'entity_list': 'entity_list', 'Guest1ID': 'Guest1ID', 'Guest2ID': 'Guest2ID', 'output_list': 'output_list'})

			# x:639 y:418
			OperatableStateMachine.add('get entity list',
										list_entities_by_name(frontality_level=0.5, distance_max=5),
										transitions={'found': 'filter the list', 'none_found': 'say not/cannot found person already in but say name/drink'},
										autonomy={'found': Autonomy.Off, 'none_found': Autonomy.Off},
										remapping={'name': 'keyPerson', 'entity_list': 'entity_list', 'number': 'number'})

			# x:329 y:546
			OperatableStateMachine.add('take first entity',
										CalculationState(calculation=lambda x: x[0]),
										transitions={'done': 'calculation'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'output_list', 'output_value': 'output_entity'})

			# x:196 y:592
			OperatableStateMachine.add('calculation',
										CalculationState(calculation=lambda x: x),
										transitions={'done': 'Point person already in'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'output_entity', 'output_value': 'personAlreadyInEntity'})

			# x:455 y:427
			OperatableStateMachine.add('set key for filter',
										SetKey(Value="person"),
										transitions={'done': 'get entity list'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'keyPerson'})


		# x:1125 y:673, x:1146 y:27
		_sm_guide_g1_and_introduice_people_20 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['personAlreadyInLocation', 'personAlreadyInName', 'personAlreadyInDrink', 'Guest1Drink', 'Guest1Name', 'Guest1ID'], output_keys=['personAlreadyInID'])

		with _sm_guide_g1_and_introduice_people_20:
			# x:75 y:21
			OperatableStateMachine.add('move to the place',
										_sm_move_to_the_place_14,
										transitions={'finished': 'Find person already in', 'failed': 'retry guide to location'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'Guest1Name': 'Guest1Name', 'personAlreadyInLocation': 'personAlreadyInLocation'})

			# x:585 y:26
			OperatableStateMachine.add('say cannot reach destination',
										SaraSay(sentence="I cannot reach the destination.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'set personAlreadyInEntity to unknown'},
										autonomy={'done': Autonomy.Off})

			# x:451 y:208
			OperatableStateMachine.add('say cannot find personAlreadyIn',
										SaraSay(sentence=lambda x: "I can not find"+x[0]+" but I will continue the scenario. The favorite drink of "+x[0]+" is "+x[1]+".", input_keys=["personAlreadyInName", "personAlreadyInDrink"], emotion=0, block=True),
										transitions={'done': 'set personAlreadyInID to unknown and continue'},
										autonomy={'done': Autonomy.Off},
										remapping={'personAlreadyInName': 'personAlreadyInName', 'personAlreadyInDrink': 'personAlreadyInDrink'})

			# x:782 y:21
			OperatableStateMachine.add('set personAlreadyInEntity to unknown',
										SetKey(Value=0),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'personAlreadyInID'})

			# x:61 y:517
			OperatableStateMachine.add('introduice G1 to person already in',
										SaraSay(sentence=lambda x: x[0]+", I would like to introduice you "+x[1]+" and his favorite drink is "+x[2]+".", input_keys=["Guest1Name","personAlreadyInName", "personAlreadyInDrink"], emotion=0, block=True),
										transitions={'done': 'replace arm before point chair'},
										autonomy={'done': Autonomy.Off},
										remapping={'Guest1Name': 'Guest1Name', 'personAlreadyInName': 'personAlreadyInName', 'personAlreadyInDrink': 'personAlreadyInDrink'})

			# x:415 y:328
			OperatableStateMachine.add('set personAlreadyInID to unknown and continue',
										SetKey(Value=0),
										transitions={'done': 'find and point empty chair'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'personAlreadyInID'})

			# x:80 y:826
			OperatableStateMachine.add('say sit there',
										SaraSay(sentence=lambda x: x[0]+", you can sit there.", input_keys=["Guest1Name"], emotion=0, block=True),
										transitions={'done': 'position repos bras'},
										autonomy={'done': Autonomy.Off},
										remapping={'Guest1Name': 'Guest1Name'})

			# x:369 y:506
			OperatableStateMachine.add('say cannot point person already in',
										SaraSay(sentence=lambda x: "I can not point to "+x[0]+" but it is the only person in this room. His favorite drink is "+x[1]+".", input_keys=["personAlreadyInName","personAlreadyInDrink"], emotion=0, block=True),
										transitions={'done': 'replace arm before point chair'},
										autonomy={'done': Autonomy.Off},
										remapping={'personAlreadyInName': 'personAlreadyInName', 'personAlreadyInDrink': 'personAlreadyInDrink'})

			# x:434 y:830
			OperatableStateMachine.add('position repos bras',
										RunTrajectory(file="repos", duration=0),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:87 y:285
			OperatableStateMachine.add('introduice G1',
										SaraSay(sentence=lambda x: "Hello "+x[0]+". Here is a new guest. His name is "+x[1]+" and love to drink "+x[2]+".", input_keys=["personAlreadyInName", "Guest1Name", "Guest1Drink"], emotion=0, block=True),
										transitions={'done': 'point person already in'},
										autonomy={'done': Autonomy.Off},
										remapping={'personAlreadyInName': 'personAlreadyInName', 'Guest1Name': 'Guest1Name', 'Guest1Drink': 'Guest1Drink'})

			# x:70 y:164
			OperatableStateMachine.add('Find person already in',
										_sm_find_person_already_in_13,
										transitions={'done': 'introduice G1', 'failed': 'say cannot find personAlreadyIn'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'Guest1ID': 'Guest1ID', 'foundEntity': 'foundEntity', 'personAlreadyInID': 'personAlreadyInID'})

			# x:71 y:413
			OperatableStateMachine.add('point person already in',
										_sm_point_person_already_in_12,
										transitions={'finished': 'introduice G1 to person already in', 'failed': 'say cannot point person already in'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'foundEntity': 'foundEntity'})

			# x:63 y:705
			OperatableStateMachine.add('find and point empty chair',
										_sm_find_and_point_empty_chair_11,
										transitions={'nothing_found': 'replace arm', 'finished': 'say sit there', 'failed': 'replace arm 2'},
										autonomy={'nothing_found': Autonomy.Inherit, 'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:409 y:25
			OperatableStateMachine.add('retry guide to location',
										ForLoop(repeat=2),
										transitions={'do': 'move to the place', 'end': 'say cannot reach destination'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index'})

			# x:642 y:639
			OperatableStateMachine.add('replace arm',
										_sm_replace_arm_10,
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Inherit},
										remapping={'Guest1Name': 'Guest1Name'})

			# x:644 y:716
			OperatableStateMachine.add('replace arm 2',
										_sm_replace_arm_2_9,
										transitions={'finished': 'finished'},
										autonomy={'finished': Autonomy.Inherit},
										remapping={'Guest1Name': 'Guest1Name'})

			# x:68 y:600
			OperatableStateMachine.add('replace arm before point chair',
										RunTrajectory(file="repos", duration=0),
										transitions={'done': 'find and point empty chair'},
										autonomy={'done': Autonomy.Off})


		# x:1010 y:784, x:1230 y:226
		_sm_welcome_guest2_21 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['entranceLocation'], output_keys=['Guest2Drink', 'Guest2Name', 'Guest2ID'])

		with _sm_welcome_guest2_21:
			# x:95 y:34
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'Welcome Guest2/Action_Move'),
										transitions={'finished': 'say ready', 'failed': 'retry moving G2'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'entranceLocation'})

			# x:294 y:35
			OperatableStateMachine.add('retry moving G2',
										ForLoop(repeat=2),
										transitions={'do': 'Action_Move', 'end': 'say cannot do task G2'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index'})

			# x:577 y:211
			OperatableStateMachine.add('say cannot do task G2',
										SaraSay(sentence="I failed to do my task.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'set G2 name to unknown'},
										autonomy={'done': Autonomy.Off})

			# x:83 y:263
			OperatableStateMachine.add('Action_findPerson',
										self.use_behavior(sara_flexbe_behaviors__Action_findPersonSM, 'Welcome Guest2/Action_findPerson', default_keys=['className']),
										transitions={'done': 'get the ID for G2', 'pas_done': 'say cannot do task G2'},
										autonomy={'done': Autonomy.Inherit, 'pas_done': Autonomy.Inherit},
										remapping={'className': 'className', 'entity': 'person2Entity'})

			# x:718 y:213
			OperatableStateMachine.add('set G2 name to unknown',
										SetKey(Value="unknown"),
										transitions={'done': 'set G2 drink to unknown'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Guest2Name'})

			# x:877 y:214
			OperatableStateMachine.add('set G2 drink to unknown',
										SetKey(Value="unknown"),
										transitions={'done': 'set G2 ID to 0'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Guest2Drink'})

			# x:1038 y:214
			OperatableStateMachine.add('set G2 ID to 0',
										SetKey(Value=0),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Guest2ID'})

			# x:97 y:356
			OperatableStateMachine.add('get the ID for G2',
										GetAttribute(attributes=["ID"]),
										transitions={'done': 'Ask name and drink while keep looking at person'},
										autonomy={'done': Autonomy.Off},
										remapping={'object': 'person2Entity', 'ID': 'person2ID'})

			# x:61 y:514
			OperatableStateMachine.add('Ask name and drink while keep looking at person',
										_sm_ask_name_and_drink_while_keep_looking_at_person_17,
										transitions={'finished': 'Action_findPerson_2', 'failed': 'Ask name and drink while keep looking at person'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'personID': 'person2ID', 'Guest2Name': 'Guest2Name', 'Guest2Drink': 'Guest2Drink'})

			# x:114 y:627
			OperatableStateMachine.add('Action_findPerson_2',
										self.use_behavior(sara_flexbe_behaviors__Action_findPersonSM, 'Welcome Guest2/Action_findPerson_2', default_keys=['className']),
										transitions={'done': 'get Guest1 ID_2', 'pas_done': 'put previous ID in Guest1ID'},
										autonomy={'done': Autonomy.Inherit, 'pas_done': Autonomy.Inherit},
										remapping={'className': 'className', 'entity': 'Guest2Entity'})

			# x:135 y:777
			OperatableStateMachine.add('get Guest1 ID_2',
										GetAttribute(attributes=["ID"]),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'object': 'Guest2Entity', 'ID': 'Guest2ID'})

			# x:316 y:666
			OperatableStateMachine.add('put previous ID in Guest1ID',
										CalculationState(calculation=lambda x: x),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'person2ID', 'output_value': 'Guest2ID'})

			# x:108 y:117
			OperatableStateMachine.add('say ready',
										SaraSay(sentence="I am ready to welcome the second guest. Please enter and stay in front of me.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'wait 5'},
										autonomy={'done': Autonomy.Off})

			# x:109 y:186
			OperatableStateMachine.add('wait 5',
										WaitState(wait_time=5),
										transitions={'done': 'Action_findPerson'},
										autonomy={'done': Autonomy.Off})



		with _state_machine:
			# x:300 y:25
			OperatableStateMachine.add('Init_Sequence',
										self.use_behavior(sara_flexbe_behaviors__Init_SequenceSM, 'Init_Sequence'),
										transitions={'finished': 'say ready', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:319 y:541
			OperatableStateMachine.add('Welcome Guest2',
										_sm_welcome_guest2_21,
										transitions={'finished': 'Guide G2 and introduice people', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'entranceLocation': 'entranceLocation', 'Guest2Drink': 'Guest2Drink', 'Guest2Name': 'Guest2Name', 'Guest2ID': 'Guest2ID'})

			# x:291 y:324
			OperatableStateMachine.add('Guide G1 and introduice people',
										_sm_guide_g1_and_introduice_people_20,
										transitions={'finished': 'Welcome Guest2', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'personAlreadyInLocation': 'personAlreadyInLocation', 'personAlreadyInName': 'personAlreadyInName', 'personAlreadyInDrink': 'personAlreadyInDrink', 'Guest1Drink': 'Guest1Drink', 'Guest1Name': 'Guest1Name', 'Guest1ID': 'Guest1ID', 'personAlreadyInID': 'personAlreadyInID'})

			# x:299 y:626
			OperatableStateMachine.add('Guide G2 and introduice people',
										_sm_guide_g2_and_introduice_people_19,
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'personAlreadyInLocation': 'personAlreadyInLocation', 'personAlreadyInName': 'personAlreadyInName', 'personAlreadyInDrink': 'personAlreadyInDrink', 'Guest1Drink': 'Guest1Drink', 'Guest1Name': 'Guest1Name', 'Guest1ID': 'Guest1ID', 'personAlreadyInID': 'personAlreadyInID', 'Guest2Drink': 'Guest2Drink', 'Guest2Name': 'Guest2Name', 'Guest2ID': 'Guest2ID'})

			# x:314 y:224
			OperatableStateMachine.add('welcome Guest1',
										_sm_welcome_guest1_18,
										transitions={'finished': 'Guide G1 and introduice people', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'entranceLocation': 'entranceLocation', 'Guest1Drink': 'Guest1Drink', 'Guest1Name': 'Guest1Name', 'Guest1ID': 'Guest1ID'})

			# x:317 y:106
			OperatableStateMachine.add('say ready',
										SaraSay(sentence="I am ready to welcome the first guest. Please enter and stay near the entrance.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'welcome Guest1'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
