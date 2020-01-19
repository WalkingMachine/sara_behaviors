#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.GetRosParam import GetRosParam
from sara_flexbe_behaviors.action_give_sm import Action_GiveSM
from sara_flexbe_states.sara_say import SaraSay
from flexbe_states.calculation_state import CalculationState
from flexbe_states.check_condition_state import CheckConditionState
from sara_flexbe_states.get_speech import GetSpeech
from sara_flexbe_behaviors.action_findperson_sm import Action_findPersonSM
from sara_flexbe_states.SetRosParam import SetRosParam
from sara_flexbe_states.SetKey import SetKey
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sat June 2 2018
@author: Veronica
'''
class ActionWrapper_GiveSM(Behavior):
	'''
	action wrapper pour give
	'''


	def __init__(self):
		super(ActionWrapper_GiveSM, self).__init__()
		self.name = 'ActionWrapper_Give'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(Action_GiveSM, 'Action_Give')
		self.add_behavior(Action_findPersonSM, 'get_person/Action_findPerson_2')
		self.add_behavior(Action_findPersonSM, 'get_person/Action_findPerson')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
        
        # [/MANUAL_INIT]

		# Behavior comments:

		# O 333 0 
		# Give|n1- to whom



	def create(self):
		# x:998 y:146, x:723 y:729, x:1065 y:284
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'critical_fail'], input_keys=['Action'])
		_state_machine.userdata.Action = []
		_state_machine.userdata.person_name = "operator"
		_state_machine.userdata.Empty = None
		_state_machine.userdata.className = "person"

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

		# x:585 y:427, x:704 y:287, x:702 y:47
		_sm_get_person_0 = OperatableStateMachine(outcomes=['true', 'done', 'pas_done'], input_keys=['Action', 'className'], output_keys=['entity'])

		with _sm_get_person_0:
			# x:30 y:40
			OperatableStateMachine.add('cond',
										CheckConditionState(predicate=lambda x: x[1] != ''),
										transitions={'true': 'get ', 'false': 'Action_findPerson_2'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'Action'})

			# x:9 y:537
			OperatableStateMachine.add('name',
										GetSpeech(watchdog=5),
										transitions={'done': 'confirming_persons_name', 'nothing': 'name', 'fail': 'Action_findPerson'},
										autonomy={'done': Autonomy.Off, 'nothing': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'words': 'person_name'})

			# x:295 y:359
			OperatableStateMachine.add('confirming_persons_name',
										CheckConditionState(predicate=lambda x: "yes" in x),
										transitions={'true': 'true', 'false': 'Action_findPerson'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'person_name'})

			# x:338 y:105
			OperatableStateMachine.add('Action_findPerson_2',
										self.use_behavior(Action_findPersonSM, 'get_person/Action_findPerson_2'),
										transitions={'done': 'done', 'pas_done': 'pas_done'},
										autonomy={'done': Autonomy.Inherit, 'pas_done': Autonomy.Inherit},
										remapping={'className': 'className', 'entity': 'entity'})

			# x:21 y:223
			OperatableStateMachine.add('Action_findPerson',
										self.use_behavior(Action_findPersonSM, 'get_person/Action_findPerson'),
										transitions={'done': 'Is_Person', 'pas_done': 'Action_findPerson_2'},
										autonomy={'done': Autonomy.Inherit, 'pas_done': Autonomy.Inherit},
										remapping={'className': 'className', 'entity': 'entity'})

			# x:47 y:127
			OperatableStateMachine.add('get ',
										CalculationState(calculation=lambda x: x[1]),
										transitions={'done': 'Action_findPerson'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Action', 'output_value': 'person_name'})

			# x:111 y:343
			OperatableStateMachine.add('Is_Person',
										SaraSay(sentence=lambda x: "Hello, are you "+x+"?", input_keys=[], emotion=0, block=True),
										transitions={'done': 'name'},
										autonomy={'done': Autonomy.Off})



		with _state_machine:
			# x:43 y:40
			OperatableStateMachine.add('Object',
										GetRosParam(ParamName="behavior/GripperContent"),
										transitions={'done': 'get_person', 'failed': 'no_object'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'Value': 'gripperContent'})

			# x:369 y:92
			OperatableStateMachine.add('Action_Give',
										self.use_behavior(Action_GiveSM, 'Action_Give'),
										transitions={'Given': 'empty hand', 'Person_not_found': 'Person_Lost', 'No_object_in_hand': 'cause1', 'fail': 'cause3'},
										autonomy={'Given': Autonomy.Inherit, 'Person_not_found': Autonomy.Inherit, 'No_object_in_hand': Autonomy.Inherit, 'fail': Autonomy.Inherit})

			# x:286 y:217
			OperatableStateMachine.add('Nobody_here',
										SaraSay(sentence="I can't find a person. Goodbye.", input_keys=[], emotion=1, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:398 y:360
			OperatableStateMachine.add('getID',
										CalculationState(calculation=lambda x: x.ID),
										transitions={'done': 'Action_Give'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'entity', 'output_value': 'ID'})

			# x:116 y:178
			OperatableStateMachine.add('get_person',
										_sm_get_person_0,
										transitions={'true': 'confirm giving', 'done': 'confirm giving', 'pas_done': 'Nobody_here'},
										autonomy={'true': Autonomy.Inherit, 'done': Autonomy.Inherit, 'pas_done': Autonomy.Inherit},
										remapping={'Action': 'Action', 'className': 'className', 'entity': 'entity'})

			# x:53 y:480
			OperatableStateMachine.add('no_object',
										SaraSay(sentence="There is nothing in my gripper.", input_keys=[], emotion=1, block=True),
										transitions={'done': 'cause1'},
										autonomy={'done': Autonomy.Off})

			# x:212 y:355
			OperatableStateMachine.add('confirm giving',
										SaraSay(sentence="Let me give you this object.", input_keys=[], emotion=1, block=True),
										transitions={'done': 'getID'},
										autonomy={'done': Autonomy.Off})

			# x:806 y:92
			OperatableStateMachine.add('empty hand',
										SetRosParam(ParamName="behavior/GripperContent"),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'Value': 'Empty'})

			# x:586 y:453
			OperatableStateMachine.add('cause1',
										SetKey(Value="There was nothing in my gripper."),
										transitions={'done': 'setcausefailure'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Key'})

			# x:789 y:373
			OperatableStateMachine.add('cause2',
										SetKey(Value="I lost the person."),
										transitions={'done': 'setcausefailure'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Key'})

			# x:886 y:230
			OperatableStateMachine.add('cause3',
										SetKey(Value="I was unable to give the object."),
										transitions={'done': 'setcausefailure'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Key'})

			# x:930 y:463
			OperatableStateMachine.add('setcausefailure',
										SetRosParam(ParamName="behavior/GPSR/CauseOfFailure"),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off},
										remapping={'Value': 'Key'})

			# x:680 y:259
			OperatableStateMachine.add('Person_Lost',
										SaraSay(sentence=lambda x: "I've lost "+x[1]+"!", input_keys=[], emotion=0, block=True),
										transitions={'done': 'cause2'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
