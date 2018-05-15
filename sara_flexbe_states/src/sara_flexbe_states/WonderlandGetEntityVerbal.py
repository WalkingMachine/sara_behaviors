#!/usr/bin/env python
# encoding=utf8

import json

import requests
from flexbe_core import EventState
from rospy import logerr, logwarn, loginfo
from sara_msgs.msg import Entity, Entities


class WonderlandGetEntityVerbal(EventState):
    '''
    Read the position of a room in a json string
    ># name             string         Recognition name of the object
    ># containers       string array   Array of containers recognition name (can be empty) on single container

    #> entities         sara_msgs/Entities

    <= one              return when one entity exist
    <= multiple         return when more than one entity exist
    <= none             return when no entity exist
    <= error            return when error reading data
    '''

    def __init__(self):
        # See example_state.py for basic explanations.
        super(WonderlandGetEntityVerbal, self).__init__(outcomes=['one', 'multiple', 'none', 'error'],
                                                        input_keys=['name', 'containers'],
                                                        output_keys=['entities'])

    def execute(self, userdata):
        # Generate URL to contact

        if type(userdata.name) is str:
            url = "http://wonderland:8000/api/entity?entityClass=" + str(userdata.name)
        else:
            url = "http://wonderland:8000/api/entity?none"

        if type(userdata.containers) is str:
            url += "&entityContainer=" + userdata.containers

        elif type(userdata.containers) is list:
            for container in userdata.containers:
                if type(container) == "str":
                    url += "&entityContainer=" + container

        logwarn(url)

        # try the request
        try:
            response = requests.get(url)
        except requests.exceptions.RequestException as e:
            logerr(e)
            return 'error'

        # parse parameter json data
        data = json.loads(response.content)

        loginfo(data)

        if len(data) == 0:
            return 'none'
        elif len(data) == 1:
            entity = Entity()
            userdata.entities = entity
            return 'one'

        else:
            entities = Entities()
            userdata.entities = entities
            return 'multiple'
