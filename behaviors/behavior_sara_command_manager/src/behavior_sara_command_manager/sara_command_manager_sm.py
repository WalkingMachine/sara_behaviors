#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_sara_command_manager')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.get_speech import GetSpeech
from sara_flexbe_states.lu4r_parser import LU4R_Parser
from sara_flexbe_states.sara_say import SaraSay
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Tue Jul 11 2017
@author: Philippe La Madeleine
'''
class sara_command_managerSM(Behavior):
	'''
	the command manager of Sara
	'''


	def __init__(self):
		super(sara_command_managerSM, self).__init__()
		self.name = 'sara_command_manager'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
        
        # [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:857 y:132, x:440 y:368
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['HighFIFO', 'MedFIFO', 'LowFIFO', 'DoNow'])
		_state_machine.userdata.HighFIFO = []
		_state_machine.userdata.MedFIFO = []
		_state_machine.userdata.LowFIFO = []
		_state_machine.userdata.DoNow = []
		_state_machine.userdata.Default_message = ""

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


		with _state_machine:
			# x:156 y:80
			OperatableStateMachine.add('get speech',
										GetSpeech(watchdog=5),
										transitions={'done': 'parse text', 'nothing': 'get speech', 'fail': 'failed'},
										autonomy={'done': Autonomy.Off, 'nothing': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'words': 'sentence'})

			# x:378 y:40
			OperatableStateMachine.add('parse text',
										LU4R_Parser(),
										transitions={'done': 'understood', 'fail': 'sorry'},
										autonomy={'done': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'sentence': 'sentence', 'HighFIFO': 'HighFIFO', 'MedFIFO': 'MedFIFO', 'LowFIFO': 'LowFIFO', 'DoNow': 'DoNow'})

			# x:579 y:41
			OperatableStateMachine.add('understood',
										SaraSay(sentence="Understood", emotion=1, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:404 y:211
			OperatableStateMachine.add('sorry',
										SaraSay(sentence="Sorry, I did not understand. Could you repeat please?", emotion=1, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
