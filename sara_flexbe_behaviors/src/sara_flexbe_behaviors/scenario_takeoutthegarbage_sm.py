#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_behaviors.action_move_sm import Action_MoveSM as sara_flexbe_behaviors__Action_MoveSM
from sara_flexbe_states.sara_say import SaraSay
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon May 13 2019
@author: Quentin Gaillot
'''
class Scenario_TakeOutTheGarbageSM(Behavior):
	'''
	Scenario 2019 for Take out the garbage, House keeper
	'''


	def __init__(self):
		super(Scenario_TakeOutTheGarbageSM, self).__init__()
		self.name = 'Scenario_TakeOutTheGarbage'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'First bin/go to bin/Action_Move')
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'second bin/go to bin/Action_Move')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:

		# O 195 44 /second bin/find the bin
		# write a state to detect the bin.|nLidar?|nsegmentation?

		# O 51 82 /First bin/find the bin
		# write a state to detect the bin.|nLidar?|nsegmentation?



	def create(self):
		# x:910 y:782, x:907 y:184
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.bin1Waypoint = "bin1"
		_state_machine.userdata.bin2Waypoint = "bin2"
		_state_machine.userdata.bin1Height = "1"
		_state_machine.userdata.bin2Height = "1"
		_state_machine.userdata.dropzoneWaypoint = "dropzone"

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:30 y:458, x:130 y:458
		_sm_go_to_drop_the_bag_0 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['dropzoneWaypoint'])

		with _sm_go_to_drop_the_bag_0:
			# x:30 y:40
			OperatableStateMachine.add('say',
										SaraSay(sentence="test", input_keys=[], emotion=0, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		# x:30 y:458, x:130 y:458
		_sm_get_the_bag_1 = OperatableStateMachine(outcomes=['finished', 'failed'])

		with _sm_get_the_bag_1:
			# x:30 y:40
			OperatableStateMachine.add('say',
										SaraSay(sentence="test", input_keys=[], emotion=0, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		# x:30 y:458, x:130 y:458
		_sm_find_the_bin_2 = OperatableStateMachine(outcomes=['finished', 'failed'])

		with _sm_find_the_bin_2:
			# x:38 y:169
			OperatableStateMachine.add('say',
										SaraSay(sentence="test", input_keys=[], emotion=0, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		# x:852 y:441, x:862 y:114
		_sm_go_to_bin_3 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['bin2Waypoint'])

		with _sm_go_to_bin_3:
			# x:268 y:164
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'second bin/go to bin/Action_Move'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'bin2Waypoint'})


		# x:30 y:458, x:130 y:458
		_sm_go_to_drop_the_bag_4 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['dropzoneWaypoint'])

		with _sm_go_to_drop_the_bag_4:
			# x:30 y:40
			OperatableStateMachine.add('say',
										SaraSay(sentence="test", input_keys=[], emotion=0, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		# x:30 y:458, x:130 y:458
		_sm_get_the_bag_5 = OperatableStateMachine(outcomes=['finished', 'failed'])

		with _sm_get_the_bag_5:
			# x:30 y:40
			OperatableStateMachine.add('say',
										SaraSay(sentence="test", input_keys=[], emotion=0, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		# x:30 y:458, x:130 y:458
		_sm_find_the_bin_6 = OperatableStateMachine(outcomes=['finished', 'failed'])

		with _sm_find_the_bin_6:
			# x:40 y:192
			OperatableStateMachine.add('say',
										SaraSay(sentence="test", input_keys=[], emotion=0, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		# x:573 y:546, x:622 y:92
		_sm_go_to_bin_7 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['bin1Waypoint'])

		with _sm_go_to_bin_7:
			# x:254 y:199
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'First bin/go to bin/Action_Move'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'bin1Waypoint'})


		# x:946 y:467, x:907 y:75
		_sm_second_bin_8 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['bin2Waypoint', 'bin2Height', 'dropzoneWaypoint'])

		with _sm_second_bin_8:
			# x:150 y:33
			OperatableStateMachine.add('go to bin',
										_sm_go_to_bin_3,
										transitions={'finished': 'find the bin', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'bin2Waypoint': 'bin2Waypoint'})

			# x:149 y:164
			OperatableStateMachine.add('find the bin',
										_sm_find_the_bin_2,
										transitions={'finished': 'get the bag', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:145 y:299
			OperatableStateMachine.add('get the bag',
										_sm_get_the_bag_1,
										transitions={'finished': 'go to drop the bag', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:141 y:430
			OperatableStateMachine.add('go to drop the bag',
										_sm_go_to_drop_the_bag_0,
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'dropzoneWaypoint': 'dropzoneWaypoint'})


		# x:776 y:624, x:717 y:53
		_sm_first_bin_9 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['bin1Waypoint', 'bin1Height', 'dropzoneWaypoint'])

		with _sm_first_bin_9:
			# x:150 y:33
			OperatableStateMachine.add('go to bin',
										_sm_go_to_bin_7,
										transitions={'finished': 'find the bin', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'bin1Waypoint': 'bin1Waypoint'})

			# x:149 y:164
			OperatableStateMachine.add('find the bin',
										_sm_find_the_bin_6,
										transitions={'finished': 'get the bag', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:145 y:299
			OperatableStateMachine.add('get the bag',
										_sm_get_the_bag_5,
										transitions={'finished': 'go to drop the bag', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:141 y:430
			OperatableStateMachine.add('go to drop the bag',
										_sm_go_to_drop_the_bag_4,
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'dropzoneWaypoint': 'dropzoneWaypoint'})



		with _state_machine:
			# x:277 y:63
			OperatableStateMachine.add('First bin',
										_sm_first_bin_9,
										transitions={'finished': 'second bin', 'failed': 'try second bin'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'bin1Waypoint': 'bin1Waypoint', 'bin1Height': 'bin1Height', 'dropzoneWaypoint': 'dropzoneWaypoint'})

			# x:331 y:381
			OperatableStateMachine.add('second bin',
										_sm_second_bin_8,
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'bin2Waypoint': 'bin2Waypoint', 'bin2Height': 'bin2Height', 'dropzoneWaypoint': 'dropzoneWaypoint'})

			# x:444 y:195
			OperatableStateMachine.add('try second bin',
										SaraSay(sentence="I failed to take out the garbage from the first bin but I will try the second bin.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'second bin'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
