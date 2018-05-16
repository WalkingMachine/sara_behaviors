#!/usr/bin/env python
# encoding=utf8

import json

import requests
from flexbe_core import EventState
from rospy import logerr, logwarn, loginfo
from sara_msgs.msg import Entity

"""
Created on 15/05/2018

@author: Lucas Maurice
"""


class WonderlandGetEntityByID(EventState):
    '''
    Read the position of a room in a json string
    ># id               int     The id of the entity in the database
    #> entity           Entity  The entity following the `sara_msgs/entity.msg` structure
    #> depth_position   int     The accuracy of the position (Number of chained container for have value)
    #> depth_waypoint   int     The accuracy of the waypoint (Number of chained container for have value)

    <= found            returned when at least one entity exist
    <= not_found        returned when no entity have the selected name
    <= error            returned when am error happen during the HTTP request
    '''

    def __init__(self):
        # See example_state.py for basic explanations.
        super(WonderlandGetEntityByID, self).__init__(outcomes=['found', 'not_found', 'error'],
                                                      input_keys=['id'],
                                                      output_keys=['entity', 'depth_position', 'depth_waypoint'])

    def execute(self, userdata):
        # Generate URL to contact
        url = "http://wonderland:8000/api/entity?entityId=" + str(userdata.id)

        # try the request
        try:
            response = requests.get(url)
            print(response)
        except requests.exceptions.RequestException as e:
            logerr(e)
            return 'error'

        # parse parameter json data
        data = json.loads(response.content)

        if 'entityId' not in data:
            logwarn("Object %i do not exist in Wonderland", userdata.id)
            return 'not_found'

        entity = Entity()

        entity.wonderlandId = data['entityId']
        if 'entityName' in data:
            entity.aliases.append(data['entityName'].encode('ascii', 'ignore'))

        # Description of the object:
        if 'entityClass' in data and data['entityClass'] is not None:
            entity.name = data['entityClass'].encode('ascii', 'ignore')
        if 'entityCategory' in data and data['entityCategory'] is not None:
            entity.category = data['entityCategory'].encode('ascii', 'ignore')
        if 'entityColor' in data and data['entityColor'] is not None:
            entity.color = data['entityColor'].encode('ascii', 'ignore')

        # Physical description of the object:
        entity.weight = data['entityWeight']
        entity.size = data['entitySize']

        # Location of the object
        entity.position.x = data['entityPosX']
        entity.position.y = data['entityPosY']
        entity.position.z = data['entityPosZ']
        # Add if needed: 'entityPosYaw' ; 'entityPosPitch' ; 'entityPosRoll'

        entity.waypoint.x = data['entityWaypointX']
        entity.waypoint.y = data['entityWaypointY']
        entity.waypoint.theta = data['entityWaypointYaw']

        entity.containerId = data['entityContainer']

        loginfo(entity)

        userdata.entity = entity
        userdata.depth_position = data['depth_position']
        userdata.depth_waypoint = data['depth_waypoint']

        return 'found'
