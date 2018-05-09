#!/usr/bin/env python
# encoding=utf8

from flexbe_core import EventState, Logger
import json
import requests



class WonderlandEntityNameByID(EventState):
    '''
    Read the position of a room in a json string
    ># id                int     id of the room

    #> entityClass       string   of the entity
    #> entityName        string   of the entity
    #> entityCategory    string   of the entity
    #> entityColor       string   of the entity
    #> entityWeight      string   of the entity
    #> entitySize        string   of the entity
    #> entityContainer   string   of the entity

    #> entityPosX        float   position of the entity
    #> entityPosY        float   position of the entity
    #> entityPosZ        float   position of the entity
    #> entityPosYaw      float   position of the entity
    #> entityPosPitch    float   position of the entity
    #> entityPosRoll     float   position of the entity

    #> entityWaypointX   float   position of the position to reach for have the object
    #> entityWaypointY   float   position of the position to reach for have the object
    #> entityWaypointYaw float   position of the position to reach for have the object

    #> depth_waypoint    float   position of the room
    #> depth_position    float   position of the room

    <= done              return when at least one entity exist
    <= none              return when no entity have the selected name
    <= error             return when error reading data
    '''

    def __init__(self):
        # See example_state.py for basic explanations.
        super(WonderlandEntityNameByID, self).__init__(outcomes=['done', 'none', 'error'],
                                                       input_keys=['id'],
                                                       output_keys=['entityClass', 'entityName', 'entityCategory',
                                                                    'entityColor', 'entityWeight', 'entitySize',
                                                                    'entityContainer', 'entityPosX', 'entityPosY',
                                                                    'entityPosZ', 'entityPosYaw', 'entityPosPitch',
                                                                    'entityPosRoll', 'entityWaypointX',
                                                                    'entityWaypointY', 'entityWaypointYaw'])

    def execute(self, userdata):
        # Generate URL to contact
        url = "http://wonderland:8000/api/entity?entityId="+str(userdata.id)

        print("This")
        print("Is")
        print("A")
        print("Test")

        # try the request
        try:
            response = requests.get(url)
            print(response)
        except requests.exceptions.RequestException as e:
            print(e)
            return 'error'

        # parse parameter json data
        data = json.loads(response.content)

        if not 'entityClass' in data:
            return 'none'

        # write return data
        userdata.entityClass = data['entityClass']
        userdata.entityName = data['entityName']
        userdata.entityCategory = data['entityCategory']
        userdata.entityColor = data['entityColor']
        userdata.entityWeight = data['entityWeight']
        userdata.entitySize = data['entitySize']
        userdata.entityContainer = data['entityContainer']

        userdata.entityPosX = data['entityPosX']
        userdata.entityPosY = data['entityPosY']
        userdata.entityPosZ = data['entityPosZ']
        userdata.entityPosYaw = data['entityPosYaw']
        userdata.entityPosPitch = data['entityPosPitch']
        userdata.entityPosRoll = data['entityPosRoll']

        userdata.entityWaypointX = data['entityWaypointX']
        userdata.entityWaypointY = data['entityWaypointY']
        userdata.entityWaypointYaw = data['entityWaypointYaw']

        userdata.depth_waypoint = data['depth_waypoint']
        userdata.depth_position = data['depth_position']

        return 'done'