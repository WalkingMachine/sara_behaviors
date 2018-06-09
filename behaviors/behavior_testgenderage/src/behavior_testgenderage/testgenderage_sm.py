#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_testgenderage')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.TakeImageCamera import TakeImageCamera
from flexbe_states.log_key_state import LogKeyState
from flexbe_states.wait_state import WaitState
from sara_flexbe_states.test_gender_age import TestGenderAge
from sara_flexbe_states.gender_age_recognition import GenderAgeRecognition
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu May 03 2018
@author: Quentin G
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
		# x:499 y:326, x:39 y:319
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:115 y:40
			OperatableStateMachine.add('fromCamera',
										TakeImageCamera(topic="/head_xtion/rgb/image_raw"),
										transitions={'received': 'Gender', 'unavailable': 'waitsmall'},
										autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
										remapping={'image': 'image'})

			# x:240 y:233
			OperatableStateMachine.add('printAgeMin',
										LogKeyState(text="age min {}", severity=Logger.REPORT_HINT),
										transitions={'done': 'printAgeMax'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'ageMin'})

			# x:407 y:204
			OperatableStateMachine.add('printAgeMax',
										LogKeyState(text="age max {}", severity=Logger.REPORT_HINT),
										transitions={'done': 'waitdelay'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'ageMax'})

			# x:307 y:48
			OperatableStateMachine.add('waitdelay',
										WaitState(wait_time=2),
										transitions={'done': 'fromCamera'},
										autonomy={'done': Autonomy.Off})

			# x:5 y:85
			OperatableStateMachine.add('waitsmall',
										WaitState(wait_time=0.5),
										transitions={'done': 'fromCamera'},
										autonomy={'done': Autonomy.Off})

			# x:589 y:130
			OperatableStateMachine.add('test',
										TestGenderAge(),
										transitions={'done': 'test'},
										autonomy={'done': Autonomy.Off},
										remapping={'image': 'image'})

			# x:55 y:177
			OperatableStateMachine.add('Gender',
										GenderAgeRecognition(),
										transitions={'success': 'printAgeMin', 'fail': 'waitdelay'},
										autonomy={'success': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'image': 'image', 'ageMin': 'ageMin', 'ageMax': 'ageMax', 'probAge': 'probAge', 'probMale': 'probMale', 'probFemale': 'probFemale'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
