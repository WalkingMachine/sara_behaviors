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
from sara_flexbe_states.sara_set_head_angle import SaraSetHeadAngle
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.Filter import Filter
from flexbe_states.check_condition_state import CheckConditionState
from sara_flexbe_states.SetKey import SetKey
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.list_entities_by_name import list_entities_by_name
from sara_flexbe_behaviors.action_move_sm import Action_MoveSM as sara_flexbe_behaviors__Action_MoveSM
from sara_flexbe_states.GetAttribute import GetAttribute
from sara_flexbe_states.get_reachable_waypoint import Get_Reacheable_Waypoint
from sara_flexbe_states.SetRosParam import SetRosParam
from sara_flexbe_states.regex_tester import RegexTester
from sara_flexbe_states.get_speech import GetSpeech
from sara_flexbe_behaviors.lookatclosest_sm import LookAtClosestSM as sara_flexbe_behaviors__LookAtClosestSM
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
		self.add_behavior(sara_flexbe_behaviors__Init_SequenceSM, 'Init_Sequence')
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'GetTaxi/Action_Move_to taxi')
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'GetTaxi/Action_Move')
		self.add_behavior(sara_flexbe_behaviors__LookAtClosestSM, 'confirm/LookAtClosest')
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'Get closer/Action_Move')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]

		# [/MANUAL_INIT]

		# Behavior comments:

		# O 832 253 
		# Retrieve coats

		# O 250 196 
		# On filtre les gens qui wavent et les femmes

		# O 224 438 
		# ON confirme que la personne veut partir

		# O 242 543 
		# on sapproche du taxi

		# O 821 211 
		# Il reste a prendre les manteaux|net ramener la deuxieme personne



	def create(self):
		# x:712 y:612, x:820 y:97
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.name = "person"
		_state_machine.userdata.distance = 1.5
		_state_machine.userdata.taxi = "taxi"
		_state_machine.userdata.vest = "vest"

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]

		# [/MANUAL_CREATE]

		# x:381 y:322, x:360 y:516
		_sm_confirm_0 = OperatableStateMachine(outcomes=['false', 'done'], input_keys=['Person', 'pronoun'])

		with _sm_confirm_0:
			# x:87 y:59
			OperatableStateMachine.add('Confirm',
										SaraSay(sentence=lambda x: "would you like to leave, " + x[0] + "?", input_keys=["pronoun"], emotion=0, block=True),
										transitions={'done': 'GetSpeech'},
										autonomy={'done': Autonomy.Off},
										remapping={'pronoun': 'pronoun'})

			# x:82 y:504
			OperatableStateMachine.add('GetID',
										SetRosParam(ParamName="OpeID"),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off},
										remapping={'Value': 'ID'})

			# x:83 y:312
			OperatableStateMachine.add('if yes',
										RegexTester(regex=".*((yes)|(I do)).*"),
										transitions={'true': 'get id', 'false': 'false'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'text': 'text', 'result': 'result'})

			# x:84 y:409
			OperatableStateMachine.add('get id',
										GetAttribute(attributes=["ID"]),
										transitions={'done': 'GetID'},
										autonomy={'done': Autonomy.Off},
										remapping={'object': 'Person', 'ID': 'ID'})

			# x:87 y:188
			OperatableStateMachine.add('GetSpeech',
										GetSpeech(watchdog=10),
										transitions={'done': 'if yes', 'nothing': 'false', 'fail': 'if yes'},
										autonomy={'done': Autonomy.Off, 'nothing': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'words': 'text'})


		# x:32 y:494, x:627 y:411
		_sm_filtregender_1 = OperatableStateMachine(outcomes=['none_found', 'found person'], input_keys=['name'], output_keys=['pronoun', 'person'])

		with _sm_filtregender_1:
			# x:56 y:31
			OperatableStateMachine.add('Looking',
										SaraSay(sentence="I am trying to find who wants to leave", input_keys=[], emotion=0, block=True),
										transitions={'done': 'List'},
										autonomy={'done': Autonomy.Off})

			# x:401 y:72
			OperatableStateMachine.add('FiltreWave',
										Filter(filter=lambda x: x.pose == "waving"),
										transitions={'done': 'FiltreWave'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_list': 'entity_list', 'output_list': 'persons'})

			# x:183 y:199
			OperatableStateMachine.add('FiltreExitingwomen',
										Filter(filter=lambda x: x.face.gender == "female"),
										transitions={'done': 'no female?'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_list': 'entity_list', 'output_list': 'female'})

			# x:181 y:292
			OperatableStateMachine.add('no female?',
										CheckConditionState(predicate=lambda x: len(x)>0),
										transitions={'true': 'set pronoun female', 'false': 'set pronoun male'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'female'})

			# x:358 y:301
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

			# x:585 y:207
			OperatableStateMachine.add('get first female',
										CalculationState(calculation=lambda x: x[0]),
										transitions={'done': 'found person'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'female', 'output_value': 'person'})

			# x:381 y:408
			OperatableStateMachine.add('get first male',
										CalculationState(calculation=lambda x: x[0]),
										transitions={'done': 'found person'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'entity_list', 'output_value': 'person'})

			# x:192 y:94
			OperatableStateMachine.add('List',
										list_entities_by_name(frontality_level=0.5, distance_max=10),
										transitions={'found': 'FiltreExitingwomen', 'none_found': 'none_found'},
										autonomy={'found': Autonomy.Off, 'none_found': Autonomy.Off},
										remapping={'name': 'name', 'entity_list': 'entity_list', 'number': 'number'})


		# x:139 y:372
		_sm_get_closer_2 = OperatableStateMachine(outcomes=['finished'], input_keys=['distance', 'person'])

		with _sm_get_closer_2:
			# x:91 y:37
			OperatableStateMachine.add('GetPose',
										GetAttribute(attributes=["position"]),
										transitions={'done': 'GetCloser'},
										autonomy={'done': Autonomy.Off},
										remapping={'object': 'person', 'position': 'position'})

			# x:82 y:134
			OperatableStateMachine.add('GetCloser',
										Get_Reacheable_Waypoint(),
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose_in': 'position', 'distance': 'distance', 'pose_out': 'pose_out'})

			# x:83 y:246
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'Get closer/Action_Move'),
										transitions={'finished': 'finished', 'failed': 'finished'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'pose_out'})


		# x:30 y:458, x:130 y:458, x:230 y:458, x:330 y:458, x:430 y:458
		_sm_confirm_3 = ConcurrencyContainer(outcomes=['false', 'done'], input_keys=['person', 'pronoun'], conditions=[
										('false', [('Confirm', 'false')]),
										('done', [('Confirm', 'done')]),
										('false', [('LookAtClosest', 'failed')])
										])

		with _sm_confirm_3:
			# x:95 y:163
			OperatableStateMachine.add('Confirm',
										_sm_confirm_0,
										transitions={'false': 'false', 'done': 'done'},
										autonomy={'false': Autonomy.Inherit, 'done': Autonomy.Inherit},
										remapping={'Person': 'person', 'pronoun': 'pronoun'})

			# x:309 y:162
			OperatableStateMachine.add('LookAtClosest',
										self.use_behavior(sara_flexbe_behaviors__LookAtClosestSM, 'confirm/LookAtClosest'),
										transitions={'failed': 'false'},
										autonomy={'failed': Autonomy.Inherit})


		# x:88 y:393, x:578 y:284
		_sm_gettaxi_4 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['vest', 'distance', 'taxi'])

		with _sm_gettaxi_4:
			# x:40 y:28
			OperatableStateMachine.add('Action_Move_to taxi',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'GetTaxi/Action_Move_to taxi'),
										transitions={'finished': 'GetTaxi', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'taxi'})

			# x:47 y:256
			OperatableStateMachine.add('GEtVest',
										GetAttribute(attributes=["position"]),
										transitions={'done': 'NotTooClose'},
										autonomy={'done': Autonomy.Off},
										remapping={'object': 'vest_list', 'position': 'position'})

			# x:243 y:373
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'GetTaxi/Action_Move'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'pose_out'})

			# x:249 y:255
			OperatableStateMachine.add('NotTooClose',
										Get_Reacheable_Waypoint(),
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose_in': 'position', 'distance': 'distance', 'pose_out': 'pose_out'})

			# x:45 y:147
			OperatableStateMachine.add('GetTaxi',
										list_entities_by_name(frontality_level=0.5, distance_max=10),
										transitions={'found': 'GEtVest', 'none_found': 'GEtVest'},
										autonomy={'found': Autonomy.Off, 'none_found': Autonomy.Off},
										remapping={'name': 'vest', 'entity_list': 'vest_list', 'number': 'number'})


		# x:463 y:38, x:447 y:185
		_sm_get_gender_5 = OperatableStateMachine(outcomes=['none_found', 'done'], input_keys=['name', 'distance'], output_keys=['person', 'pronoun'])

		with _sm_get_gender_5:
			# x:30 y:40
			OperatableStateMachine.add('set head',
										SaraSetHeadAngle(pitch=0, yaw=0),
										transitions={'done': 'FiltreGender'},
										autonomy={'done': Autonomy.Off})

			# x:197 y:53
			OperatableStateMachine.add('FiltreGender',
										_sm_filtregender_1,
										transitions={'none_found': 'none_found', 'found person': 'done'},
										autonomy={'none_found': Autonomy.Inherit, 'found person': Autonomy.Inherit},
										remapping={'name': 'name', 'pronoun': 'pronoun', 'person': 'person'})



		with _state_machine:
			# x:81 y:38
			OperatableStateMachine.add('Init_Sequence',
										self.use_behavior(sara_flexbe_behaviors__Init_SequenceSM, 'Init_Sequence'),
										transitions={'finished': 'Get Gender', 'failed': 'say fail'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:99 y:141
			OperatableStateMachine.add('Get Gender',
										_sm_get_gender_5,
										transitions={'none_found': 'say nobody', 'done': 'Get closer'},
										autonomy={'none_found': Autonomy.Inherit, 'done': Autonomy.Inherit},
										remapping={'name': 'name', 'distance': 'distance', 'person': 'person', 'pronoun': 'pronoun'})

			# x:117 y:565
			OperatableStateMachine.add('GetTaxi',
										_sm_gettaxi_4,
										transitions={'finished': 'say succeed', 'failed': 'say fail'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'vest': 'vest', 'distance': 'distance', 'taxi': 'taxi'})

			# x:104 y:327
			OperatableStateMachine.add('confirm',
										_sm_confirm_3,
										transitions={'false': 'say ok', 'done': 'say taxi'},
										autonomy={'false': Autonomy.Inherit, 'done': Autonomy.Inherit},
										remapping={'person': 'person', 'pronoun': 'pronoun'})

			# x:313 y:113
			OperatableStateMachine.add('say nobody',
										SaraSay(sentence="There is nobody here.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'say fail'},
										autonomy={'done': Autonomy.Off})

			# x:571 y:44
			OperatableStateMachine.add('say fail',
										SaraSay(sentence="I failed this scenario. Sorry.", input_keys=[], emotion=3, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:506 y:600
			OperatableStateMachine.add('say succeed',
										SaraSay(sentence="Yay! I succeeded this scenario!", input_keys=[], emotion=5, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:22 y:229
			OperatableStateMachine.add('say ok',
										SaraSay(sentence="Ok, nevermind.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'Get Gender'},
										autonomy={'done': Autonomy.Off})

			# x:229 y:236
			OperatableStateMachine.add('Get closer',
										_sm_get_closer_2,
										transitions={'finished': 'confirm'},
										autonomy={'finished': Autonomy.Inherit},
										remapping={'distance': 'distance', 'person': 'person'})

			# x:114 y:465
			OperatableStateMachine.add('say taxi',
										SaraSay(sentence="Ok, follow me to the taxi then.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'GetTaxi'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]

	# [/MANUAL_FUNC]
