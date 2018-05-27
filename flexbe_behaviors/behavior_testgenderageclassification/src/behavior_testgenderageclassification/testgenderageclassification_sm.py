#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_testgenderageclassification')
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
class TestGenderAgeClassificationSM(Behavior):
	'''
	TestGenderAgeClassification
	'''


	def __init__(self):
		super(TestGenderAgeClassificationSM, self).__init__()
		self.name = 'TestGenderAgeClassification'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:30 y:365, x:130 y:365
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:30 y:40
			OperatableStateMachine.add('test',
										TestGenderAge(Format=1, emotion=2, block=True),
										transitions={'done': 'gender'},
										autonomy={'done': Autonomy.Off},
										remapping={'image': 'image'})

			# x:30 y:110
			OperatableStateMachine.add('gender',
										GenderAgeRecognition(Format=0, emotion=1, block=True),
										transitions={'success': 'print', 'fail': 'failed'},
										autonomy={'success': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'image': 'image', 'ageMin': 'ageMin', 'ageMax': 'ageMax', 'probAge': 'probAge', 'probMale': 'probMale', 'probFemale': 'probFemale'})

			# x:23 y:252
			OperatableStateMachine.add('print',
										LogKeyState(text="{}", severity=1),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'probMale'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
