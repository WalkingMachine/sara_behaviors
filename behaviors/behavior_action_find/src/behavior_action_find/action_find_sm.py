#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_action_find')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.wait_state import WaitState
from sara_flexbe_states.sara_move_base import SaraMoveBase
from sara_flexbe_states.for_loop import ForLoop
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sat May 12 2018
@author: Raphaël Duchaîne
'''
class Action_findSM(Behavior):
    '''
    Cherche et trouve quelque chose. (personne ou objet) en étant souscrit au topic /entities
    '''


    def __init__(self):
        super(Action_findSM, self).__init__()
        self.name = 'Action_find'

        # parameters of this behavior

        # references to used behaviors

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
        
        # [/MANUAL_INIT]

        # Behavior comments:



    def create(self):
        # x:30 y:293, x:130 y:293
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


        with _state_machine:
            # x:40 y:72
            OperatableStateMachine.add('Placeholder',
                                        WaitState(wait_time=0),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off})

            # x:764 y:338
            OperatableStateMachine.add('rotateToTheRight',
                                        SaraMoveBase(),
                                        transitions={'arrived': 'search_around', 'failed': 'finished'},
                                        autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'pose': 'pose'})

            # x:496 y:173
            OperatableStateMachine.add('search_around',
                                        ForLoop(repeat=4),
                                        transitions={'do': 'rotateToTheRight', 'end': 'failed'},
                                        autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
                                        remapping={'index': 'index'})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
