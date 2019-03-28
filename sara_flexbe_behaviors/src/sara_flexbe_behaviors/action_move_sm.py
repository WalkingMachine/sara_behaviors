#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.sara_set_expression import SetExpression
from sara_flexbe_states.sara_move_base import SaraMoveBase
from sara_flexbe_states.sara_set_head_angle_key import SaraSetHeadAngleKey
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.GetClosestObstacle import GetClosestObstacle
from flexbe_states.check_condition_state import CheckConditionState
from sara_flexbe_states.sara_set_head_angle import SaraSetHeadAngle
from sara_flexbe_states.WonderlandGetEntityVerbal import WonderlandGetEntityVerbal
from sara_flexbe_states.GetAttribute import GetAttribute
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
		# x:860 y:152, x:755 y:568
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['pose'])
		_state_machine.userdata.pose = ["room"]

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
		_sm_move_1 = OperatableStateMachine(outcomes=['arrived', 'failed'], input_keys=['pose'])

		with _sm_move_1:
			# x:95 y:122
			OperatableStateMachine.add('move',
										SaraMoveBase(reference="map"),
										transitions={'arrived': 'arrived', 'failed': 'failed'},
										autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'pose'})


		# x:259 y:573, x:488 y:254, x:509 y:305
		_sm_manage_name_2 = OperatableStateMachine(outcomes=['done', 'too much', 'not found'], input_keys=['pose'], output_keys=['pose', 'name'])

		with _sm_manage_name_2:
			# x:38 y:163
			OperatableStateMachine.add('check if Pose',
										CheckConditionState(predicate=lambda x: type(x) is type([]) or type(x) is type("")),
										transitions={'true': 'getname', 'false': 'done'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'pose'})

			# x:257 y:264
			OperatableStateMachine.add('getcontainers',
										CalculationState(calculation=lambda x: x[1:]),
										transitions={'done': 'get wonderland entity'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'pose', 'output_value': 'containers'})

			# x:232 y:354
			OperatableStateMachine.add('get wonderland entity',
										WonderlandGetEntityVerbal(),
										transitions={'one': 'get waypoint', 'multiple': 'too much', 'none': 'not found', 'error': 'not found'},
										autonomy={'one': Autonomy.Off, 'multiple': Autonomy.Off, 'none': Autonomy.Off, 'error': Autonomy.Off},
										remapping={'name': 'name', 'containers': 'containers', 'entities': 'entities', 'firstEntity': 'firstEntity'})

			# x:238 y:442
			OperatableStateMachine.add('get waypoint',
										GetAttribute(attributes=["waypoint"]),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off},
										remapping={'object': 'firstEntity', 'waypoint': 'pose'})

			# x:256 y:166
			OperatableStateMachine.add('getname',
										CalculationState(calculation=lambda x: x[0]),
										transitions={'done': 'getcontainers'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'pose', 'output_value': 'name'})


		# x:30 y:365, x:130 y:365, x:230 y:365, x:330 y:365, x:430 y:365
		_sm_move_concurent_3 = ConcurrencyContainer(outcomes=['arrived', 'failed'], input_keys=['pose'], conditions=[
										('arrived', [('Move', 'arrived')]),
										('failed', [('Move', 'failed')]),
										('failed', [('Look around', 'failed')])
										])

		with _sm_move_concurent_3:
			# x:30 y:40
			OperatableStateMachine.add('Move',
										_sm_move_1,
										transitions={'arrived': 'arrived', 'failed': 'failed'},
										autonomy={'arrived': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'pose'})

			# x:268 y:74
			OperatableStateMachine.add('Look around',
										_sm_look_around_0,
										transitions={'failed': 'failed'},
										autonomy={'failed': Autonomy.Inherit})



		with _state_machine:
			# x:54 y:27
			OperatableStateMachine.add('SetCount',
										SetKey(Value=2),
										transitions={'done': 'manage name'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Count'})

			# x:258 y:250
			OperatableStateMachine.add('stuck',
										SaraSay(sentence="I'm getting stuck.", input_keys=[], emotion=2, block=True),
										transitions={'done': 'Count--'},
										autonomy={'done': Autonomy.Off})

			# x:49 y:251
			OperatableStateMachine.add('try again',
										SaraSay(sentence="But I'm still going.", input_keys=[], emotion=1, block=False),
										transitions={'done': 'Move concurent'},
										autonomy={'done': Autonomy.Off})

			# x:360 y:508
			OperatableStateMachine.add('sorry',
										SaraSay(sentence="Well. It seem's I can't go there.", input_keys=[], emotion=2, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:672 y:147
			OperatableStateMachine.add('set blink',
										SetExpression(emotion=6, brightness=-1),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:252 y:146
			OperatableStateMachine.add('Move concurent',
										_sm_move_concurent_3,
										transitions={'arrived': 'reset head', 'failed': 'stuck'},
										autonomy={'arrived': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'pose'})

			# x:254 y:353
			OperatableStateMachine.add('Count--',
										CalculationState(calculation=lambda x: x-1),
										transitions={'done': 'check count'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Count', 'output_value': 'Count'})

			# x:37 y:351
			OperatableStateMachine.add('check count',
										CheckConditionState(predicate=lambda x: x>=0),
										transitions={'true': 'try again', 'false': 'sorry'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'Count'})

			# x:497 y:149
			OperatableStateMachine.add('reset head',
										SaraSetHeadAngle(pitch=0.1, yaw=0),
										transitions={'done': 'set blink'},
										autonomy={'done': Autonomy.Off})

			# x:269 y:21
			OperatableStateMachine.add('manage name',
										_sm_manage_name_2,
										transitions={'done': 'set head', 'too much': 'say too much', 'not found': 'say not known'},
										autonomy={'done': Autonomy.Inherit, 'too much': Autonomy.Inherit, 'not found': Autonomy.Inherit},
										remapping={'pose': 'pose', 'name': 'poseName'})

			# x:46 y:147
			OperatableStateMachine.add('set head',
										SaraSetHeadAngle(pitch=0.8, yaw=0),
										transitions={'done': 'Move concurent'},
										autonomy={'done': Autonomy.Off})

			# x:477 y:333
			OperatableStateMachine.add('say too much',
										SaraSay(sentence=lambda x: "There is more than one "+x[0]+".", input_keys=["poseName"], emotion=3, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off},
										remapping={'poseName': 'poseName'})

			# x:445 y:418
			OperatableStateMachine.add('say not known',
										SaraSay(sentence=lambda x: "I don't know where the "+x[0]+" is.", input_keys=["poseName"], emotion=0, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off},
										remapping={'poseName': 'poseName'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
