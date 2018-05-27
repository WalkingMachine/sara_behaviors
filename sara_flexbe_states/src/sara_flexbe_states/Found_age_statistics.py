#!/usr/bin/env python

from flexbe_core import EventState, Logger
import rospy
from gender_age_service.srv import ListGenderPrediction, ListGenderPredictionRequest


class Found_age_statitics(EventState):
    '''
    Output the age statistics of a group of people

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
        super(Found_age_statitics, self).__init__(outcomes=['People_found', 'Nobody_found'], input_keys=['image'],
                                                   output_keys=['nbOfFrom0to2', 'nbOfFrom3to6', 'nbOfFrom7to13','nbOfFrom14to22','nbOfFrom23to34','nbOfFrom35to45','nbOfFrom46to56',
                                                                'nbOfFrom57to100','nbOfKids','nbOfTeenagers','nbOfAdults','listPrediction'])
        Logger.loginfo('Initialisation')
        self.msg = ListGenderPredictionRequest()

    def execute(self, userdata):
        """Return the data of GenderAgeClassification"""
        self.msg.image = userdata.image

        Logger.loginfo('Wait for service')
        rospy.wait_for_service('/prediction')
        serv = rospy.ServiceProxy('/prediction', ListGenderPrediction)
        resp = serv(self.msg)
        Logger.loginfo(str(resp))
        from0to2 = 0
        from3to6 = 0
        from7to13 = 0
        from14to22 = 0
        from23to34 = 0
        from35to45 = 0
        from46to56 = 0
        from57to100 = 0

        kids = 0
        teenagers = 0
        adults = 0

        userdata.listPrediction = resp.listPrediction

        Logger.loginfo('Responce received')
        if len(resp.listPrediction) is not 0:
            for prediction in resp.listPrediction:
                Logger.loginfo(str(prediction))
                if prediction.ageMin == 0:
                    from0to2 = from0to2 +1
                    kids = kids +1

                if prediction.ageMin == 4:
                    from3to6 = from3to6 +1
                    kids = kids +1

                if prediction.ageMin == 8:
                    from7to13 = from7to13 +1
                    kids = kids +1

                if prediction.ageMin == 15:
                    from14to22 = from14to22 +1
                    teenagers = teenagers +1

                if prediction.ageMin == 25:
                    from23to34 = from23to34 +1
                    adults = adults +1

                if prediction.ageMin == 38:
                    from35to45 = from35to45 +1
                    adults = adults +1

                if prediction.ageMin == 48:
                    from46to56 = from46to56 +1
                    adults = adults +1

                if prediction.ageMin == 60:
                    from57to100 = from57to100 +1
                    adults = adults +1

            userdata.nbOfFrom0to2 = from0to2
            userdata.nbOfFrom3to6 = from3to6
            userdata.nbOfFrom7to13 = from7to13
            userdata.nbOfFrom14to22 = from14to22
            userdata.nbOfFrom23to34 = from23to34
            userdata.nbOfFrom35to45 = from35to45
            userdata.nbOfFrom46to56 = from46to56
            userdata.nbOfFrom57to100 = from57to100

            userdata.nbOfKids = kids
            userdata.nbOfTeenagers = teenagers
            userdata.nbOfAdults = adults

            return 'People_found'
        else:
            return 'Nobody_found'
