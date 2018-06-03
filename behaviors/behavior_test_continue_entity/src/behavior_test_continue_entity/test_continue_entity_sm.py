#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_test_continue_entity')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.sara_say import SaraSay
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.list_entities_by_name import list_entities_by_name
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Tue Jul 25 2017
@author: Philippe la Madeleine
'''
class Test_continue_entitySM(Behavior):
    '''
    test the continue button
    '''


    def __init__(self):
        super(Test_continue_entitySM, self).__init__()
        self.name = 'Test_continue_entity'

        # parameters of this behavior

        # references to used behaviors

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]

	# [/MANUAL_INIT]

        # Behavior comments:



    def create(self):
        # x:828 y:190, x:382 y:420
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['list_person'])
        _state_machine.userdata.id = None
        _state_machine.userdata.name = "living room"
        _state_machine.userdata.type = None
        _state_machine.userdata.list_person = None

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]

		# [/MANUAL_CREATE]


        with _state_machine:
            # x:82 y:90
            OperatableStateMachine.add('debut',
                                        SaraSay(sentence='Je suis prete', emotion=1, block=True),
                                        transitions={'done': 'entity_name'},
                                        autonomy={'done': Autonomy.Off})

            # x:680 y:274
            OperatableStateMachine.add('parle',
                                        SaraSay(sentence='Destination atteinte', emotion=1, block=True),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off})

            # x:387 y:208
            OperatableStateMachine.add('get person position',
                                        CalculationState(calculation=lambda x: x[1].position),
                                        transitions={'done': 'parle'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'input_value': 'list_person', 'output_value': 'pos'})

            # x:200 y:167
            OperatableStateMachine.add('entity_name',
                                        list_entities_by_name(frontality_level=0 ),
                                        transitions={'found': 'get person position', 'not_found': 'failed'},
                                        autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
                                        remapping={'name': 'name', 'entity_list': 'entity_list', 'number': 'number'})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]

	# [/MANUAL_FUNC]
