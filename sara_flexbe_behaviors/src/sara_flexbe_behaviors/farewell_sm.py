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
from sara_flexbe_behaviors.actionwrapper_move_sm import ActionWrapper_MoveSM as sara_flexbe_behaviors__ActionWrapper_MoveSM
from sara_flexbe_states.list_entities_by_name import list_entities_by_name
from sara_flexbe_states.Filter import Filter
from flexbe_states.log_key_state import LogKeyState
from sara_flexbe_states.sara_say import SaraSay
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.get_reachable_waypoint import Get_Reacheable_Waypoint
from sara_flexbe_states.GetAttribute import GetAttribute
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
		self.add_behavior(sara_flexbe_behaviors__ActionWrapper_MoveSM, 'ActionWrapper_Move')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]

		# [/MANUAL_INIT]

		# Behavior comments:

		# O 156 646 
		# Retrieve coats

		# O 327 207 
		# empty= just male|ndone = female

		# O 254 418 
		# confirm

		# O 131 674 
		# se diriger vers le taxi

		# O 247 297 
		# si cest false, on retourne voir les bonne personnes



	def create(self):
		# x:580 y:663, x:557 y:117
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.name = "person"
		_state_machine.userdata.Action = ["move","taxi"]
		_state_machine.userdata.distance = 0.5

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]

		# [/MANUAL_CREATE]

		# x:32 y:494, x:233 y:480, x:477 y:334
		_sm_filtregender_0 = OperatableStateMachine(outcomes=['none_found', 'List_Wave', 'List_women'], input_keys=['name'], output_keys=['List_Women', 'List_Wave'])

		with _sm_filtregender_0:
			# x:30 y:97
			OperatableStateMachine.add('List',
										list_entities_by_name(frontality_level=0.5, distance_max=10),
										transitions={'found': 'Entities_List', 'none_found': 'none_found'},
										autonomy={'found': Autonomy.Off, 'none_found': Autonomy.Off},
										remapping={'name': 'name', 'entity_list': 'entity_list', 'number': 'number'})

			# x:205 y:206
			OperatableStateMachine.add('FiltreWave',
										Filter(filter=lambda x: x.pose == "waving"),
										transitions={'done': 'FiltreExitingPeople', 'empty': 'FiltreExitingPeople'},
										autonomy={'done': Autonomy.Off, 'empty': Autonomy.Off},
										remapping={'input_list': 'entity_list', 'output_list': 'List_Wave'})

			# x:312 y:67
			OperatableStateMachine.add('Entities_List',
										LogKeyState(text="{}", severity=Logger.REPORT_HINT),
										transitions={'done': 'FiltreWave'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'entity_list'})

			# x:212 y:343
			OperatableStateMachine.add('FiltreExitingPeople',
										Filter(filter=lambda x: x.face.gender == "female"),
										transitions={'done': 'List_women', 'empty': 'List_Wave'},
										autonomy={'done': Autonomy.Off, 'empty': Autonomy.Off},
										remapping={'input_list': 'List_Wave', 'output_list': 'List_women'})


		# x:602 y:150, x:190 y:547
		_sm_confirm__1 = OperatableStateMachine(outcomes=['none_found', 'done'], input_keys=['name', 'distance'], output_keys=['Person'])

		with _sm_confirm__1:
			# x:122 y:40
			OperatableStateMachine.add('FiltreGender',
										_sm_filtregender_0,
										transitions={'none_found': 'none_found', 'List_Wave': 'GetIdM', 'List_women': 'GetIdF'},
										autonomy={'none_found': Autonomy.Inherit, 'List_Wave': Autonomy.Inherit, 'List_women': Autonomy.Inherit},
										remapping={'name': 'name', 'List_Women': 'List_women', 'List_Wave': 'List_Wave'})

			# x:112 y:491
			OperatableStateMachine.add('Confirm',
										SaraSay(sentence="would you like to leave?", input_keys=[], emotion=0, block=True),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off})

			# x:31 y:142
			OperatableStateMachine.add('GetIdM',
										CalculationState(calculation=lambda x: x[0]),
										transitions={'done': 'GetPose'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'List_Wave', 'output_value': 'Person'})

			# x:95 y:382
			OperatableStateMachine.add('GetCloser',
										Get_Reacheable_Waypoint(),
										transitions={'done': 'Confirm'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose_in': 'position', 'distance': 'distance', 'pose_out': 'pose_out'})

			# x:119 y:250
			OperatableStateMachine.add('GetPose',
										GetAttribute(attributes=["position"]),
										transitions={'done': 'GetCloser'},
										autonomy={'done': Autonomy.Off},
										remapping={'object': 'Person', 'position': 'position'})

			# x:258 y:145
			OperatableStateMachine.add('GetIdF',
										CalculationState(calculation=lambda x: x[0]),
										transitions={'done': 'GetPose'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'List_women', 'output_value': 'Person'})


		# x:392 y:183, x:268 y:346
		_sm_getid_2 = OperatableStateMachine(outcomes=['false', 'done'], input_keys=['Person'])

		with _sm_getid_2:
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

			# x:40 y:146
			OperatableStateMachine.add('Listen',
										RegexTester(regex=".*((yes)|(I do).*"),
										transitions={'true': 'GetID', 'false': 'false'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'text': 'text', 'result': 'result'})



		with _state_machine:
			# x:89 y:30
			OperatableStateMachine.add('Sara_Init',
										self.use_behavior(sara_flexbe_behaviors__Sara_InitSM, 'Sara_Init'),
										transitions={'finished': 'Confirm ', 'failed': 'Confirm '},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:91 y:295
			OperatableStateMachine.add('GetID',
										_sm_getid_2,
										transitions={'false': 'Confirm ', 'done': 'ActionWrapper_Move'},
										autonomy={'false': Autonomy.Inherit, 'done': Autonomy.Inherit},
										remapping={'Person': 'Person'})

			# x:159 y:582
			OperatableStateMachine.add('ActionWrapper_Move',
										self.use_behavior(sara_flexbe_behaviors__ActionWrapper_MoveSM, 'ActionWrapper_Move'),
										transitions={'finished': 'finished', 'failed': 'failed', 'critical_fail': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'Action'})

			# x:90 y:153
			OperatableStateMachine.add('Confirm ',
										_sm_confirm__1,
										transitions={'none_found': 'failed', 'done': 'GetID'},
										autonomy={'none_found': Autonomy.Inherit, 'done': Autonomy.Inherit},
										remapping={'name': 'name', 'distance': 'distance', 'Person': 'Person'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]

	# [/MANUAL_FUNC]
