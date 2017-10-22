#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_check_reachability')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.gen_gripper_pose import GenGripperPose
from flexbe_states.check_condition_state import CheckConditionState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Fri Oct 20 2017
@author: Philippe La Madeleine
'''
class Check_reachabilitySM(Behavior):
    '''
    check if the object is in range
    '''


    def __init__(self):
        super(Check_reachabilitySM, self).__init__()
        self.name = 'Check_reachability'

        # parameters of this behavior

        # references to used behaviors

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
        
        # [/MANUAL_INIT]

        # Behavior comments:



    def create(self):
        # x:410 y:309, x:404 y:84
        _state_machine = OperatableStateMachine(outcomes=['ok', 'too_far'], input_keys=['pose'])
        _state_machine.userdata.pose = 0

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


        with _state_machine:
            # x:74 y:58
            OperatableStateMachine.add('gen',
                                        GenGripperPose(x=0, y=0, z=0, t=0),
                                        transitions={'done': 'first check'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'pose_in': 'pose', 'pose_out': 'pose_out'})

            # x:68 y:411
            OperatableStateMachine.add('third check',
                                        CheckConditionState(predicate=lambda x: x.position.x*x.position.x+x.position.y*x.position.y+x.position.z*x.position.z < 2),
                                        transitions={'true': 'ok', 'false': 'too_far'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                        remapping={'input_value': 'pose_out'})

            # x:69 y:171
            OperatableStateMachine.add('first check',
                                        CheckConditionState(predicate=lambda x: x.position.x<2),
                                        transitions={'true': 'second check', 'false': 'too_far'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                        remapping={'input_value': 'pose_out'})

            # x:76 y:275
            OperatableStateMachine.add('second check',
                                        CheckConditionState(predicate=lambda x: x.position.z>0.5),
                                        transitions={'true': 'third check', 'false': 'too_far'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                        remapping={'input_value': 'pose_out'})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
