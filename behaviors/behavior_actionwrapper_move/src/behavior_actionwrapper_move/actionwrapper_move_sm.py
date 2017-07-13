#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_actionwrapper_move')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.check_condition_state import CheckConditionState
from sara_flexbe_states.sara_say_key import SaraSayKey
from sara_flexbe_states.sara_say import SaraSay
from flexbe_states.wait_state import WaitState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Tue Jul 11 2017
@author: Philippe La Madeleine
'''
class ActionWrapper_MoveSM(Behavior):
    '''
    action wrapper pour move_base
    '''


    def __init__(self):
        super(ActionWrapper_MoveSM, self).__init__()
        self.name = 'ActionWrapper_Move'

        # parameters of this behavior

        # references to used behaviors

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
        
        # [/MANUAL_INIT]

        # Behavior comments:

        # O 664 17 
        # move|n1- where to go|n2- direction to go (oferriden by 1-)|n3- distance to go (oferriden by 1-)



    def create(self):
        # x:822 y:356, x:821 y:464
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['Action'])
        _state_machine.userdata.Action = ['Move','','forward','1 meter']

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

        # x:30 y:322, x:130 y:322
        _sm_move_area_0 = OperatableStateMachine(outcomes=['finished', 'failed'])

        with _sm_move_area_0:
            # x:46 y:190
            OperatableStateMachine.add('wait',
                                        WaitState(wait_time=2),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off})


        # x:30 y:322, x:130 y:322
        _sm_move_vector_1 = OperatableStateMachine(outcomes=['finished', 'failed'])

        with _sm_move_vector_1:
            # x:52 y:136
            OperatableStateMachine.add('wait',
                                        WaitState(wait_time=2),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off})



        with _state_machine:
            # x:21 y:122
            OperatableStateMachine.add('check',
                                        CheckConditionState(predicate=lambda x: x[1] != ''),
                                        transitions={'true': 'say area', 'false': 'cond1'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                        remapping={'input_value': 'Action'})

            # x:187 y:328
            OperatableStateMachine.add('say vector',
                                        SaraSayKey(Format=lambda x: "I'm now going to move "+x[2]+x[3], emotion=1),
                                        transitions={'done': 'move vector'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'sentence': 'Action'})

            # x:203 y:123
            OperatableStateMachine.add('say area',
                                        SaraSayKey(Format=lambda x: "I'm now going to the "+x[1], emotion=1),
                                        transitions={'done': 'move area'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'sentence': 'Action'})

            # x:15 y:329
            OperatableStateMachine.add('cond1',
                                        CheckConditionState(predicate=lambda x: x[2] != ''),
                                        transitions={'true': 'say vector', 'false': 'say no info'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                        remapping={'input_value': 'Action'})

            # x:32 y:573
            OperatableStateMachine.add('say no info',
                                        SaraSay(sentence="You didn't told me where to go", emotion=1),
                                        transitions={'done': 'say no goal given'},
                                        autonomy={'done': Autonomy.Off})

            # x:372 y:574
            OperatableStateMachine.add('say no goal given',
                                        SaraSay(sentence="I'm lost now because of you", emotion=1),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off})

            # x:366 y:323
            OperatableStateMachine.add('move vector',
                                        _sm_move_vector_1,
                                        transitions={'finished': 'finished', 'failed': 'failed'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

            # x:363 y:118
            OperatableStateMachine.add('move area',
                                        _sm_move_area_0,
                                        transitions={'finished': 'finished', 'failed': 'failed'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
