#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_action_give')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.sara_follow import SaraFollow
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_states.torque_reader import ReadTorque
from sara_flexbe_states.set_gripper_state import SetGripperState
from sara_flexbe_states.sara_say import SaraSay
from flexbe_states.wait_state import WaitState
from sara_flexbe_states.moveit_move import MoveitMove
from flexbe_states.log_state import LogState
from sara_flexbe_states.SetRosParam import SetRosParam
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu May 10 2018
@author: Philippe La Madeleine
'''
class Action_GiveSM(Behavior):
    '''
    give the content of the gripper to a person.
    '''


    def __init__(self):
        super(Action_GiveSM, self).__init__()
        self.name = 'Action_Give'

        # parameters of this behavior

        # references to used behaviors

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
		
		# [/MANUAL_INIT]

        # Behavior comments:



    def create(self):
        # x:1195 y:433, x:135 y:397, x:1125 y:546
        _state_machine = OperatableStateMachine(outcomes=['Given', 'Person_not_found', 'fail'], input_keys=['person_id'])
        _state_machine.userdata.person_id = 0

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

        # x:641 y:299, x:318 y:522
        _sm_give_0 = OperatableStateMachine(outcomes=['failed', 'given'], input_keys=['Object'])

        with _sm_give_0:
            # x:67 y:27
            OperatableStateMachine.add('SetPose',
                                        SetKey(Value="ShowGripper"),
                                        transitions={'done': 'moveArm'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'Key': 'target'})

            # x:53 y:413
            OperatableStateMachine.add('read torque',
                                        ReadTorque(watchdog=5, Joint="right_elbow_pitch_joint", Threshold=2, min_time=1),
                                        transitions={'threshold': 'open gripper', 'watchdog': 'read torque', 'fail': 'arm_problem'},
                                        autonomy={'threshold': Autonomy.Off, 'watchdog': Autonomy.Off, 'fail': Autonomy.Off},
                                        remapping={'torque': 'torque'})

            # x:52 y:500
            OperatableStateMachine.add('open gripper',
                                        SetGripperState(width=0.15, effort=1),
                                        transitions={'object': 'given', 'no_object': 'given'},
                                        autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
                                        remapping={'object_size': 'object_size'})

            # x:64 y:248
            OperatableStateMachine.add('say pull',
                                        SaraSay(sentence="You can pull on it", emotion=1, block=False),
                                        transitions={'done': 'wait 1'},
                                        autonomy={'done': Autonomy.Off})

            # x:64 y:325
            OperatableStateMachine.add('wait 1',
                                        WaitState(wait_time=1),
                                        transitions={'done': 'read torque'},
                                        autonomy={'done': Autonomy.Off})

            # x:57 y:175
            OperatableStateMachine.add('moveArm',
                                        MoveitMove(move=True, waitForExecution=True, group="RightArm"),
                                        transitions={'done': 'say pull', 'failed': 'arm_problem'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'target': 'target'})

            # x:351 y:283
            OperatableStateMachine.add('arm_problem',
                                        SaraSay(sentence="I have a problem with my arm.", emotion=1, block=True),
                                        transitions={'done': 'failed'},
                                        autonomy={'done': Autonomy.Off})


        # x:531 y:121
        _sm_follow_1 = OperatableStateMachine(outcomes=['failed'], input_keys=['ID'])

        with _sm_follow_1:
            # x:30 y:40
            OperatableStateMachine.add('follow',
                                        SaraFollow(distance=1.2),
                                        transitions={'failed': 'failed'},
                                        autonomy={'failed': Autonomy.Off},
                                        remapping={'ID': 'ID'})


        # x:313 y:247, x:301 y:177, x:86 y:292, x:303 y:71, x:88 y:385, x:84 y:479, x:93 y:335, x:89 y:532
        _sm_give_2 = ConcurrencyContainer(outcomes=['failed', 'given', 'person_lost'], input_keys=['ID'], conditions=[
                                        ('failed', [('Give', 'failed')]),
                                        ('given', [('Give', 'given')]),
                                        ('person_lost', [('Follow', 'failed')])
                                        ])

        with _sm_give_2:
            # x:91 y:50
            OperatableStateMachine.add('Follow',
                                        _sm_follow_1,
                                        transitions={'failed': 'person_lost'},
                                        autonomy={'failed': Autonomy.Inherit},
                                        remapping={'ID': 'ID'})

            # x:84 y:164
            OperatableStateMachine.add('Give',
                                        _sm_give_0,
                                        transitions={'failed': 'failed', 'given': 'given'},
                                        autonomy={'failed': Autonomy.Inherit, 'given': Autonomy.Inherit},
                                        remapping={'Object': 'Object'})



        with _state_machine:
            # x:288 y:222
            OperatableStateMachine.add('give',
                                        _sm_give_2,
                                        transitions={'failed': 'log movebase fail', 'given': 'set idle pose', 'person_lost': 'Person_not_found'},
                                        autonomy={'failed': Autonomy.Inherit, 'given': Autonomy.Inherit, 'person_lost': Autonomy.Inherit},
                                        remapping={'ID': 'person_id'})

            # x:815 y:527
            OperatableStateMachine.add('log movebase fail',
                                        LogState(text="giving Failed", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'fail'},
                                        autonomy={'done': Autonomy.Off})

            # x:863 y:76
            OperatableStateMachine.add('set idle pose',
                                        SetKey(Value="IdlePose"),
                                        transitions={'done': 'moveArm2'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'Key': 'target'})

            # x:1174 y:94
            OperatableStateMachine.add('moveArm2',
                                        MoveitMove(move=True, waitForExecution=True, group="RightArm"),
                                        transitions={'done': 'set none', 'failed': 'log moveitfail'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'target': 'target'})

            # x:1167 y:337
            OperatableStateMachine.add('close gripper',
                                        SetGripperState(width=0, effort=1),
                                        transitions={'object': 'Given', 'no_object': 'Given'},
                                        autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
                                        remapping={'object_size': 'object_size'})

            # x:1258 y:255
            OperatableStateMachine.add('remove gripper content',
                                        SetRosParam(ParamName="GripperContent"),
                                        transitions={'done': 'close gripper'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'Value': 'none'})

            # x:1180 y:179
            OperatableStateMachine.add('set none',
                                        SetKey(Value=None),
                                        transitions={'done': 'close gripper'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'Key': 'none'})

            # x:971 y:298
            OperatableStateMachine.add('log moveitfail',
                                        LogState(text="moveit failed", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'fail'},
                                        autonomy={'done': Autonomy.Off})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
