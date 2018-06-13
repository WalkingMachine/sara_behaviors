#!/usr/bin/env python
# encoding=utf8

import json

import requests
from flexbe_core import EventState
from rospy import logerr, loginfo
from sara_msgs.msg import Entity

"""
Created on 09/06/2018

@author: Lucas Maurice
"""


class WonderlandGetPersonStat(EventState):
    '''
    Find a person by ID.
    #> men           Integer    Number of men in the database
    #> women         Integer    Number of women in the database
    #> others        Integer    Number of others in the database

    <= done             return when one or more person exist
    <= none             return when no person exist
    <= error            return when error reading data
    '''

    def __init__(self):
        # See example_state.py for basic explanations.
        super(WonderlandGetPersonStat, self).__init__(outcomes=['done', 'none', 'error'],
                                                      output_keys=['women', 'men', 'others'])
        self.url = "http://wonderland:8000/api/people/"

    def execute(self, userdata):
        women = 0
        men = 0
        others = 0

        # try the request
        try:
            response = requests.get(self.url)
        except requests.exceptions.RequestException as e:
            logerr(e)
            return 'error'

        # parse parameter json data
        data = json.loads(response.content)

        loginfo(data)

        if len(data) <= 0:
            return 'none'

        for person in data:
            if 'peopleGender' in person and (person['peopleGender'] == 'male' or person['peopleGender'] == 'boy'):
                men += 1
            elif 'peopleGender' in person and (person['peopleGender'] == 'female' or person['peopleGender'] == 'girl'):
                women += 1
            else:
                others += 1

        userdata.women = women
        userdata.men = men
        userdata.others = others

        return 'done'
