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
from sara_flexbe_states.sara_move_base import SaraMoveBase
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.regex_tester import RegexTester
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_states.pose_gen_euler_key import GenPoseEulerKey
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
        _state_machine.userdata.x = ""
        _state_machine.userdata.y = ""
        _state_machine.userdata.z = ""
        _state_machine.userdata.theta = ""
        _state_machine.userdata.waypoint_id = ""
        _state_machine.userdata.pose = ""

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

        # x:819 y:438
        _sm_gen_vector_0 = OperatableStateMachine(outcomes=['finished'], input_keys=['Action'], output_keys=['pose'])

        with _sm_gen_vector_0:
            # x:139 y:36
            OperatableStateMachine.add('Parse If forward',
                                        RegexTester(regex=".*forward"),
                                        transitions={'true': 'set distance forward', 'false': 'finished'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                        remapping={'text': 'Action', 'result': 'result'})

            # x:612 y:123
            OperatableStateMachine.add('set pitch forward',
                                        SetKey(Value=0),
                                        transitions={'done': 'set roll forward'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'Key': 'pitch'})

            # x:641 y:179
            OperatableStateMachine.add('set roll forward',
                                        SetKey(Value=0),
                                        transitions={'done': 'gen pose forward'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'Key': 'roll'})

            # x:590 y:56
            OperatableStateMachine.add('set yaw forward',
                                        SetKey(Value=0),
                                        transitions={'done': 'set pitch forward'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'Key': 'yaw'})

            # x:416 y:31
            OperatableStateMachine.add('set distance forward',
                                        SetKey(Value=1),
                                        transitions={'done': 'set y forward'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'Key': 'distance'})

            # x:454 y:101
            OperatableStateMachine.add('set y forward',
                                        SetKey(Value=0),
                                        transitions={'done': 'set z forward'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'Key': 'y'})

            # x:488 y:173
            OperatableStateMachine.add('set z forward',
                                        SetKey(Value=0),
                                        transitions={'done': 'set yaw forward'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'Key': 'z'})

            # x:744 y:65
            OperatableStateMachine.add('gen pose forward',
                                        GenPoseEulerKey(),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'x': 'distance', 'y': 'y', 'z': 'z', 'yaw': 'yaw', 'pitch': 'pitch', 'roll': 'roll', 'pose': 'pose'})


        # x:30 y:325
        _sm_move_to_location_1 = OperatableStateMachine(outcomes=['done'], input_keys=['Action'])

        with _sm_move_to_location_1:
            # x:30 y:40
            OperatableStateMachine.add('Get name of location',
                                        CalculationState(calculation=lambda x: x[1]),
                                        transitions={'done': 'done'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'input_value': 'Action', 'output_value': 'name'})


        # x:525 y:95, x:551 y:258
        _sm_move_vector_2 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['pose'])

        with _sm_move_vector_2:
            # x:201 y:59
            OperatableStateMachine.add('move Sara',
                                        SaraMoveBase(),
                                        transitions={'arrived': 'finished', 'failed': 'failed'},
                                        autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'pose': 'pose'})



        with _state_machine:
            # x:21 y:122
            OperatableStateMachine.add('check',
                                        CheckConditionState(predicate=lambda x: x[1] != ''),
                                        transitions={'true': 'say area', 'false': 'cond1'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                        remapping={'input_value': 'Action'})

            # x:187 y:328
            OperatableStateMachine.add('say vector',
                                        SaraSayKey(Format=lambda x: "I'm now going to move "+x[2]+x[3], emotion=1, block=True),
                                        transitions={'done': 'gen vector'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'sentence': 'Action'})

            # x:230 y:127
            OperatableStateMachine.add('say area',
                                        SaraSayKey(Format=lambda x: "I'm now going to the "+x[1], emotion=1, block=True),
                                        transitions={'done': 'move to location'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'sentence': 'Action'})

            # x:15 y:329
            OperatableStateMachine.add('cond1',
                                        CheckConditionState(predicate=lambda x: x[2] != ''),
                                        transitions={'true': 'say vector', 'false': 'say no info'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                        remapping={'input_value': 'Action'})

            # x:35 y:521
            OperatableStateMachine.add('say no info',
                                        SaraSay(sentence="You didn't told me where to go", emotion=1, block=True),
                                        transitions={'done': 'say no goal given'},
                                        autonomy={'done': Autonomy.Off})

            # x:373 y:528
            OperatableStateMachine.add('say no goal given',
                                        SaraSay(sentence="I'm lost now because of you", emotion=1, block=True),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off})

            # x:504 y:299
            OperatableStateMachine.add('move vector',
                                        _sm_move_vector_2,
                                        transitions={'finished': 'finished', 'failed': 'failed'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'pose': 'pose'})

            # x:362 y:125
            OperatableStateMachine.add('move to location',
                                        _sm_move_to_location_1,
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Inherit},
                                        remapping={'Action': 'Action'})

            # x:327 y:307
            OperatableStateMachine.add('gen vector',
                                        _sm_gen_vector_0,
                                        transitions={'finished': 'move vector'},
                                        autonomy={'finished': Autonomy.Inherit},
                                        remapping={'Action': 'Action', 'pose': 'pose'})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
