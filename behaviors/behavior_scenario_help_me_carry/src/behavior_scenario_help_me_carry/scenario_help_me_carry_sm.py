#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_scenario_help_me_carry')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.AMCL_initial_pose import AmclInit
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.GetPersonID import GetPersonID
from flexbe_states.wait_state import WaitState
from sara_flexbe_states.for_state import ForState
from sara_flexbe_states.GetIDPose import GetIDPose
from sara_flexbe_states.sara_move_base import SaraMoveBase
from sara_flexbe_states.get_robot_pose import Get_Robot_Pose
from sara_flexbe_states.compare_poses import ComparePoses
from flexbe_states.check_condition_state import CheckConditionState
from flexbe_states.subscriber_state import SubscriberState
from sara_flexbe_states.regex_tester import RegexTester
from flexbe_states.calculation_state import CalculationState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu Jul 27 2017
@author: Philippe La Madeleine
'''
class Scenario_Help_me_carrySM(Behavior):
    '''
    Help_me_carry
    '''


    def __init__(self):
        super(Scenario_Help_me_carrySM, self).__init__()
        self.name = 'Scenario_Help_me_carry'

        # parameters of this behavior

        # references to used behaviors

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
        
        # [/MANUAL_INIT]

        # Behavior comments:



    def create(self):
        # x:733 y:345, x:291 y:142
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
        _state_machine.userdata.car = false

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

        # x:30 y:308, x:130 y:308, x:230 y:308
        _sm_get_operator_pose_0 = OperatableStateMachine(outcomes=['failed', 'lost', 'done'], input_keys=['person_id'], output_keys=['pose'])

        with _sm_get_operator_pose_0:
            # x:62 y:124
            OperatableStateMachine.add('get pose',
                                        GetIDPose(),
                                        transitions={'done': 'done', 'lost': 'lost', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'lost': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'person_id': 'person_id', 'person_pose': 'pose'})


        # x:646 y:266
        _sm_listen_1 = OperatableStateMachine(outcomes=['fail'], input_keys=['car'])

        with _sm_listen_1:
            # x:152 y:129
            OperatableStateMachine.add('listen for order',
                                        SubscriberState(topic="/speach", blocking=True, clear=True),
                                        transitions={'received': 'calc', 'unavailable': 'listen for order'},
                                        autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
                                        remapping={'message': 'message'})

            # x:589 y:95
            OperatableStateMachine.add('test',
                                        RegexTester(regex=".*[Ss]top.*"),
                                        transitions={'true': 'listen for order', 'false': 'listen for order'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                        remapping={'text': 'text', 'result': 'car'})

            # x:381 y:216
            OperatableStateMachine.add('calc',
                                        CalculationState(calculation=lambda x: x.data),
                                        transitions={'done': 'test'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'input_value': 'message', 'output_value': 'text'})


        # x:384 y:427, x:823 y:153
        _sm_follow_2 = OperatableStateMachine(outcomes=['failed', 'finished'], input_keys=['person_id', 'car'])

        with _sm_follow_2:
            # x:49 y:53
            OperatableStateMachine.add('Get operator pose',
                                        _sm_get_operator_pose_0,
                                        transitions={'failed': 'failed', 'lost': 'for', 'done': 'get robot pose'},
                                        autonomy={'failed': Autonomy.Inherit, 'lost': Autonomy.Inherit, 'done': Autonomy.Inherit},
                                        remapping={'person_id': 'person_id', 'pose': 'pose'})

            # x:792 y:41
            OperatableStateMachine.add('move',
                                        SaraMoveBase(),
                                        transitions={'arrived': 'cond', 'failed': 'failed'},
                                        autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'pose': 'pose'})

            # x:387 y:129
            OperatableStateMachine.add('say stop',
                                        SaraSay(sentence="Wait for me. I've lost you. Stay still until I find you again.", emotion=1),
                                        transitions={'done': 'Get operator pose'},
                                        autonomy={'done': Autonomy.Off})

            # x:380 y:239
            OperatableStateMachine.add('for',
                                        ForState(repeat=3),
                                        transitions={'do': 'say stop', 'end': 'failed'},
                                        autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
                                        remapping={'index': 'index'})

            # x:163 y:518
            OperatableStateMachine.add('get robot pose',
                                        Get_Robot_Pose(blocking=True, clear=False),
                                        transitions={'done': 'compare poses', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'pose': 'pose_robot'})

            # x:487 y:517
            OperatableStateMachine.add('compare poses',
                                        ComparePoses(),
                                        transitions={'done': 'move'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'pose_robot': 'pose_robot', 'pose_other': 'pose', 'pose': 'pose'})

            # x:370 y:31
            OperatableStateMachine.add('cond',
                                        CheckConditionState(predicate=lambda x: x),
                                        transitions={'true': 'finished', 'false': 'Get operator pose'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                        remapping={'input_value': 'car'})


        # x:313 y:60, x:320 y:223, x:230 y:308, x:299 y:117, x:430 y:322
        _sm_follow_operator_3 = ConcurrencyContainer(outcomes=['finished', 'failed'], input_keys=['person_id', 'car'], conditions=[
                                        ('failed', [('follow', 'failed')]),
                                        ('failed', [('listen', 'fail')]),
                                        ('finished', [('follow', 'finished')])
                                        ])

        with _sm_follow_operator_3:
            # x:87 y:42
            OperatableStateMachine.add('follow',
                                        _sm_follow_2,
                                        transitions={'failed': 'failed', 'finished': 'finished'},
                                        autonomy={'failed': Autonomy.Inherit, 'finished': Autonomy.Inherit},
                                        remapping={'person_id': 'person_id', 'car': 'car'})

            # x:87 y:211
            OperatableStateMachine.add('listen',
                                        _sm_listen_1,
                                        transitions={'fail': 'failed'},
                                        autonomy={'fail': Autonomy.Inherit},
                                        remapping={'car': 'car'})


        # x:30 y:308, x:130 y:308
        _sm_find_operator_4 = OperatableStateMachine(outcomes=['finished', 'failed'], output_keys=['person_id'])

        with _sm_find_operator_4:
            # x:121 y:126
            OperatableStateMachine.add('get id',
                                        GetPersonID(),
                                        transitions={'done': 'finished', 'failed': 'failed', 'notfound': 'wait'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off, 'notfound': Autonomy.Off},
                                        remapping={'person_id': 'person_id'})

            # x:416 y:89
            OperatableStateMachine.add('wait',
                                        WaitState(wait_time=1),
                                        transitions={'done': 'get id'},
                                        autonomy={'done': Autonomy.Off})


        # x:30 y:322, x:130 y:322
        _sm_wait_for_operator_5 = OperatableStateMachine(outcomes=['found', 'fail'])

        with _sm_wait_for_operator_5:
            # x:16 y:156
            OperatableStateMachine.add('say',
                                        SaraSay(sentence="I'm ready to star carrying groceries", emotion=1),
                                        transitions={'done': 'found'},
                                        autonomy={'done': Autonomy.Off})



        with _state_machine:
            # x:57 y:52
            OperatableStateMachine.add('init amcl',
                                        AmclInit(x=0.494079113007, y=0.182213068008, z=0, ox=0, oy=0, oz=-0.00849557845025, ow=0.999963911922),
                                        transitions={'done': 'wait for operator', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'pose': 'pose'})

            # x:46 y:131
            OperatableStateMachine.add('wait for operator',
                                        _sm_wait_for_operator_5,
                                        transitions={'found': 'instruct operator', 'fail': 'failed'},
                                        autonomy={'found': Autonomy.Inherit, 'fail': Autonomy.Inherit})

            # x:54 y:225
            OperatableStateMachine.add('instruct operator',
                                        SaraSay(sentence="Please, let me look at you closely", emotion=1),
                                        transitions={'done': 'find operator'},
                                        autonomy={'done': Autonomy.Off})

            # x:206 y:543
            OperatableStateMachine.add('instruct2',
                                        SaraSay(sentence="I need you to stand in frond of me", emotion=1),
                                        transitions={'done': 'wait'},
                                        autonomy={'done': Autonomy.Off})

            # x:49 y:333
            OperatableStateMachine.add('find operator',
                                        _sm_find_operator_4,
                                        transitions={'finished': 'perfect', 'failed': 'instruct2'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'person_id': 'person_id'})

            # x:67 y:543
            OperatableStateMachine.add('wait',
                                        WaitState(wait_time=10),
                                        transitions={'done': 'For'},
                                        autonomy={'done': Autonomy.Off})

            # x:69 y:436
            OperatableStateMachine.add('For',
                                        ForState(repeat=3),
                                        transitions={'do': 'find operator', 'end': 'say sorry'},
                                        autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
                                        remapping={'index': 'index'})

            # x:276 y:437
            OperatableStateMachine.add('say sorry',
                                        SaraSay(sentence="Sorry, I don't seem to be able to find you", emotion=1),
                                        transitions={'done': 'failed'},
                                        autonomy={'done': Autonomy.Off})

            # x:345 y:340
            OperatableStateMachine.add('perfect',
                                        SaraSay(sentence="Perfect! I'm now ready to follow you. Please, tell me to stop when we arrive", emotion=1),
                                        transitions={'done': 'Follow operator'},
                                        autonomy={'done': Autonomy.Off})

            # x:480 y:332
            OperatableStateMachine.add('Follow operator',
                                        _sm_follow_operator_3,
                                        transitions={'finished': 'finished', 'failed': 'operator lost'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'person_id': 'person_id', 'car': 'car'})

            # x:496 y:136
            OperatableStateMachine.add('operator lost',
                                        SaraSay(sentence="Sorry, I can't find you.", emotion=1),
                                        transitions={'done': 'failed'},
                                        autonomy={'done': Autonomy.Off})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
