#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_actionwrapper_waitfordoor')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.door_detector import DoorDetector
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed Jul 26 2017
@author: Samuel Otis
'''
class ActionWrapper_WaitForDoorSM(Behavior):
    '''
    This behavior waits for the opening of a door
    '''


    def __init__(self):
        super(ActionWrapper_WaitForDoorSM, self).__init__()
        self.name = 'ActionWrapper_WaitForDoor'

        # parameters of this behavior

        # references to used behaviors

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
        
        # [/MANUAL_INIT]

        # Behavior comments:



    def create(self):
        # x:30 y:304, x:130 y:304
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


        with _state_machine:
            # x:137 y:150
            OperatableStateMachine.add('DoorDetector',
                                        DoorDetector(timeout=10),
                                        transitions={'done': 'finished', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
