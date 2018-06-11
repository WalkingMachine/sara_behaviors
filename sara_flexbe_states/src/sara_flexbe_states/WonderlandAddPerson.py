#!/usr/bin/env python
# encoding=utf8

import json

import requests
from flexbe_core import EventState, Logger

"""
Created on 17/05/2018

@author: Lucas Maurice
"""


class WonderlandAddPerson(EventState):
    '''
    Add a person.
    >#  entity                  sara_msgs/Entity    an entity

    <= done                     return when the add correctly append
    <= already_exit             return when the entity already exist
    <= bad_request              return when error reading data
    <= error                    return when error reading data
    '''

    def __init__(self):
        # See example_state.py for basic explanations.
        super(WonderlandAddPerson, self).__init__(input_keys=['entity'],
                                                  outcomes=['done', 'already_exit', 'bad_request', 'error'])

    def execute(self, userdata):
        # Generate URL to contact
        url = "http://wonderland:8000/api/people/"

        entity = userdata.entity

        data = {}

        if entity.ID is not None:
            data.update({'peopleRecognitionId': entity.ID})

        if entity.color is not None:
            data.update({'peopleColor': entity.color})

        if entity.pose is not None:
            data.update({'peoplePose': entity.pose})

        if entity.poseProbability is not None:
            data.update({'peoplePoseAccuracy': entity.poseProbability})

        if entity.face.gender is not None:
            data.update({'peopleGender': entity.face.gender})

        if entity.face.genderProbability is not None:
            data.update({'peopleGenderAccuracy': entity.face.genderProbability})

        if entity.face.emotion is not None:
            data.update({'peopleEmotion': entity.face.emotion})

        if entity.face.emotionProbability is not None:
            data.update({'peopleEmotionAccuracy': entity.face.emotionProbability})

        if entity.face.emotion is not None:
            data.update({'peopleEmotion': entity.face.emotion})

        if entity.face.emotionProbability is not None:
            data.update({'peopleEmotionAccuracy': entity.face.emotionProbability})

        if entity.isOperator is None:
            data.update({'peopleIsOperator': False})
        else:
            data.update({'peopleIsOperator': entity.isOperator})

        if len(entity.aliases) > 0:
            data.update({'peopleName': entity.aliases[0]})

        # try the request
        try:
            response = requests.post(url, data=data)
            if response.status_code == 201:
                return 'done'

            elif 400 <= response.status_code < 500:
                Logger.logwarn(response.status_code)
                data = json.loads(response.content)
                if 'peopleRecognitionId' in data and data['peopleRecognitionId'][0]\
                        == u'people with this peopleRecognitionId already exists.':
                    return 'already_exit'
                else:
                    return 'bad_request'
            else:
                Logger.logerr(response.status_code)
                return 'error'

        except requests.exceptions.RequestException as e:
            Logger.logerr(e)
            return 'error'
