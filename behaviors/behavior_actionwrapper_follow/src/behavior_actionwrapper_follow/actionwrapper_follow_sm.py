#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_actionwrapper_follow')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.check_condition_state import CheckConditionState
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.sara_say_key import SaraSayKey
from sara_flexbe_states.follow_client import FollowClient
from sara_flexbe_states.for_loop import ForLoop
from sara_flexbe_states.get_speech import GetSpeech
from sara_flexbe_states.regex_tester import RegexTester
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Tue Jul 11 2017
@author: Philippe La Madeleine
'''
class ActionWrapper_FollowSM(Behavior):
	'''
	action wrapper pour follow
	'''


	def __init__(self):
		super(ActionWrapper_FollowSM, self).__init__()
		self.name = 'ActionWrapper_Follow'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
        
        # [/MANUAL_INIT]

		# Behavior comments:

		# O 295 30 
		# Follow|n1- person|n2- area where the person is|n3- path (unused)



	def create(self):
		# x:683 y:657, x:891 y:463
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['Action'])
		_state_machine.userdata.Action = ["Follow", "you", "", ""]

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


		with _state_machine:
			# x:42 y:117
			OperatableStateMachine.add('cond',
										CheckConditionState(predicate=lambda x: x[1] != ''),
										transitions={'true': 'cond2', 'false': 'stand'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'Action'})

			# x:44 y:437
			OperatableStateMachine.add('say follow you',
										SaraSay(sentence="I'm following you", emotion=1, block=True),
										transitions={'done': 'stand'},
										autonomy={'done': Autonomy.Off})

			# x:43 y:579
			OperatableStateMachine.add('say follow person in area',
										SaraSayKey(Format=lambda x: "I'm going to follow "+ x[1], emotion=1, block=True),
										transitions={'done': 'stand'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'Action'})

			# x:41 y:503
			OperatableStateMachine.add('say follow person',
										SaraSayKey(Format=lambda x: "I'm going to follow "+x, emotion=1, block=True),
										transitions={'done': 'stand'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'Action'})

			# x:36 y:263
			OperatableStateMachine.add('cond2',
										CheckConditionState(predicate=lambda x: x[2] != ''),
										transitions={'true': 'stand', 'false': 'stand'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'Action'})

			# x:418 y:216
			OperatableStateMachine.add('start',
										FollowClient(command=1),
										transitions={'done': 'follow', 'fail': 'for'},
										autonomy={'done': Autonomy.Off, 'fail': Autonomy.Off})

			# x:304 y:280
			OperatableStateMachine.add('stand',
										SaraSay(sentence="Ok, Please stand in front of me so I can identify you", emotion=1, block=True),
										transitions={'done': 'start'},
										autonomy={'done': Autonomy.Off})

			# x:559 y:198
			OperatableStateMachine.add('follow',
										FollowClient(command=2),
										transitions={'done': 'say follow', 'fail': 'for'},
										autonomy={'done': Autonomy.Off, 'fail': Autonomy.Off})

			# x:425 y:442
			OperatableStateMachine.add('for',
										ForLoop(repeat=1),
										transitions={'do': 'wait', 'end': 'say fail'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index'})

			# x:679 y:255
			OperatableStateMachine.add('say follow',
										SaraSay(sentence="I'm now following you. Please tell me when we arrive.", emotion=1, block=True),
										transitions={'done': 'get speech'},
										autonomy={'done': Autonomy.Off})

			# x:297 y:365
			OperatableStateMachine.add('wait',
										SaraSay(sentence="This is harder than it looks like. Please wait a bit longer.", emotion=1, block=True),
										transitions={'done': 'start'},
										autonomy={'done': Autonomy.Off})

			# x:674 y:353
			OperatableStateMachine.add('get speech',
										GetSpeech(watchdog=100),
										transitions={'done': 'test', 'nothing': 'get speech', 'fail': 'failed'},
										autonomy={'done': Autonomy.Off, 'nothing': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'words': 'words'})

			# x:676 y:434
			OperatableStateMachine.add('test',
										RegexTester(regex=".*((here)|(done)|(arrived)|(halt)|(finish)).*"),
										transitions={'true': 'stop1', 'false': 'get speech'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'text': 'words', 'result': 'result'})

			# x:808 y:512
			OperatableStateMachine.add('stop1',
										FollowClient(command=3),
										transitions={'done': 'stop2', 'fail': 'failed'},
										autonomy={'done': Autonomy.Off, 'fail': Autonomy.Off})

			# x:811 y:568
			OperatableStateMachine.add('stop2',
										FollowClient(command=4),
										transitions={'done': 'say good', 'fail': 'failed'},
										autonomy={'done': Autonomy.Off, 'fail': Autonomy.Off})

			# x:650 y:553
			OperatableStateMachine.add('say good',
										SaraSay(sentence="good", emotion=1, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:454 y:641
			OperatableStateMachine.add('say fail',
										SaraSay(sentence="Sorry, I failed to follow you", emotion=1, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
