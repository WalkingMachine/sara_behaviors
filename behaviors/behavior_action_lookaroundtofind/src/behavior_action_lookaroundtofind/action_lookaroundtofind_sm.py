#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_action_lookaroundtofind')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.list_entities_by_name import list_entities_by_name
from behavior_action_turn.action_turn_sm import action_turnSM
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_states.for_loop import ForLoop
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sat May 12 2018
@author: Raphaël Duchaîne
'''
class Action_lookAroundToFindSM(Behavior):
    '''
    Cherche et trouve quelque chose. (personne ou objet) en regardant à 360 degrees.
    '''


    def __init__(self):
        super(Action_lookAroundToFindSM, self).__init__()
        self.name = 'Action_lookAroundToFind'

        # parameters of this behavior

        # references to used behaviors
        self.add_behavior(action_turnSM, 'action_turn')

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
        
        # [/MANUAL_INIT]

        # Behavior comments:



    def create(self):
        # x:382 y:411, x:794 y:39
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['name'])
        _state_machine.userdata.name = "apple"

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


        with _state_machine:
            # x:204 y:72
            OperatableStateMachine.add('look1',
                                        list_entities_by_name(frontality_level=0.5),
                                        transitions={'found': 'finished', 'not_found': 'search_around'},
                                        autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
                                        remapping={'name': 'name', 'list_entities_by_name': 'list_entities_by_name', 'number': 'number'})

            # x:738 y:258
            OperatableStateMachine.add('action_turn',
                                        self.use_behavior(action_turnSM, 'action_turn'),
                                        transitions={'finished': 'list_entities_by_name', 'failed': 'search_around'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'rotation': 'rotation'})

            # x:766 y:153
            OperatableStateMachine.add('SetRotation',
                                        SetKey(Value=90),
                                        transitions={'done': 'action_turn'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'Key': 'rotation'})

            # x:624 y:381
            OperatableStateMachine.add('list_entities_by_name',
                                        list_entities_by_name(frontality_level=0.5),
                                        transitions={'found': 'finished', 'not_found': 'search_around'},
                                        autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
                                        remapping={'name': 'name', 'list_entities_by_name': 'list_entities_by_name', 'number': 'number'})

            # x:522 y:87
            OperatableStateMachine.add('search_around',
                                        ForLoop(repeat=3),
                                        transitions={'do': 'SetRotation', 'end': 'failed'},
                                        autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
                                        remapping={'index': 'index'})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
