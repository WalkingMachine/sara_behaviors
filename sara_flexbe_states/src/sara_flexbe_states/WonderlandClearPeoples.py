#!/usr/bin/env python
# encoding=utf8

import requests
from flexbe_core import EventState
from rospy import logerr, loginfo

"""
Created on 09/06/2018

@author: Lucas Maurice
"""


class WonderlandClearPeoples(EventState):
    '''
    Reset the people list in Wonderland. To use with care !
    '''

    def __init__(self):
        # See example_state.py for basic explanations.
        super(WonderlandClearPeoples, self).__init__(outcomes=['done', 'error'])
        self.url = "http://wonderland:8000/api/clear-people/"

    def execute(self, userdata):

        # try the request
        try:
            response = requests.delete(self.url)
            loginfo(response)
        except requests.exceptions.RequestException as e:
            logerr(e)
            return 'error'

        return 'done'
