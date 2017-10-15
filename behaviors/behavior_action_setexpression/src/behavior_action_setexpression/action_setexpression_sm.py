#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_action_setexpression')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.sara_start_face import StartFace
from sara_flexbe_states.uint8_topic_publisher import PublishUint8
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed Jul 19 2017
@author: Redouane Laref
'''
class Action_SetExpressionSM(Behavior):
	'''
	State qui change la couleur des expressions de SARA.
	'''


	def __init__(self):
		super(Action_SetExpressionSM, self).__init__()
		self.name = 'Action_SetExpression'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:559 y:334, x:393 y:345
		_state_machine = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['emotion', 'brightness'])
		_state_machine.userdata.emotion = ""
		_state_machine.userdata.brightness = 255
		_state_machine.userdata.topic_emotion = "sara_face/Emotion"
		_state_machine.userdata.topic_brightness = "sara_face/Brightness"

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:187 y:93
			OperatableStateMachine.add('start face',
										StartFace(),
										transitions={'done': 'publish emotion', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

			# x:482 y:103
			OperatableStateMachine.add('publish emotion',
										PublishUint8(),
										transitions={'done': 'publish brightness'},
										autonomy={'done': Autonomy.Off},
										remapping={'topic': 'topic_emotion', 'data': 'emotion'})

			# x:645 y:197
			OperatableStateMachine.add('publish brightness',
										PublishUint8(),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off},
										remapping={'topic': 'topic_emotion', 'data': 'brightness'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
