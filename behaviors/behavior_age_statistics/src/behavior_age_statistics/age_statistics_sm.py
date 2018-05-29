#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_age_statistics')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.TakeImageCamera import TakeImageCamera
from sara_flexbe_states.Found_age_statistics import Found_age_statitics
from flexbe_states.log_key_state import LogKeyState
from flexbe_states.wait_state import WaitState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sat May 26 2018
@author: QuentinG
'''
class Age_StatisticsSM(Behavior):
	'''
	Return the number of person in each age range of gender-age-service
	'''


	def __init__(self):
		super(Age_StatisticsSM, self).__init__()
		self.name = 'Age_Statistics'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:586 y:482, x:96 y:491
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:123 y:53
			OperatableStateMachine.add('readImage',
										TakeImageCamera(topic="/head_xtion/rgb/image_raw"),
										transitions={'received': 'ageStat', 'unavailable': 'waitSmall'},
										autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
										remapping={'image': 'image'})

			# x:90 y:333
			OperatableStateMachine.add('ageStat',
										Found_age_statitics(),
										transitions={'People_found': 'printKids', 'Nobody_found': 'readImage'},
										autonomy={'People_found': Autonomy.Off, 'Nobody_found': Autonomy.Off},
										remapping={'image': 'image', 'nbOfFrom0to2': 'nbOfFrom0to2', 'nbOfFrom3to6': 'nbOfFrom3to6', 'nbOfFrom7to13': 'nbOfFrom7to13', 'nbOfFrom14to22': 'nbOfFrom14to22', 'nbOfFrom23to34': 'nbOfFrom23to34', 'nbOfFrom35to45': 'nbOfFrom35to45', 'nbOfFrom46to56': 'nbOfFrom46to56', 'nbOfFrom57to100': 'nbOfFrom57to100', 'nbOfKids': 'nbOfKids', 'nbOfTeenagers': 'nbOfTeenagers', 'nbOfAdults': 'nbOfAdults', 'listPrediction': 'listPrediction'})

			# x:408 y:315
			OperatableStateMachine.add('printTeen',
										LogKeyState(text="{} teenager(s) found", severity=Logger.REPORT_HINT),
										transitions={'done': 'printAdults'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'nbOfTeenagers'})

			# x:306 y:69
			OperatableStateMachine.add('WaitLong',
										WaitState(wait_time=2),
										transitions={'done': 'readImage'},
										autonomy={'done': Autonomy.Off})

			# x:14 y:146
			OperatableStateMachine.add('waitSmall',
										WaitState(wait_time=1),
										transitions={'done': 'readImage'},
										autonomy={'done': Autonomy.Off})

			# x:625 y:297
			OperatableStateMachine.add('printAdults',
										LogKeyState(text=" and {} adults", severity=Logger.REPORT_HINT),
										transitions={'done': 'readImage'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'nbOfAdults'})

			# x:281 y:413
			OperatableStateMachine.add('printKids',
										LogKeyState(text="{} kids ", severity=Logger.REPORT_HINT),
										transitions={'done': 'printTeen'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'nbOfKids'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
