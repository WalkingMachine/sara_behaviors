#!/usr/bin/env python

from flexbe_core import EventState, Logger
import rospy
import re

class RegexTester(EventState):
    """
    test a regular expressuion

    -- regex     string      regular expression


    <= true
    <= false 
    """

    def __init__(self, regex):
        """Constructor"""

        super(RegexTester, self).__init__(outcomes = ['true','false'], inputdata = ['text'])
        self.test = re.compile(regex)

    def execute(self, userdata):
        """Wait for action result and return outcome accordingly"""

        n = self.test.match(userdata.text)
        if n:
            return 'true'
        return 'true'
