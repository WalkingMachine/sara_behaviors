#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_test_continue')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.lu4r_parser import LU4R_Parser
from flexbe_states.log_key_state import LogKeyState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Tue Jul 25 2017
@author: Philippe la Madeleine
'''
class Test_continueSM(Behavior):
    '''
    test the continue button
    '''


    def __init__(self):
        super(Test_continueSM, self).__init__()
        self.name = 'Test_continue'

        # parameters of this behavior

        # references to used behaviors

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]

	# [/MANUAL_INIT]

        # Behavior comments:



    def create(self):
        # x:649 y:285, x:641 y:194
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
        _state_machine.userdata.sentence = "bring the cup from the table to the room"
        _state_machine.userdata.HighFIFO = []
        _state_machine.userdata.MedFIFO = []
        _state_machine.userdata.LowFIFO = []
        _state_machine.userdata.DoNow = []

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]

		# [/MANUAL_CREATE]


        with _state_machine:
            # x:206 y:70
            OperatableStateMachine.add('parse lu4r',
                                        LU4R_Parser(),
                                        transitions={'done': 'log', 'fail': 'finished'},
                                        autonomy={'done': Autonomy.Off, 'fail': Autonomy.Off},
                                        remapping={'sentence': 'sentence', 'HighFIFO': 'HighFIFO', 'MedFIFO': 'MedFIFO', 'LowFIFO': 'LowFIFO', 'DoNow': 'DoNow'})

            # x:360 y:267
            OperatableStateMachine.add('log',
                                        LogKeyState(text="{}", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'failed'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'data': 'MedFIFO'})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]

	# [/MANUAL_FUNC]
