#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_behaviors.sara_init_sm import Sara_InitSM as sara_flexbe_behaviors__Sara_InitSM
from sara_flexbe_states.get_speech import GetSpeech
from sara_flexbe_states.SetRosParam import SetRosParam
from sara_flexbe_states.regex_tester import RegexTester
from sara_flexbe_states.list_entities_by_name import list_entities_by_name
from sara_flexbe_states.Filter import Filter
from flexbe_states.check_condition_state import CheckConditionState
from sara_flexbe_states.SetKey import SetKey
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.get_reachable_waypoint import Get_Reacheable_Waypoint
from sara_flexbe_states.GetAttribute import GetAttribute
from sara_flexbe_behaviors.action_move_sm import Action_MoveSM as sara_flexbe_behaviors__Action_MoveSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Mar 18 2019
@author: Huynh-Anh Le
'''
class FarewellSM(Behavior):
	'''
	Some guests are tired, so they call the robot to retrieve their coat.  It’s raining outside and thereis only one umbrella, so the robot takes the guests one by one to their cab and returns with theumbrella
	'''


	def __init__(self):
		super(FarewellSM, self).__init__()
		self.name = 'Farewell'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(sara_flexbe_behaviors__Sara_InitSM, 'Sara_Init')
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'GetGEnder/Action_Move')
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'GetTaxi/Action_Move')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]

		# [/MANUAL_INIT]

		# Behavior comments:

		# O 683 215 
		# Retrieve coats

		# O 228 184 
		# On filtre les gens qui wavent et les femmes

		# O 220 309 
		# ON confirme que la personne veut partir

		# O 241 422 
		# on sapproche du taxi

		# O 683 162 
		# Il reste a prendre les manteaux|net ramener la deuxieme personne



	def create(self):
		# x:492 y:550, x:557 y:117
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.name = "person"
		_state_machine.userdata.distance = 0.5
		_state_machine.userdata.taxi = "taxi"
		_state_machine.userdata.vest = "vest"

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]

		# [/MANUAL_CREATE]

		# x:32 y:494, x:627 y:411
		_sm_filtregender_0 = OperatableStateMachine(outcomes=['none_found', 'found person'], input_keys=['name'], output_keys=['pronoun', 'person'])

		with _sm_filtregender_0:
			# x:174 y:24
			OperatableStateMachine.add('List',
										list_entities_by_name(frontality_level=0.5, distance_max=10),
										transitions={'found': 'FiltreWave', 'none_found': 'none_found'},
										autonomy={'found': Autonomy.Off, 'none_found': Autonomy.Off},
										remapping={'name': 'name', 'entity_list': 'entity_list', 'number': 'number'})

			# x:179 y:109
			OperatableStateMachine.add('FiltreWave',
										Filter(filter=lambda x: x.pose == "waving"),
										transitions={'done': 'FiltreExitingwomen'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_list': 'entity_list', 'output_list': 'persons'})

			# x:183 y:199
			OperatableStateMachine.add('FiltreExitingwomen',
										Filter(filter=lambda x: x.face.gender == "female"),
										transitions={'done': 'no female?'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_list': 'persons', 'output_list': 'female'})

			# x:181 y:292
			OperatableStateMachine.add('no female?',
										CheckConditionState(predicate=lambda x: len(x)>0),
										transitions={'true': 'set pronoun female', 'false': 'set pronoun male'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'female'})

			# x:400 y:293
			OperatableStateMachine.add('set pronoun female',
										SetKey(Value="miss"),
										transitions={'done': 'get first female'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'pronoun'})

			# x:184 y:394
			OperatableStateMachine.add('set pronoun male',
										SetKey(Value="mister"),
										transitions={'done': 'get first male'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'pronoun'})

			# x:590 y:293
			OperatableStateMachine.add('get first female',
										CalculationState(calculation=lambda x: x[0]),
										transitions={'done': 'found person'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'female', 'output_value': 'person'})

			# x:427 y:391
			OperatableStateMachine.add('get first male',
										CalculationState(calculation=lambda x: x[0]),
										transitions={'done': 'found person'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'persons', 'output_value': 'person'})


		# x:30 y:365
		_sm_gettaxi_1 = OperatableStateMachine(outcomes=['finished'], input_keys=['vest', 'distance'])

		with _sm_gettaxi_1:
			# x:34 y:40
			OperatableStateMachine.add('GetTaxi',
										list_entities_by_name(frontality_level=0.5, distance_max=10),
										transitions={'found': 'GEtVest', 'none_found': 'GEtVest'},
										autonomy={'found': Autonomy.Off, 'none_found': Autonomy.Off},
										remapping={'name': 'vest', 'entity_list': 'vest_list', 'number': 'number'})

			# x:30 y:138
			OperatableStateMachine.add('GEtVest',
										GetAttribute(attributes=["position"]),
										transitions={'done': 'NotTooClose'},
										autonomy={'done': Autonomy.Off},
										remapping={'object': 'vest_list', 'position': 'position'})

			# x:431 y:153
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'GetTaxi/Action_Move'),
										transitions={'finished': 'finished', 'failed': 'Action_Move'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'pose_out'})

			# x:210 y:153
			OperatableStateMachine.add('NotTooClose',
										Get_Reacheable_Waypoint(),
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose_in': 'position', 'distance': 'distance', 'pose_out': 'pose_out'})


		# x:463 y:38, x:714 y:633
		_sm_getgender_2 = OperatableStateMachine(outcomes=['none_found', 'done'], input_keys=['name', 'distance'], output_keys=['person'])

		with _sm_getgender_2:
			# x:122 y:40
			OperatableStateMachine.add('FiltreGender',
										_sm_filtregender_0,
										transitions={'none_found': 'none_found', 'found person': 'GetPose'},
										autonomy={'none_found': Autonomy.Inherit, 'found person': Autonomy.Inherit},
										remapping={'name': 'name', 'pronoun': 'pronoun', 'person': 'person'})

			# x:302 y:541
			OperatableStateMachine.add('Confirm',
										SaraSay(sentence="would you like to leave?", input_keys=[], emotion=0, block=True),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off})

			# x:95 y:382
			OperatableStateMachine.add('GetCloser',
										Get_Reacheable_Waypoint(),
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose_in': 'position', 'distance': 'distance', 'pose_out': 'pose_out'})

			# x:119 y:250
			OperatableStateMachine.add('GetPose',
										GetAttribute(attributes=["position"]),
										transitions={'done': 'GetCloser'},
										autonomy={'done': Autonomy.Off},
										remapping={'object': 'person', 'position': 'position'})

			# x:106 y:478
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'GetGEnder/Action_Move'),
										transitions={'finished': 'Confirm', 'failed': 'Confirm'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'pose_out'})


		# x:392 y:183, x:268 y:346
		_sm_confirm_3 = OperatableStateMachine(outcomes=['false', 'done'], input_keys=['Person'])

		with _sm_confirm_3:
			# x:44 y:40
			OperatableStateMachine.add('GetSpeech',
										GetSpeech(watchdog=10),
										transitions={'done': 'Listen', 'nothing': 'Listen', 'fail': 'Listen'},
										autonomy={'done': Autonomy.Off, 'nothing': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'words': 'text'})

			# x:30 y:261
			OperatableStateMachine.add('GetID',
										SetRosParam(ParamName=OpeID),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off},
										remapping={'Value': 'Person'})

			# x:37 y:161
			OperatableStateMachine.add('Listen',
										RegexTester(regex=".*((yes)|(I do).*"),
										transitions={'true': 'GetID', 'false': 'false'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'text': 'text', 'result': 'result'})



		with _state_machine:
			# x:89 y:30
			OperatableStateMachine.add('Sara_Init',
										self.use_behavior(sara_flexbe_behaviors__Sara_InitSM, 'Sara_Init'),
										transitions={'finished': 'GetGEnder', 'failed': 'GetGEnder'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:91 y:295
			OperatableStateMachine.add('Confirm',
										_sm_confirm_3,
										transitions={'false': 'GetGEnder', 'done': 'GetTaxi'},
										autonomy={'false': Autonomy.Inherit, 'done': Autonomy.Inherit},
										remapping={'Person': 'person'})

			# x:90 y:153
			OperatableStateMachine.add('GetGEnder',
										_sm_getgender_2,
										transitions={'none_found': 'failed', 'done': 'Confirm'},
										autonomy={'none_found': Autonomy.Inherit, 'done': Autonomy.Inherit},
										remapping={'name': 'name', 'distance': 'distance', 'person': 'person'})

			# x:99 y:418
			OperatableStateMachine.add('GetTaxi',
										_sm_gettaxi_1,
										transitions={'finished': 'finished'},
										autonomy={'finished': Autonomy.Inherit},
										remapping={'vest': 'vest', 'distance': 'distance'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]

	# [/MANUAL_FUNC]
