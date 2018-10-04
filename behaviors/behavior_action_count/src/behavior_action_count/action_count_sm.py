#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_action_count')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.SetKey import SetKey
from flexbe_states.log_key_state import LogKeyState
from sara_flexbe_states.sara_set_head_angle import SaraSetHeadAngle
from sara_flexbe_states.list_entities_by_name import list_entities_by_name
from flexbe_states.flexible_calculation_state import FlexibleCalculationState
from flexbe_states.wait_state import WaitState
from sara_flexbe_states.sara_say_key import SaraSayKey
from sara_flexbe_states.for_loop import ForLoop
from behavior_action_turn.action_turn_sm import action_turnSM
from sara_flexbe_states.SetRosParam import SetRosParam
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sat Jun 1 2018
@author: Raphael Duchaine
'''
class Action_countSM(Behavior):
	'''
	Count instances of entity class around sara (will only rotate, won't move).
	'''


	def __init__(self):
		super(Action_countSM, self).__init__()
		self.name = 'Action_count'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(action_turnSM, 'action_turn')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
        
        # [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:475 y:412, x:73 y:374
		_state_machine = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['className'], output_keys=['Count'])
		_state_machine.userdata.className = "bottle"
		_state_machine.userdata.Count = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

		# x:687 y:347
		_sm_move_head_0 = OperatableStateMachine(outcomes=['finished'], input_keys=['className', 'Count'], output_keys=['Count'])

		with _sm_move_head_0:
			# x:19 y:95
			OperatableStateMachine.add('set left',
										SaraSetHeadAngle(pitch=-0.6, yaw=1.2),
										transitions={'done': 'wait1'},
										autonomy={'done': Autonomy.Off})

			# x:5 y:229
			OperatableStateMachine.add('count',
										list_entities_by_name(frontality_level=0, distance_max=2),
										transitions={'found': 'add', 'none_found': 'add'},
										autonomy={'found': Autonomy.Off, 'none_found': Autonomy.Off},
										remapping={'name': 'className', 'entity_list': 'entity_list', 'number': 'number'})

			# x:10 y:326
			OperatableStateMachine.add('add',
										FlexibleCalculationState(calculation=lambda x: x[0]+x[1], input_keys=["Count", "number"]),
										transitions={'done': 'gen text'},
										autonomy={'done': Autonomy.Off},
										remapping={'Count': 'Count', 'number': 'number', 'output_value': 'Count'})

			# x:241 y:88
			OperatableStateMachine.add('set center',
										SaraSetHeadAngle(pitch=-0.6, yaw=0),
										transitions={'done': 'wait 2'},
										autonomy={'done': Autonomy.Off})

			# x:266 y:154
			OperatableStateMachine.add('wait 2',
										WaitState(wait_time=10),
										transitions={'done': 'count2'},
										autonomy={'done': Autonomy.Off})

			# x:245 y:224
			OperatableStateMachine.add('count2',
										list_entities_by_name(frontality_level=0, distance_max=2),
										transitions={'found': 'add2', 'none_found': 'add2'},
										autonomy={'found': Autonomy.Off, 'none_found': Autonomy.Off},
										remapping={'name': 'className', 'entity_list': 'entity_list', 'number': 'number'})

			# x:252 y:321
			OperatableStateMachine.add('add2',
										FlexibleCalculationState(calculation=lambda x: x[0]+x[1], input_keys=["Count", "number"]),
										transitions={'done': 'geb text 2'},
										autonomy={'done': Autonomy.Off},
										remapping={'Count': 'Count', 'number': 'number', 'output_value': 'Count'})

			# x:24 y:162
			OperatableStateMachine.add('wait1',
										WaitState(wait_time=12),
										transitions={'done': 'count'},
										autonomy={'done': Autonomy.Off})

			# x:445 y:90
			OperatableStateMachine.add('set right',
										SaraSetHeadAngle(pitch=-0.6, yaw=-1.2),
										transitions={'done': 'wait 3'},
										autonomy={'done': Autonomy.Off})

			# x:464 y:164
			OperatableStateMachine.add('wait 3',
										WaitState(wait_time=10),
										transitions={'done': 'count3'},
										autonomy={'done': Autonomy.Off})

			# x:443 y:237
			OperatableStateMachine.add('count3',
										list_entities_by_name(frontality_level=0, distance_max=2),
										transitions={'found': 'add3', 'none_found': 'add3'},
										autonomy={'found': Autonomy.Off, 'none_found': Autonomy.Off},
										remapping={'name': 'className', 'entity_list': 'entity_list', 'number': 'number'})

			# x:457 y:334
			OperatableStateMachine.add('add3',
										FlexibleCalculationState(calculation=lambda x: x[0]+x[1], input_keys=["Count", "number"]),
										transitions={'done': 'gen text3'},
										autonomy={'done': Autonomy.Off},
										remapping={'Count': 'Count', 'number': 'number', 'output_value': 'Count'})

			# x:70 y:497
			OperatableStateMachine.add('say1',
										SaraSayKey(Format=lambda x: x, emotion=1, block=False),
										transitions={'done': 'set center'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'text'})

			# x:30 y:412
			OperatableStateMachine.add('gen text',
										FlexibleCalculationState(calculation=lambda x: "I see "+ str(x[0])+ " "+ str(x[1]), input_keys=["number", "classname"]),
										transitions={'done': 'say1'},
										autonomy={'done': Autonomy.Off},
										remapping={'number': 'number', 'classname': 'className', 'output_value': 'text'})

			# x:253 y:392
			OperatableStateMachine.add('geb text 2',
										FlexibleCalculationState(calculation=lambda x: "I see "+ str(x[0])+ " "+ str(x[1]), input_keys=["number", "classname"]),
										transitions={'done': 'say2'},
										autonomy={'done': Autonomy.Off},
										remapping={'number': 'number', 'classname': 'className', 'output_value': 'text'})

			# x:282 y:480
			OperatableStateMachine.add('say2',
										SaraSayKey(Format=lambda x: x, emotion=1, block=False),
										transitions={'done': 'set right'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'text'})

			# x:461 y:405
			OperatableStateMachine.add('gen text3',
										FlexibleCalculationState(calculation=lambda x: "I see "+ str(x[0])+ " "+ str(x[1]), input_keys=["number", "classname"]),
										transitions={'done': 'say 3'},
										autonomy={'done': Autonomy.Off},
										remapping={'number': 'number', 'classname': 'className', 'output_value': 'text'})

			# x:499 y:479
			OperatableStateMachine.add('say 3',
										SaraSayKey(Format=lambda x: x, emotion=1, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'text'})



		with _state_machine:
			# x:55 y:34
			OperatableStateMachine.add('init count',
										SetKey(Value=0),
										transitions={'done': 'set angle'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Count'})

			# x:444 y:326
			OperatableStateMachine.add('Log Count',
										LogKeyState(text="Found: {} objects", severity=Logger.REPORT_HINT),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'Count'})

			# x:40 y:183
			OperatableStateMachine.add('Move head',
										_sm_move_head_0,
										transitions={'finished': 'for 1'},
										autonomy={'finished': Autonomy.Inherit},
										remapping={'className': 'className', 'Count': 'Count'})

			# x:419 y:254
			OperatableStateMachine.add('Look Center Found',
										SaraSetHeadAngle(pitch=-0.4, yaw=0),
										transitions={'done': 'Log Count'},
										autonomy={'done': Autonomy.Off})

			# x:234 y:227
			OperatableStateMachine.add('for 1',
										ForLoop(repeat=0),
										transitions={'do': 'action_turn', 'end': 'Log Count'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index'})

			# x:38 y:275
			OperatableStateMachine.add('action_turn',
										self.use_behavior(action_turnSM, 'action_turn'),
										transitions={'finished': 'Move head', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'rotation': 'rotation'})

			# x:56 y:102
			OperatableStateMachine.add('set angle',
										SetKey(Value=3.14159),
										transitions={'done': 'Move head'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'rotation'})

			# x:417 y:37
			OperatableStateMachine.add('store count',
										SetRosParam(ParamName="behavior/Count/CountedObjets"),
										transitions={'done': 'concat'},
										autonomy={'done': Autonomy.Off},
										remapping={'Value': 'Count'})

			# x:400 y:114
			OperatableStateMachine.add('concat',
										FlexibleCalculationState(calculation=lambda x: "I counted "+str(x[0])+" "+str(x[1])+".", input_keys=["Count", "className"]),
										transitions={'done': 'say Count'},
										autonomy={'done': Autonomy.Off},
										remapping={'Count': 'Count', 'className': 'className', 'output_value': 'Text'})

			# x:432 y:182
			OperatableStateMachine.add('say Count',
										SaraSayKey(Format=lambda x: x, emotion=1, block=True),
										transitions={'done': 'Look Center Found'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'Text'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
