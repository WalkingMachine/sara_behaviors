#!/usr/bin/env python

from flexbe_core import EventState, Logger
import rospy
import re

class RegexTester(EventState):
    """
    test a regular expression

    -- regex     string      regular expression. e.g. ".*hello my ((brother)|(sister))s?"
    


    <= true   true
    <= false   false
    """

    def __init__(self, regex):
        """Constructor"""

        super(RegexTester, self).__init__(outcomes = ['true','false'], input_keys = ['text'], output_keys = ['result'])
        self.test = re.compile(regex)

    def execute(self, userdata):
        """Wait for action result and return outcome accordingly"""

        n = self.test.match(str(userdata.text).lower())
        if n:
            return 'true'
        return 'false'
