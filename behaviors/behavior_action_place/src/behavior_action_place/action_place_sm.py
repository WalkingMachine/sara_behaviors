#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_action_place')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.wait_state import WaitState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sat May 12 2018
@author: Raphaël Duchaîne
'''
class Action_placeSM(Behavior):
    '''
    Place un objet à une position
    '''


    def __init__(self):
        super(Action_placeSM, self).__init__()
        self.name = 'Action_place'

        # parameters of this behavior

        # references to used behaviors

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
        
        # [/MANUAL_INIT]

        # Behavior comments:

        # O 125 32 
        # TF Transform |nFrame1 Frame2|n

        # O 1029 137 
        # Gen Grip pose|n|nA

        # O 328 118 
        # MoveIt move|nmove = false|n|nPos

        # O 541 129 
        # PreGrip Pose #pre grip

        # O 743 126 
        # #approche Pose|nGen Grip pose|ndistance = 0.25|nB

        # O 1039 205 
        # MoveIt move|nmove =True|n|nA

        # O 977 258 
        # open grip

        # O 868 131 
        # MoveIt move|nmove =True|n|nB

        # O 858 266 
        # MoveIt move|n|nB

        # O 759 297 
        # #preGrip|nMoveIt move



    def create(self):
        # x:688 y:316, x:546 y:230
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


        with _state_machine:
            # x:142 y:203
            OperatableStateMachine.add('WaitState',
                                        WaitState(wait_time=0),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
