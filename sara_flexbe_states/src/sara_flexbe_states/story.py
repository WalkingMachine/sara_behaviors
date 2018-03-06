#!/usr/bin/env python

from flexbe_core import EventState, Logger
import rospy
from vizbox.msg import Story


class Set_Story(EventState):
    """
       set_story
    -- titre    string     the title
    -- storyline  string[]      the steps

    <= done  what's suppose to be written is written
    """

    def __init__(self, titre, storyline):
        """set the story"""
        super(Set_Story, self).__init__(outcomes=['done'])
        self.pub = rospy.Publisher("/story", Story)

        self.msg = Story()
        self.msg.title = titre
        self.msg.storyline = storyline

    def execute(self, userdata):
        """execute what needs to be executed"""
        self.pub.publish(self.msg)
        Logger.loginfo('Success')
        return 'done'
