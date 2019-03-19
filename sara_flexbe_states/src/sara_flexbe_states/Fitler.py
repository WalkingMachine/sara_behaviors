#!/usr/bin/env python

import rospy
from flexbe_core import EventState, Logger

'''
Created on 18.03.2019

@author: Huynh-Anh Le
'''


class Filter(EventState):
    '''
    ALlows the user to filter some data

    -- filter  function	     ALlows the user to filter/sort data

    ># input_list  list		Input to the filter function

    #> output_list list		The result of the filter.

    <= done					Indicates completion of the filter.

    '''

    def __init__(self, filter):
        '''
        Constructor
        '''
        super(Filter, self).__init__(outcomes=['done'],
                                               input_keys=['input_list'],
                                               output_keys=['output_list'])

        self.filter = filter

    def execute(self, userdata):
        '''Execute this state'''

        userdata.output_list = self.filterbyvalue(userdata.input_list,self.filter)
        print(userdata.input_list)
        print(userdata.output_list)

        # nothing to check
        return 'done'

    def filterbyvalue(self, seq, filter):
        for el in seq:
            if filter(el): yield el
