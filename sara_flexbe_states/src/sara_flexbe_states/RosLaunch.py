# !/usr/bin/env python

import rospy
from flexbe_core import EventState, Logger
from subprocess import call
from os import system
import roslaunch
import rospkg
'''
Created on 21.09.2017
@author: Philippe La Madeleine
'''


class RosLaunch(EventState):
    '''
    Do a roslaunch (WIP)
    -- Package     String      Package where to find the launchfile
    -- File        String      File to launch
    
    <= done                     Launch is done
    '''

    def __init__(self, Package, File):
        '''
        Constructor
        '''
        super(RosLaunch, self).__init__(outcomes=['done'])
        self.Package = Package
        self.File = File
    def execute(self, userdata):
        '''
        Execute this state
        '''
        '''
        # get an instance of RosPack with the default search paths
        rospack = rospkg.RosPack()

        # get the file path for rospy_tutorials
        path = rospack.get_path(self.Package)

        #system("roslaunch sara_teleop sara_teleop.launch")
        #call( "roslaunch "+str(self.Package)+" "+str(self.File) )

        uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
        roslaunch.configure_logging(uuid)

        launch = roslaunch.parent.ROSLaunchParent(uuid, path+"/launch/"+str(self.File))
        launch.start()
        '''
        Logger.logerr("Roslaunch is still WIP")
        return "done"