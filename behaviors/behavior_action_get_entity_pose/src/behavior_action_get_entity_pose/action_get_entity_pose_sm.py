#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_action_get_entity_pose')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.get_box_center import GetBoxCenter
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Fri Oct 20 2017
@author: Philippe La Madeleine
'''
class Action_get_entity_poseSM(Behavior):
    '''
    standard way to get the pose on an entity
    '''


    def __init__(self):
        super(Action_get_entity_poseSM, self).__init__()
        self.name = 'Action_get_entity_pose'

        # parameters of this behavior

        # references to used behaviors

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
        
        # [/MANUAL_INIT]

        # Behavior comments:



    def create(self):
        # x:470 y:151, x:458 y:325
        _state_machine = OperatableStateMachine(outcomes=['found', 'not found'], input_keys=['name'], output_keys=['pose'])
        _state_machine.userdata.name = "cup"
        _state_machine.userdata.pose = 0

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


        with _state_machine:
            # x:106 y:129
            OperatableStateMachine.add('get box',
                                        GetBoxCenter(watchdog=5),
                                        transitions={'done': 'found', 'not_found': 'not found'},
                                        autonomy={'done': Autonomy.Off, 'not_found': Autonomy.Off},
                                        remapping={'box_name': 'name', 'point': 'pose'})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]