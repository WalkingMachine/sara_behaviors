#!/usr/bin/env python

from flexbe_core import EventState, Logger
import rospy
from gender_age_service.srv import ListGenderPrediction, ListGenderPredictionRequest


class GenderAgeRecognition(EventState):
    '''
    Finding the gender and an age range of a person

    ># image         image with a face

    #> ageMin        low range age
    #> ageMax        high range age
    #> probAge       age range probability
    #> probFemale    female probability
    #> probMale      male probability
    <= success       face has been classified
    <= fail          no face fined
    '''

    def __init__(self):
        """Constructor"""
        super(GenderAgeRecognition, self).__init__(outcomes=['success', 'fail'], input_keys=['image'],
                                                   output_keys=['ageMin', 'ageMax', 'probAge', 'probMale',
                                                                'probFemale'])
        Logger.loginfo('Initialisation')
        self.msg = ListGenderPredictionRequest()

    def execute(self, userdata):
        """Return the data of GenderAgeClassification"""
        self.msg.image = userdata.image

        Logger.loginfo('Wait for service')
        rospy.wait_for_service('/prediction')
        serv = rospy.ServiceProxy('/prediction', ListGenderPrediction)
        resp = serv(self.msg)

        Logger.loginfo('Responce received')
        if resp.listPrediction[0].ageMax is not 0 and resp.listPrediction[0].ageMin is not 0:
            userdata.ageMin = resp.listPrediction[0].ageMin
            userdata.ageMax = resp.listPrediction[0].ageMax
            userdata.probAge = resp.listPrediction[0].probAge
            userdata.probFemale = resp.listPrediction[0].probFemale
            userdata.probMale = resp.listPrediction[0].probMale
            return 'success'
        else:
            return 'fail'
