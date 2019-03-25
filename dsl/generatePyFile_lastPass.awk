        BEGIN{
            LINT=true;
        }

        NR==1{
            print "#!/usr/bin/env python\n\
# -*- coding: utf-8 -*- \n\
###########################################################\n\
#               WARNING: Generated code!                  #\n\
#              **************************                 #\n\
# Manual changes may get lost if file is generated again. #\n\
# Only code inside the [MANUAL] tags will be kept.        #\n\
###########################################################\n\
\n\
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger\n\
from flexbe_states.decision_state import DecisionState\n\
# Additional imports can be added inside the following tags\n\
# [MANUAL_IMPORT]\n\
\n\
# [/MANUAL_IMPORT]\n\
\n\
\n\
'''\n\
@author: Raphaël Duchaîne\n\
'''\n\
class "$0"SM(Behavior):\n\
    '''\n\
    Behavior to test dsl parsing to flexbe\n\
    '''\n\
\n\
\n\
    def __init__(self):\n\
        super("$0"SM, self).__init__()\n\
        self.name = '"$0"'\n\
\n\
        # parameters of this behavior\n\
\n\
        # references to used behaviors\n\
\n\
        # Additional initialization code can be added inside the following tags\n\
        # [MANUAL_INIT]\n\
    \n\
        # [/MANUAL_INIT]\n\
\n\
        # Behavior comments:\n\
\n\
\n\
\n\
    def create(self):\n\
        # x:1200 y:570, x:12 y:570\n\
        _state_machine = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['input_value'])\n\
        _state_machine.userdata.input_value = ''";
            for(i=1; i<lineCount-2; i++){
                print "\n\
        # x:130 y:465, x:230 y:465\n\
        _sm_group_0"i" = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['input_value'])\n\
\n\
        with _sm_group_0"i":\n\
            # x:98 y:96\n\
            OperatableStateMachine.add('0"i"',\n\
                                    DecisionState(outcomes=['done','failed'], conditions=lambda x:'done'),\n\
                                    transitions={'done': 'done', 'failed': 'failed'},\n\
                                    autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},\n\
                                    remapping={'input_value': 'input_value'})";
            }
            print "\n\
        with _state_machine:";
        }

# /.* \? .* (: .*)?/
        NR>3{
            parent =$1
            good_child = $3
            bad_child = $5

            print "\n\
            # x:"181" y:"(NR-3)*60+34"\n\
            OperatableStateMachine.add('"parent"',\n\
                                    _sm_group_0"NR-3",\n\
                                    transitions={'done': '"good_child"', 'failed': '"bad_child"'},\n\
                                    autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},\n\
                                    remapping={'input_value': 'input_value'})";
        }

        END{
            print "\n\
        return _state_machine\n\n";
        }
