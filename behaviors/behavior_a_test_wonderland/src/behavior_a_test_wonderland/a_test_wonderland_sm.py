#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_a_test_wonderland')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, Logger
from flexbe_states.log_state import LogState
from sara_flexbe_states.WonderlandGetEntityVerbal import WonderlandGetEntityVerbal
from sara_flexbe_states.LogEntity import LogEntity
from sara_flexbe_states.WonderlandGetPersonById import WonderlandGetPersonById
from sara_flexbe_states.WonderlandGetEntityByID import WonderlandGetEntityByID
from sara_flexbe_states.WonderlandGetPersonByRecognitionId import WonderlandGetPersonByRecognitionId
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Jul 17 2017
@author: Lucas
'''
class A_TEST_WONDERLANDSM(Behavior):
	'''
	sfdf
	'''


	def __init__(self):
		super(A_TEST_WONDERLANDSM, self).__init__()
		self.name = 'A_TEST_WONDERLAND'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1157 y:92
		_state_machine = OperatableStateMachine(outcomes=['finished'],
												input_keys=['name', 'containers', 'id', 'faceId'])
		_state_machine.userdata.name = "apple"
		_state_machine.userdata.containers = ["dining", "tray"]
		_state_machine.userdata.id = 2
		_state_machine.userdata.faceId = 45

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:36 y:233
			OperatableStateMachine.add('LogState',
									   LogState(text="RUNING", severity=Logger.REPORT_HINT),
									   transitions={'done': 'WonderlandGetPersonByRecognitionId'},
									   autonomy={'done': Autonomy.Off})

			# x:333 y:72
			OperatableStateMachine.add('WonderlandGetEntityVerbal',
									   WonderlandGetEntityVerbal(),
									   transitions={'one': 'one', 'multiple': 'multiple', 'none': 'none',
													'error': 'error'},
									   autonomy={'one': Autonomy.Off, 'multiple': Autonomy.Off, 'none': Autonomy.Off,
												 'error': Autonomy.Off},
									   remapping={'name': 'name', 'containers': 'containers', 'entities': 'entities'})

			# x:718 y:115
			OperatableStateMachine.add('one',
									   LogState(text="One entity found.", severity=Logger.REPORT_HINT),
									   transitions={'done': 'LogEntity'},
									   autonomy={'done': Autonomy.Off})

			# x:718 y:165
			OperatableStateMachine.add('multiple',
									   LogState(text="Multiple entity found.", severity=Logger.REPORT_HINT),
									   transitions={'done': 'LogEntity'},
										autonomy={'done': Autonomy.Off})

			# x:717 y:63
			OperatableStateMachine.add('none',
									   LogState(text="None entity found.", severity=Logger.REPORT_HINT),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:717 y:11
			OperatableStateMachine.add('error',
									   LogState(text="Error in Wonderland.", severity=Logger.REPORT_HINT),
									   transitions={'done': 'finished'},
									   autonomy={'done': Autonomy.Off})

			# x:902 y:149
			OperatableStateMachine.add('LogEntity',
									   LogEntity(),
									   transitions={'done': 'finished'},
									   autonomy={'done': Autonomy.Off},
									   remapping={'entity': 'entities'})

			# x:335 y:123
			OperatableStateMachine.add('WonderlandGetPersonById',
									   WonderlandGetPersonById(),
									   transitions={'done': 'one', 'none': 'none', 'error': 'error'},
									   autonomy={'done': Autonomy.Off, 'none': Autonomy.Off, 'error': Autonomy.Off},
									   remapping={'id': 'id', 'entity': 'entities'})

			# x:339 y:19
			OperatableStateMachine.add('WonderlandGetEntityByID',
									   WonderlandGetEntityByID(),
									   transitions={'found': 'one', 'not_found': 'none', 'error': 'error'},
									   autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off,
												 'error': Autonomy.Off},
									   remapping={'id': 'id', 'entity': 'entities', 'depth_position': 'depth_position',
												  'depth_waypoint': 'depth_waypoint'})

			# x:311 y:177
			OperatableStateMachine.add('WonderlandGetPersonByRecognitionId',
									   WonderlandGetPersonByRecognitionId(),
									   transitions={'done': 'one', 'none': 'none', 'error': 'error'},
									   autonomy={'done': Autonomy.Off, 'none': Autonomy.Off, 'error': Autonomy.Off},
									   remapping={'id': 'faceId', 'entity': 'entities'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
