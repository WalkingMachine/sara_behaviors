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
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.pose_gen_euler_key import GenPoseEulerKey
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_states.regex_tester import RegexTester
from sara_flexbe_states.Get_Number_From_Text import GetNumberFromText
from flexbe_states.log_key_state import LogKeyState
from sara_flexbe_states.sara_rel_move_base import SaraRelMoveBase
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sat Oct 28 2017
@author: Raphael Duchaine
'''
class ActionWrapper_MoveSM(Behavior):
    '''
    Behaviours
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



    def create(self):
        # x:822 y:356, x:821 y:464
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['Action'])
        _state_machine.userdata.Action = ['Move','',' backward',' one meter']
        _state_machine.userdata.x = ""
        _state_machine.userdata.y = ""
        _state_machine.userdata.z = ""
        _state_machine.userdata.theta = ""
        _state_machine.userdata.waypoint_id = ""
        _state_machine.userdata.pose = ""

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]

        # [/MANUAL_CREATE]

        # x:30 y:293
        _sm_initialize_vars_0 = OperatableStateMachine(outcomes=['done'], output_keys=['y', 'z', 'yaw', 'pitch', 'roll'])

        with _sm_initialize_vars_0:
            # x:31 y:40
            OperatableStateMachine.add('set z',
                                        SetKey(Value=0),
                                        transitions={'done': 'set y'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'Key': 'z'})

            # x:100 y:40
            OperatableStateMachine.add('set yaw',
                                        SetKey(Value=0),
                                        transitions={'done': 'set pitch'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'Key': 'yaw'})

            # x:111 y:110
            OperatableStateMachine.add('set pitch',
                                        SetKey(Value=0),
                                        transitions={'done': 'set roll'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'Key': 'pitch'})

            # x:30 y:175
            OperatableStateMachine.add('set roll',
                                        SetKey(Value=0),
                                        transitions={'done': 'done'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'Key': 'roll'})

            # x:42 y:105
            OperatableStateMachine.add('set y',
                                        SetKey(Value=0),
                                        transitions={'done': 'set yaw'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'Key': 'y'})


        # x:1094 y:102, x:1090 y:336
        _sm_gen_vector_1 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['Action'], output_keys=['pose'])

        with _sm_gen_vector_1:
            # x:30 y:124
            OperatableStateMachine.add('get distanceString',
                                        CalculationState(calculation=lambda x: x[3]),
                                        transitions={'done': 'get Distance'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'input_value': 'Action', 'output_value': 'distance_string'})

            # x:888 y:165
            OperatableStateMachine.add('gen pose ',
                                        GenPoseEulerKey(),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.High},
                                        remapping={'xpos': 'distance', 'ypos': 'y', 'zpos': 'z', 'yaw': 'yaw', 'pitch': 'pitch', 'roll': 'roll', 'pose': 'pose'})

            # x:653 y:119
            OperatableStateMachine.add('initialize vars',
                                        _sm_initialize_vars_0,
                                        transitions={'done': 'log distance'},
                                        autonomy={'done': Autonomy.Inherit},
                                        remapping={'y': 'y', 'z': 'z', 'yaw': 'yaw', 'pitch': 'pitch', 'roll': 'roll'})

            # x:361 y:152
            OperatableStateMachine.add('Parse If forward',
                                        RegexTester(regex=".*forward"),
                                        transitions={'true': 'initialize vars', 'false': 'Parse if Backward'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                        remapping={'text': 'Action', 'result': 'result'})

            # x:161 y:278
            OperatableStateMachine.add('get Distance',
                                        GetNumberFromText(min=0, max=100),
                                        transitions={'done': 'Parse If forward', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'text': 'distance_string', 'value': 'distance', 'unit': 'unit'})

            # x:765 y:199
            OperatableStateMachine.add('log distance',
                                        LogKeyState(text="distance:{}", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'gen pose '},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'data': 'distance'})

            # x:356 y:237
            OperatableStateMachine.add('Parse if Backward',
                                        RegexTester(regex=".*back"),
                                        transitions={'true': 'reverse distance', 'false': 'failed'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                        remapping={'text': 'Action', 'result': 'result'})

            # x:580 y:210
            OperatableStateMachine.add('reverse distance',
                                        CalculationState(calculation=lambda x: x*-1),
                                        transitions={'done': 'initialize vars'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'input_value': 'distance', 'output_value': 'distance'})


        # x:30 y:325
        _sm_move_to_location_2 = OperatableStateMachine(outcomes=['done'], input_keys=['Action'])

        with _sm_move_to_location_2:
            # x:30 y:40
            OperatableStateMachine.add('Get name of location',
                                        CalculationState(calculation=lambda x: x[1]),
                                        transitions={'done': 'done'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'input_value': 'Action', 'output_value': 'name'})



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

            # x:362 y:125
            OperatableStateMachine.add('move to location',
                                        _sm_move_to_location_2,
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Inherit},
                                        remapping={'Action': 'Action'})

            # x:327 y:307
            OperatableStateMachine.add('gen vector',
                                        _sm_gen_vector_1,
                                        transitions={'finished': 'move sara rel', 'failed': 'say no goal given'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'Action': 'Action', 'pose': 'pose'})

            # x:499 y:302
            OperatableStateMachine.add('move sara rel',
                                        SaraRelMoveBase(),
                                        transitions={'arrived': 'finished', 'failed': 'finished'},
                                        autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'pose': 'pose'})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]

    # [/MANUAL_FUNC]
