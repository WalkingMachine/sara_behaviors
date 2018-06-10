#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_action_move')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.sara_set_head_angle import SaraSetHeadAngle
from sara_flexbe_states.for_loop import ForLoop
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.sara_set_expression import SetExpression
from flexbe_states.check_condition_state import CheckConditionState
from sara_flexbe_states.sara_rel_move_base import SaraRelMoveBase
from sara_flexbe_states.sara_move_base import SaraMoveBase
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Tue Oct 24 2017
@author: Philippe La Madeleine
'''
class Action_MoveSM(Behavior):
	'''
	Move Sara to a specific point.
	'''


	def __init__(self):
		super(Action_MoveSM, self).__init__()
		self.name = 'Action_Move'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
        
        # [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:765 y:155, x:767 y:456
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['pose', 'relative'])
		_state_machine.userdata.pose = 0
		_state_machine.userdata.relative = False

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

		# x:566 y:38, x:553 y:248
		_sm_move_0 = OperatableStateMachine(outcomes=['arrived', 'failed'], input_keys=['relative', 'pose'])

		with _sm_move_0:
			# x:40 y:24
			OperatableStateMachine.add('check rel',
										CheckConditionState(predicate=lambda x: x==True),
										transitions={'true': 'rel move', 'false': 'move'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'relative'})

			# x:230 y:177
			OperatableStateMachine.add('rel move',
										SaraRelMoveBase(),
										transitions={'arrived': 'arrived', 'failed': 'failed'},
										autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'pose'})

			# x:249 y:28
			OperatableStateMachine.add('move',
										SaraMoveBase(),
										transitions={'arrived': 'arrived', 'failed': 'failed'},
										autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'pose'})



		with _state_machine:
			# x:46 y:147
			OperatableStateMachine.add('set head',
										SaraSetHeadAngle(pitch=0.9, yaw=0),
										transitions={'done': 'Move'},
										autonomy={'done': Autonomy.Off})

			# x:271 y:449
			OperatableStateMachine.add('for',
										ForLoop(repeat=1),
										transitions={'do': 'set straight face', 'end': 'sorry'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index'})

			# x:271 y:347
			OperatableStateMachine.add('stuck',
										SaraSay(sentence="Hum, look's like I'm stuck.", emotion=1, block=True),
										transitions={'done': 'for'},
										autonomy={'done': Autonomy.Off})

			# x:58 y:339
			OperatableStateMachine.add('try again',
										SaraSay(sentence="Let me try again", emotion=1, block=True),
										transitions={'done': 'set head'},
										autonomy={'done': Autonomy.Off})

			# x:585 y:448
			OperatableStateMachine.add('sorry',
										SaraSay(sentence="Well. It seem's I can't go there.", emotion=1, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:260 y:250
			OperatableStateMachine.add('set sad face',
										SetExpression(emotion=2, brightness=-1),
										transitions={'done': 'stuck'},
										autonomy={'done': Autonomy.Off})

			# x:50 y:447
			OperatableStateMachine.add('set straight face',
										SetExpression(emotion=3, brightness=-1),
										transitions={'done': 'try again'},
										autonomy={'done': Autonomy.Off})

			# x:450 y:150
			OperatableStateMachine.add('set blink',
										SetExpression(emotion=6, brightness=-1),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:252 y:146
			OperatableStateMachine.add('Move',
										_sm_move_0,
										transitions={'arrived': 'set blink', 'failed': 'set sad face'},
										autonomy={'arrived': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'relative': 'relative', 'pose': 'pose'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
