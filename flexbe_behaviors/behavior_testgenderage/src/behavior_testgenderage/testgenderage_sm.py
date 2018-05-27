#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_testgenderage')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.test_gender_age import TestGenderAge
from sara_flexbe_states.gender_age_recognition import GenderAgeRecognition
from flexbe_states.log_key_state import LogKeyState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu May 03 2018
@author: Quentin
'''
class testGenderAgeSM(Behavior):
	'''
	testGenderAge
	'''


	def __init__(self):
		super(testGenderAgeSM, self).__init__()
		self.name = 'testGenderAge'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:188 y:379, x:39 y:319
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:41 y:70
			OperatableStateMachine.add('test',
										TestGenderAge(),
										transitions={'done': 'Gender'},
										autonomy={'done': Autonomy.Off},
										remapping={'image': 'image'})

			# x:44 y:173
			OperatableStateMachine.add('Gender',
										GenderAgeRecognition(),
										transitions={'success': 'print', 'fail': 'failed'},
										autonomy={'success': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'image': 'image', 'ageMin': 'ageMin', 'ageMax': 'ageMax', 'probAge': 'probAge', 'probMale': 'probMale', 'probFemale': 'probFemale'})

			# x:140 y:285
			OperatableStateMachine.add('print',
										LogKeyState(text="{}", severity=Logger.REPORT_HINT),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'probMale'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
