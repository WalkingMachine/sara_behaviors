#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_presentation_robotique_zone_1')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.list_entities_by_name import list_entities_by_name
from flexbe_states.flexible_calculation_state import FlexibleCalculationState
from flexbe_states.wait_state import WaitState
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.KeepLookingAt import KeepLookingAt
from sara_flexbe_states.GetClosestObstacle import GetClosestObstacle
from sara_flexbe_states.sara_set_head_angle_key import SaraSetHeadAngleKey
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Fri Jul 06 2018
@author: Philippe La Madeleine
'''
class Presentation_Robotique_Zone_1SM(Behavior):
	'''
	Presentation_Robotique_Zone_1
	'''


	def __init__(self):
		super(Presentation_Robotique_Zone_1SM, self).__init__()
		self.name = 'Presentation_Robotique_Zone_1'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:89 y:539, x:30 y:533
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.pitch = 0.5
		_state_machine.userdata.SoftAngle = 0
		_state_machine.userdata.name = "person"

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:321 y:320, x:130 y:365, x:473 y:343
		_sm_group_0 = ConcurrencyContainer(outcomes=['failed'], input_keys=['ID'], conditions=[
										('failed', [('3', 'done')]),
										('failed', [('KeepLookingAt', 'failed')])
										])

		with _sm_group_0:
			# x:29 y:99
			OperatableStateMachine.add('KeepLookingAt',
										KeepLookingAt(),
										transitions={'failed': 'failed'},
										autonomy={'failed': Autonomy.Off},
										remapping={'ID': 'ID'})

			# x:270 y:110
			OperatableStateMachine.add('3',
										WaitState(wait_time=1),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})



		with _state_machine:
			# x:149 y:295
			OperatableStateMachine.add('get entities',
										list_entities_by_name(frontality_level=0, distance_max=2),
										transitions={'found': 'get closest', 'not_found': 'get entities'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'name': 'name', 'entity_list': 'entity_list', 'number': 'number'})

			# x:309 y:44
			OperatableStateMachine.add('processAngle',
										FlexibleCalculationState(calculation=lambda x: x[1]+(max(min(x[0],1), -1)-x[1])/10, input_keys=["Angle", "SoftAngle"]),
										transitions={'done': 'SaraSetHeadAngleKey'},
										autonomy={'done': Autonomy.Off},
										remapping={'Angle': 'Angle', 'SoftAngle': 'SoftAngle', 'output_value': 'SoftAngle'})

			# x:230 y:202
			OperatableStateMachine.add('WaitState',
										WaitState(wait_time=2),
										transitions={'done': 'GetClosestObstacle'},
										autonomy={'done': Autonomy.Off})

			# x:406 y:308
			OperatableStateMachine.add('get closest',
										CalculationState(calculation=lambda x: x[0].ID),
										transitions={'done': 'Group'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'entity_list', 'output_value': 'ID'})

			# x:301 y:445
			OperatableStateMachine.add('Group',
										_sm_group_0,
										transitions={'failed': 'get entities'},
										autonomy={'failed': Autonomy.Inherit},
										remapping={'ID': 'ID'})

			# x:77 y:112
			OperatableStateMachine.add('GetClosestObstacle',
										GetClosestObstacle(topic="/scan", maximumDistance=2),
										transitions={'done': 'processAngle'},
										autonomy={'done': Autonomy.Off},
										remapping={'Angle': 'Angle'})

			# x:155 y:409
			OperatableStateMachine.add('wait1',
										WaitState(wait_time=3),
										transitions={'done': 'get entities'},
										autonomy={'done': Autonomy.Off})

			# x:389 y:162
			OperatableStateMachine.add('SaraSetHeadAngleKey',
										SaraSetHeadAngleKey(),
										transitions={'done': 'WaitState'},
										autonomy={'done': Autonomy.Off},
										remapping={'yaw': 'Angle', 'pitch': 'pitch'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
