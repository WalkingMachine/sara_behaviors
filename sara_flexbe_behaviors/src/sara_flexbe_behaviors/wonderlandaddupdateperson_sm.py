#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib;

roslib.load_manifest('behavior_wonderlandaddupdateperson')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine
from sara_flexbe_states.WonderlandAddPerson import WonderlandAddPerson
from sara_flexbe_states.WonderlandPatchPerson import WonderlandPatchPerson

# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Fri May 18 2018
@author: Lucas Maurice
'''


class WonderlandAddUpdatePersonSM(Behavior):
    '''
    Add or update a person in wonderland.
    '''

    def __init__(self):
        super(WonderlandAddUpdatePersonSM, self).__init__()
        self.name = 'WonderlandAddUpdatePerson'

    # parameters of this behavior

    # references to used behaviors

    # Additional initialization code can be added inside the following tags
    # [MANUAL_INIT]

    # [/MANUAL_INIT]

    # Behavior comments:

    def create(self):
        # x:322 y:361, x:960 y:237, x:804 y:397, x:817 y:95
        _state_machine = OperatableStateMachine(outcomes=['added', 'updated', 'error', 'bad_object'],
                                                input_keys=['entity'])
        _state_machine.userdata.entity = None

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]

        # [/MANUAL_CREATE]

        with _state_machine:
            # x:216 y:230
            OperatableStateMachine.add('AddPerson',
                                       WonderlandAddPerson(),
                                       transitions={'done': 'added', 'already_exit': 'PatchPerson',
                                                    'bad_request': 'bad_object', 'error': 'error'},
                                       autonomy={'done': Autonomy.Off, 'already_exit': Autonomy.Off,
                                                 'bad_request': Autonomy.Off, 'error': Autonomy.Off},
                                       remapping={'entity': 'entity'})

            # x:586 y:231
            OperatableStateMachine.add('PatchPerson',
                                       WonderlandPatchPerson(),
                                       transitions={'done': 'updated', 'dont_exist': 'bad_object',
                                                    'bad_request': 'bad_object', 'error': 'error'},
                                       autonomy={'done': Autonomy.Off, 'dont_exist': Autonomy.Off,
                                                 'bad_request': Autonomy.Off, 'error': Autonomy.Off},
                                       remapping={'entity': 'entity'})

        return _state_machine

# Private functions can be added inside the following tags
# [MANUAL_FUNC]

# [/MANUAL_FUNC]
