#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_test_look_at_sound')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.Look_at_sound import LookAtSound
from sara_flexbe_states.get_speech import GetSpeech
from flexbe_states.wait_state import WaitState
from sara_flexbe_states.regex_tester import RegexTester
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Fri Oct 26 2018
@author: Jeffrey
'''
class test_look_at_soundSM(Behavior):
	'''
	test look at sound
	'''


	def __init__(self):
		super(test_look_at_soundSM, self).__init__()
		self.name = 'test_look_at_sound'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:310 y:409, x:130 y:365
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:17 y:314
		_sm_group_0 = OperatableStateMachine(outcomes=['done'], output_keys=['Words'])

		with _sm_group_0:
			# x:84 y:76
			OperatableStateMachine.add('speech',
										GetSpeech(watchdog=8),
										transitions={'done': 'wait', 'nothing': 'speech', 'fail': 'speech'},
										autonomy={'done': Autonomy.Off, 'nothing': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'words': 'Words'})

			# x:92 y:221
			OperatableStateMachine.add('wait',
										WaitState(wait_time=1),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off})


		# x:30 y:365
		_sm_group_2_1 = OperatableStateMachine(outcomes=['done'])

		with _sm_group_2_1:
			# x:32 y:131
			OperatableStateMachine.add('test_sound',
										LookAtSound(),
										transitions={'done': 'test_sound'},
										autonomy={'done': Autonomy.Off})


		# x:30 y:365, x:337 y:100, x:230 y:365
		_sm_look_and_wait_2 = ConcurrencyContainer(outcomes=['done'], output_keys=['Words'], conditions=[
										('done', [('Group', 'done')]),
										('done', [('Group_2', 'done')])
										])

		with _sm_look_and_wait_2:
			# x:75 y:82
			OperatableStateMachine.add('Group_2',
										_sm_group_2_1,
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Inherit})

			# x:28 y:173
			OperatableStateMachine.add('Group',
										_sm_group_0,
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Inherit},
										remapping={'Words': 'Words'})



		with _state_machine:
			# x:60 y:65
			OperatableStateMachine.add('say marco!',
										SaraSay(sentence="Marco?", emotion=1, block=True),
										transitions={'done': 'Look and wait'},
										autonomy={'done': Autonomy.Off})

			# x:335 y:191
			OperatableStateMachine.add('Look and wait',
										_sm_look_and_wait_2,
										transitions={'done': 'is polo!'},
										autonomy={'done': Autonomy.Inherit},
										remapping={'Words': 'Words'})

			# x:281 y:85
			OperatableStateMachine.add('hey',
										SaraSay(sentence="Hey! You need to say polo!", emotion=1, block=True),
										transitions={'done': 'say marco!'},
										autonomy={'done': Autonomy.Off})

			# x:520 y:36
			OperatableStateMachine.add('is polo!',
										RegexTester(regex="[^o]*o[^o\ ]*o[^o]*"),
										transitions={'true': 'say marco!', 'false': 'hey'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'text': 'Words', 'result': 'result'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
