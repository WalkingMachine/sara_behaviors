#!/usr/bin/env python
# encoding=utf8

import json

import requests
from flexbe_core import EventState, Logger

"""
Created on 17/05/2018

@author: Lucas Maurice
"""


class WonderlandAddUpdatePeople(EventState):
    '''
    Add or update all known persons in wonderland.

    <= done                     return when the add correctly append
    '''

    def __init__(self):
        # See example_state.py for basic explanations.
        super(WonderlandAddUpdatePeople, self).__init__(outcomes=['done'])
        self.url = "http://wonderland:8000/api/people/"

    def execute(self, userdata):
        # Generate URL to contact
        s = 0

    def add_person(self, entity):
        data = {}

        if entity.face.id is not None:
            data.update({'peopleRecognitionId': entity.face.id})

        if entity.color is not None:
            data.update({'peopleColor': entity.color})

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
            response = requests.post(self.url, data=data)
            if response.status_code == 201:
                return 0

            elif 400 <= response.status_code < 500:
                Logger.logwarn(response.status_code)
                data = json.loads(response.content)
                if 'peopleRecognitionId' in data and data['peopleRecognitionId'][0] \
                        == u'people with this peopleRecognitionId already exists.':
                    return 1
                else:
                    return -1
            else:
                Logger.logerr(response.status_code)
                return -1

        except requests.exceptions.RequestException as e:
            Logger.logerr(e)
            return -1

    def update_person(self, entity):
        data = {}

        if entity.wonderlandId is None and entity.face.id is None:
            Logger.logwarn('Need wonderland ID or face ID !')
            return 'bad_request'

        if entity.wonderlandId is not None:
            data.update({'peopleId': entity.wonderlandId})

        if entity.face.id is not None:
            data.update({'peopleRecognitionId': entity.face.id})

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

        if entity.isOperator is not None:
            data.update({'peopleIsOperator': entity.isOperator})

        if len(entity.aliases) > 0:
            data.update({'peopleName': entity.aliases[0]})

        # try the request
        try:
            response = requests.patch(self.url, data=data)
            if response.status_code == 200:
                return 0

            elif response.status_code == 404:
                Logger.logwarn("Bad Request")
                return 1

            elif 400 <= response.status_code < 500:
                Logger.logwarn(response.status_code)
                Logger.logwarn("Bad Request")
                return -1

            else:
                Logger.logerr(response.status_code)
                Logger.logwarn("Bad Request")
                return -1

        except requests.exceptions.RequestException as e:
            Logger.logerr(e)
            return -1
