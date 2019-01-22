#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_action_move')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.sara_set_expression import SetExpression
from flexbe_states.check_condition_state import CheckConditionState
from sara_flexbe_states.sara_rel_move_base import SaraRelMoveBase
from sara_flexbe_states.sara_move_base import SaraMoveBase
from sara_flexbe_states.sara_set_head_angle_key import SaraSetHeadAngleKey
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.GetClosestObstacle import GetClosestObstacle
from sara_flexbe_states.sara_set_head_angle import SaraSetHeadAngle
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
		# x:765 y:155, x:755 y:568
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['pose', 'relative'])
		_state_machine.userdata.pose = 0
		_state_machine.userdata.relative = False

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

		# x:130 y:365
		_sm_look_around_0 = OperatableStateMachine(outcomes=['failed'])

		with _sm_look_around_0:
			# x:78 y:40
			OperatableStateMachine.add('set pitch',
										SetKey(Value=0.9),
										transitions={'done': 'get angle'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'pitch'})

			# x:348 y:210
			OperatableStateMachine.add('set head',
										SaraSetHeadAngleKey(),
										transitions={'done': 'get angle'},
										autonomy={'done': Autonomy.Off},
										remapping={'yaw': 'yaw', 'pitch': 'pitch'})

			# x:204 y:248
			OperatableStateMachine.add('limit yaw',
										CalculationState(calculation=lambda x: max(min(x,1), -1)),
										transitions={'done': 'set head'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'yaw', 'output_value': 'yaw'})

			# x:191 y:126
			OperatableStateMachine.add('get angle',
										GetClosestObstacle(topic="/scan", maximumDistance=2),
										transitions={'done': 'limit yaw'},
										autonomy={'done': Autonomy.Off},
										remapping={'Angle': 'yaw'})


		# x:30 y:365, x:130 y:365
		_sm_move_1 = OperatableStateMachine(outcomes=['arrived', 'failed'], input_keys=['relative', 'pose'])

		with _sm_move_1:
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


		# x:30 y:365, x:130 y:365, x:230 y:365, x:330 y:365, x:430 y:365
		_sm_move_concurent_2 = ConcurrencyContainer(outcomes=['arrived', 'failed'], input_keys=['relative', 'pose'], conditions=[
										('arrived', [('Move', 'arrived')]),
										('failed', [('Move', 'failed')]),
										('failed', [('Look around', 'failed')])
										])

		with _sm_move_concurent_2:
			# x:30 y:40
			OperatableStateMachine.add('Move',
										_sm_move_1,
										transitions={'arrived': 'arrived', 'failed': 'failed'},
										autonomy={'arrived': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'relative': 'relative', 'pose': 'pose'})

			# x:268 y:74
			OperatableStateMachine.add('Look around',
										_sm_look_around_0,
										transitions={'failed': 'failed'},
										autonomy={'failed': Autonomy.Inherit})



		with _state_machine:
			# x:54 y:27
			OperatableStateMachine.add('SetCount',
										SetKey(Value=2),
										transitions={'done': 'set head'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Count'})

			# x:271 y:347
			OperatableStateMachine.add('stuck',
										SaraSay(sentence="I'm getting stuck.", emotion=1, block=True),
										transitions={'done': 'Count--'},
										autonomy={'done': Autonomy.Off})

			# x:58 y:339
			OperatableStateMachine.add('try again',
										SaraSay(sentence="But I'm still going.", emotion=1, block=False),
										transitions={'done': 'set head'},
										autonomy={'done': Autonomy.Off})

			# x:582 y:558
			OperatableStateMachine.add('sorry',
										SaraSay(sentence="Well. It seem's I can't go there.", emotion=1, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:260 y:250
			OperatableStateMachine.add('set sad face',
										SetExpression(emotion=2, brightness=-1),
										transitions={'done': 'stuck'},
										autonomy={'done': Autonomy.Off})

			# x:39 y:568
			OperatableStateMachine.add('set straight face',
										SetExpression(emotion=3, brightness=-1),
										transitions={'done': 'try again'},
										autonomy={'done': Autonomy.Off})

			# x:583 y:147
			OperatableStateMachine.add('set blink',
										SetExpression(emotion=6, brightness=-1),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:252 y:146
			OperatableStateMachine.add('Move concurent',
										_sm_move_concurent_2,
										transitions={'arrived': 'reset head', 'failed': 'set sad face'},
										autonomy={'arrived': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'relative': 'relative', 'pose': 'pose'})

			# x:261 y:471
			OperatableStateMachine.add('Count--',
										CalculationState(calculation=lambda x: x-1),
										transitions={'done': 'check count'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Count', 'output_value': 'Count'})

			# x:253 y:569
			OperatableStateMachine.add('check count',
										CheckConditionState(predicate=lambda x: x>=0),
										transitions={'true': 'set straight face', 'false': 'sorry'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'Count'})

			# x:46 y:147
			OperatableStateMachine.add('set head',
										SaraSetHeadAngle(pitch=-0.9, yaw=0),
										transitions={'done': 'Move concurent'},
										autonomy={'done': Autonomy.Off})

			# x:425 y:143
			OperatableStateMachine.add('reset head',
										SaraSetHeadAngle(pitch=0.1, yaw=0),
										transitions={'done': 'set blink'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
