#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_action_turn')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.pose_gen_euler import GenPoseEuler
from behavior_action_move.action_move_sm import Action_MoveSM
from sara_flexbe_states.SetKey import SetKey
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon May 21 2018
@author: Raphael Duchaine
'''
class action_turnSM(Behavior):
    '''
    Quality of life action

Ask for a rotation in degree with forward as 0deg

Verify which rotation is positive
    '''


    def __init__(self):
        super(action_turnSM, self).__init__()
        self.name = 'action_turn'

        # parameters of this behavior

        # references to used behaviors
        self.add_behavior(Action_MoveSM, 'Action_Move')

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
        
        # [/MANUAL_INIT]

        # Behavior comments:



    def create(self):
        # x:445 y:258, x:241 y:301
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['rotation'])
        _state_machine.userdata.rotation = 0

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


        with _state_machine:
            # x:38 y:33
            OperatableStateMachine.add('GenPoseEuler',
                                        GenPoseEuler(x=0, y=0, z=0, roll=0, pitch=0, yaw=rotation),
                                        transitions={'done': 'SetRelative'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'pose': 'pose'})

            # x:126 y:142
            OperatableStateMachine.add('Action_Move',
                                        self.use_behavior(Action_MoveSM, 'Action_Move'),
                                        transitions={'finished': 'finished', 'failed': 'failed'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'pose': 'pose', 'relative': 'relative'})

            # x:185 y:27
            OperatableStateMachine.add('SetRelative',
                                        SetKey(Value=True),
                                        transitions={'done': 'Action_Move'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'Key': 'relative'})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
