#!/usr/bin/env python
import string
import math
from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxySubscriberCached

from geometry_msgs.msg import Point
from sara_msgs.msg import Entity

'''
Created on 16.06.2019
@author: Alexandre Mongrain
'''

class GetPointedPositionOnPlane(EventState):
    """
    Prend l'entite d'une personne et renvoie la position de l'intersection de la position pointee par le bras de la personne avec un plan de hauteur planeHeight.

    ># entity  Entity    Entite de la personne qui pointe

    -- planeHeight float hauteur a laquelle calculer l'intersection

    <= position  Point  Position 3D du point trouve
    """

    def __init__(self, planeHeight):
        '''
        Constructor
        '''
        super(GetPointedPositionOnPlane, self).__init__(outcomes=['done', 'not_pointing', 'pointing_up' , 'failed'],
                                                        input_keys=['entity'],
                                                        output_keys=['position'])

        self.planeHeight = planeHeight

    def execute(self, userdata):
        '''
        Execute this state
        '''
        pointingArm = checkWhichArmIsRaised(userdata)
        if pointingArm == 0:
            return 'not_pointing'
        elif pointingArm == 1:
            partsId = [8, 10]
        elif pointingArm == 2:
            partsId = [7, 9]
        else:  # Par defaut, prend le bras droit
            partsId = [8, 10]
        
        partDict={}
        for part in userdata.entity.pose.parts:
            partDict[part.id] = part.position
        try:
            handPosition = partDict[partsId[1]]
            elbowPosition = partDict[partsId[0]]
        except:
            return 'failed'
        
        if elbowPosition.z < handPosition.z:
            return 'pointing_up'
        
        # x(t) =t*(ax) + x0 ; y(t) =t*(by) + y0 ; z(t) =t*(cz) + z0

        dz = handPosition.z - elbowPosition.z  # Difference en negatif
        t = (self.planeHeight - handPosition.z)/dz  # valeur de t a partir de la main sera positif
        
        zIntersect = handPosition.z + t * dz  #Devrait etre planeHeight
        yIntersect = handPosition.y + t * (handPosition.y - elbowPosition.y)
        xIntersect = handPosition.x + t * (handPosition.x - elbowPosition.x)

        pointToReturn = Point()
        pointToReturn.x = xIntersect
        pointToReturn.y = yIntersect
        pointToReturn.z = zIntersect
        userdata.position = pointToReturn
        return 'done'
        
        
    
    
def checkWhichArmIsRaised(userdata):
    '''
    Verifie quel bras est leve
    0=pas de bras
    1=droit
    2=gauche
    3=both
    '''
    right_arm_point = userdata.entity.pose.right_arm_point
    left_arm_point = userdata.entity.pose.left_arm_point
    if right_arm_point and left_arm_point:
        return 3
    elif right_arm_point:
        return 1
    elif left_arm_point:
        return 2
    else:
        return 0
