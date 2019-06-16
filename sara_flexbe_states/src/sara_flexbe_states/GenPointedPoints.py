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

class GenPointedPoints(EventState):
    """
    Generates a list of points along a vector defined by a pointing person, generated from pointing hand.

    ># entity  Entity    Pointing persons entity

    -- step float Distance between generated points
    -- qty int Qty of generated points

    <= positionList  PointList  List of generated points
    """

    def __init__(self, step, qty):
        '''
        Constructor
        '''
        super(GenPointedPoints, self).__init__(outcomes=['done', 'not_pointing', 'failed'],
                                               input_keys=['entity'],
                                               output_keys=['positionList'])

        self.step = step
        self.qty = qty

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
        
        dx, dy, dz = normalize(handPosition, elbowPosition)
        
        positionList = []
        for i in range(self.qty):
            pointToReturn = Point()
            pointToReturn.x = handPosition.x+dx*(i+1)
            pointToReturn.y = handPosition.y+dy*(i+1)
            pointToReturn.z = handPosition.z+dz*(i+1)
            positionList.append(point)
        userdata.positionList = positionList
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

def normalize(handPosition, elbowPosition):
    dx = handPosition.x - elbowPosition.x
    dy = handPosition.y - elbowPosition.y
    dz = handPosition.z - elbowPosition.z
    dist = (dx**2 + dy**2 + dz**2)**0.5
    dx /= dist
    dy /= dist
    dz /= dist
    
    return [dx, dy, dz]