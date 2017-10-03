#!/usr/bin/env python
# encoding=utf8

from flexbe_core import EventState, Logger


class test_log(EventState):
    '''
    Print a log in console.
    
    ># text     object  object to print
    
    <= done     done
    '''

    def __init__(self):
        super(test_log, self).__init__(outcomes=['done'], input_keys=['text'])

    def execute(self, userdata):
        print userdata.text
        return 'done'
