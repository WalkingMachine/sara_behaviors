#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_wonderlandsaveallpersons')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.list_entities_by_name import list_entities_by_name
from flexbe_states.log_state import LogState
from flexbe_states.calculation_state import CalculationState
from flexbe_states.check_condition_state import CheckConditionState
from flexbe_states.flexible_calculation_state import FlexibleCalculationState
from behavior_wonderlandaddupdateperson.wonderlandaddupdateperson_sm import WonderlandAddUpdatePersonSM
from sara_flexbe_states.SetKey import SetKey
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Fri Jun 7 2018
@author: Lucas Maurice
'''
class WonderlandSaveAllPersonsSM(Behavior):
	'''
	Add or update all people detected in wonderland.
	'''


	def __init__(self):
		super(WonderlandSaveAllPersonsSM, self).__init__()
		self.name = 'WonderlandSaveAllPersons'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(WonderlandAddUpdatePersonSM, 'Save all persons/WonderlandAddUpdatePerson')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]

    # [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:977 y:71, x:166 y:335
		_state_machine = OperatableStateMachine(outcomes=['done', 'none'], output_keys=['females', 'males', 'number'])
		_state_machine.userdata.person = "person"
		_state_machine.userdata.males = 0
		_state_machine.userdata.females = 0
		_state_machine.userdata.number = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]

        # [/MANUAL_CREATE]

		# x:55 y:794
		_sm_save_all_persons_0 = OperatableStateMachine(outcomes=['finished'], input_keys=['entities', 'number'], output_keys=['females', 'males'])

		with _sm_save_all_persons_0:
			# x:33 y:40
			OperatableStateMachine.add('setIndex',
										CalculationState(calculation=lambda x: x),
										transitions={'done': 'Init Female Count'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'number', 'output_value': 'index'})

			# x:228 y:261
			OperatableStateMachine.add('IsEnd',
										CheckConditionState(predicate=lambda x: x>0),
										transitions={'true': 'Decrease Index', 'false': 'finished'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'index'})

			# x:434 y:186
			OperatableStateMachine.add('Decrease Index',
										CalculationState(calculation=lambda x: x-1),
										transitions={'done': 'Select entity'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'index', 'output_value': 'index'})

			# x:621 y:189
			OperatableStateMachine.add('Select entity',
										FlexibleCalculationState(calculation=lambda x: x[0][x[1]], input_keys=["index", "entities"]),
										transitions={'done': 'Is Female'},
										autonomy={'done': Autonomy.Off},
										remapping={'index': 'index', 'entities': 'entities', 'output_value': 'entity'})

			# x:564 y:459
			OperatableStateMachine.add('WonderlandAddUpdatePerson',
										self.use_behavior(WonderlandAddUpdatePersonSM, 'Save all persons/WonderlandAddUpdatePerson'),
										transitions={'added': 'Added', 'updated': 'Updated', 'error': 'BadObject', 'bad_object': 'BadObject'},
										autonomy={'added': Autonomy.Inherit, 'updated': Autonomy.Inherit, 'error': Autonomy.Inherit, 'bad_object': Autonomy.Inherit},
										remapping={'entity': 'entity'})

			# x:448 y:281
			OperatableStateMachine.add('Added',
										LogState(text="Object added.", severity=Logger.REPORT_HINT),
										transitions={'done': 'IsEnd'},
										autonomy={'done': Autonomy.Off})

			# x:398 y:362
			OperatableStateMachine.add('Updated',
										LogState(text="Object already in Database. Updated.", severity=Logger.REPORT_WARN),
										transitions={'done': 'IsEnd'},
										autonomy={'done': Autonomy.Off})

			# x:276 y:466
			OperatableStateMachine.add('BadObject',
										LogState(text="Can not add oject.", severity=Logger.REPORT_ERROR),
										transitions={'done': 'IsEnd'},
										autonomy={'done': Autonomy.Off})

			# x:29 y:120
			OperatableStateMachine.add('Init Female Count',
										SetKey(Value=0),
										transitions={'done': 'Init Male Count'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'females'})

			# x:30 y:200
			OperatableStateMachine.add('Init Male Count',
										SetKey(Value=0),
										transitions={'done': 'IsEnd'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'males'})

			# x:886 y:311
			OperatableStateMachine.add('Is Male',
										CheckConditionState(predicate=lambda x: x.face.gender == "male"),
										transitions={'true': 'Increase Male', 'false': 'WonderlandAddUpdatePerson'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'entity'})

			# x:1094 y:185
			OperatableStateMachine.add('Is Female',
										CheckConditionState(predicate=lambda x: x.face.gender == "female"),
										transitions={'true': 'Increase Female', 'false': 'Is Male'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'entity'})

			# x:1107 y:607
			OperatableStateMachine.add('Increase Female',
										CalculationState(calculation=lambda x: x+1),
										transitions={'done': 'WonderlandAddUpdatePerson'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'females', 'output_value': 'females'})

			# x:879 y:440
			OperatableStateMachine.add('Increase Male',
										CalculationState(calculation=lambda x: x+1),
										transitions={'done': 'WonderlandAddUpdatePerson'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'males', 'output_value': 'males'})



		with _state_machine:
			# x:249 y:50
			OperatableStateMachine.add('Get All Persons',
										list_entities_by_name(frontality_level=0.5),
										transitions={'found': 'Save all persons', 'not_found': 'No Person Found'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'name': 'person', 'entity_list': 'entities', 'number': 'number'})

			# x:181 y:218
			OperatableStateMachine.add('No Person Found',
										LogState(text="No person found.", severity=Logger.REPORT_WARN),
										transitions={'done': 'none'},
										autonomy={'done': Autonomy.Off})

			# x:483 y:37
			OperatableStateMachine.add('Save all persons',
										_sm_save_all_persons_0,
										transitions={'finished': 'Saved!'},
										autonomy={'finished': Autonomy.Inherit},
										remapping={'entities': 'entities', 'number': 'number', 'females': 'females', 'males': 'males'})

			# x:752 y:47
			OperatableStateMachine.add('Saved!',
										LogState(text="All person saved!", severity=Logger.REPORT_HINT),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]

# [/MANUAL_FUNC]
