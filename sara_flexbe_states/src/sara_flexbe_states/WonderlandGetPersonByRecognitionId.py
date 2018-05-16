#!/usr/bin/env python
# encoding=utf8

import json

import requests
from flexbe_core import EventState
from rospy import logerr, loginfo
from sara_msgs.msg import Entity

"""
Created on 15/05/2018

@author: Lucas Maurice
"""


class WonderlandGetPersonByRecognitionId(EventState):
    '''
    Find a person by ID.
    ># id               int         Recognition name of the object

    #> entity           sara_msgs/Entity

    <= done             return when one entity exist
    <= none             return when no entity exist
    <= error            return when error reading data
    '''

    def __init__(self):
        # See example_state.py for basic explanations.
        super(WonderlandGetPersonByRecognitionId, self).__init__(outcomes=['done', 'none', 'error'],
                                                                 input_keys=['id'], output_keys=['entity'])

    def execute(self, userdata):
        # Generate URL to contact

        url = "http://wonderland:8000/api/people/?peopleRecognitionId=" + str(userdata.id)

        # try the request
        try:
            response = requests.get(url)
        except requests.exceptions.RequestException as e:
            logerr(e)
            return 'error'

        # parse parameter json data
        data = json.loads(response.content)

        loginfo(data)

        if 'peopleId' in data:
            userdata.entity = self.generate_entity(data)
            return 'done'
        else:
            return 'none'

    @staticmethod
    def generate_entity(data):
        entity = Entity()

        entity.wonderlandId = data['peopleId']
        entity.face.id = data['peopleRecognitionId']

        if 'peopleColor' in data and data['peopleColor'] is not None:
            entity.color = data['peopleColor'].encode('ascii', 'ignore')

        if 'peopleName' in data:
            entity.aliases.append(data['peopleName'].encode('ascii', 'ignore'))

        if 'peoplePose' in data and data['peoplePose'] is not None:
            entity.pose = data['peoplePose'].encode('ascii', 'ignore')
        entity.poseProbability = data['peopleGenderAccuracy']

        if 'peopleGender' in data and data['peopleGender'] is not None:
            entity.face.gender = data['peopleGender'].encode('ascii', 'ignore')
        entity.face.genderProbability = data['peopleGenderAccuracy']

        if 'peopleEmotion' in data and data['peopleEmotion'] is not None:
            entity.face.emotion = data['peopleEmotion'].encode('ascii', 'ignore')
        entity.face.emotionProbability = data['peopleEmotionAccuracy']

        entity.isOperator = data['peopleIsOperator']

        loginfo(entity)

        return entity
