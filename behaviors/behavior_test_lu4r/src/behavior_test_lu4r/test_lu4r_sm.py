#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_test_lu4r')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.lu4r_parser import LU4R_Parser
from sara_flexbe_states.string_list_logger import StringListLogger
from flexbe_states.calculation_state import CalculationState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Jul 10 2017
@author: Philippe La Madeleine
'''
class Test_LU4RSM(Behavior):
    '''
    behavior to test LU4R
    '''


    def __init__(self):
        super(Test_LU4RSM, self).__init__()
        self.name = 'Test_LU4R'

        # parameters of this behavior

        # references to used behaviors

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
        
        # [/MANUAL_INIT]

        # Behavior comments:



    def create(self):
        # x:30 y:322, x:130 y:322
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
        _state_machine.userdata.sentence = "go to the soda"
        _state_machine.userdata.HighFIFO = []
        _state_machine.userdata.MedFIFO = []
        _state_machine.userdata.LowFIFO = []
        _state_machine.userdata.DoNow = ["test"]

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


        with _state_machine:
            # x:254 y:108
            OperatableStateMachine.add('lu4r',
                                        LU4R_Parser(),
                                        transitions={'done': 'dd', 'fail': 'finished'},
                                        autonomy={'done': Autonomy.Off, 'fail': Autonomy.Off},
                                        remapping={'sentence': 'sentence', 'HighFIFO': 'HighFIFO', 'MedFIFO': 'MedFIFO', 'LowFIFO': 'LowFIFO', 'DoNow': 'DoNow'})

            # x:220 y:216
            OperatableStateMachine.add('log',
                                        StringListLogger(),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'List': 'ActionForm1'})

            # x:362 y:172
            OperatableStateMachine.add('dd',
                                        CalculationState(calculation=lambda x: x[0]),
                                        transitions={'done': 'log'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'input_value': 'MedFIFO', 'output_value': 'ActionForm1'})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
