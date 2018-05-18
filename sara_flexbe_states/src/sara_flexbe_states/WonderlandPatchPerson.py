#!/usr/bin/env python
# encoding=utf8

import requests
from flexbe_core import EventState, Logger

"""
Created on 17/05/2018

@author: Lucas Maurice
"""


class WonderlandPatchPerson(EventState):
    '''
    Patch (update) a person.
    >#  entity                  sara_msgs/Entity

    <= done                     return when the add correctly append
    <= dont_exist                return when the entity already exist
    <= bad_request              return when error reading data
    <= error                    return when error reading data
    '''

    def __init__(self):
        # See example_state.py for basic explanations.
        super(WonderlandPatchPerson, self).__init__(input_keys=['entity'],
                                                    outcomes=['done', 'dont_exist', 'bad_request', 'error'])

    def execute(self, userdata):

        # Generate URL to contact
        url = "http://wonderland:8000/api/people/"

        entity = userdata.entity

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
            data.update({'peoplePoseAccuracy': entity.color})

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
            response = requests.patch(url, data=data)
            if response.status_code == 200:
                return 'done'

            elif response.status_code == 404:
                return 'dont_exist'

            elif 400 <= response.status_code < 500:
                Logger.logwarn(response.status_code)
                return 'bad_request'

            else:
                Logger.logerr(response.status_code)
                return 'error'

        except requests.exceptions.RequestException as e:
            Logger.logerr(e)
            return 'error'
