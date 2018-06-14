#!/usr/bin/env python

from flexbe_core import EventState, Logger
import rospy
from vizbox.msg import Story


class StoryboardSetStoryKey(EventState):
    """
       set_story
    -- titre    string     the title
    -- actionList  string[][]      the steps

    <= done  what's suppose to be written is written
    """

    def __init__(self):
        """set the story"""
        super(StoryboardSetStoryKey, self).__init__(outcomes=['done'], input_keys=['titre', 'actionList'])
        self.pub = rospy.Publisher("/story", Story)



    def execute(self, userdata):
        """execute what needs to be executed"""
        self.msg = Story()

        self.msg.title = userdata.titre

        story = []
        for action in userdata.actionList:
            if action[0] is "Move":
                story.append("Move to the "+action[1])
            else if action[0] is "Find":
                story.append("Find the " + action[1])
            else if action[0] is "FindPerson":
                story.append("Find " + action[1])
            else if action[0] is "Guide":
                story.append("Guide to " + action[1])
            else if action[0] is "Pick":
                story.append("Pick the " + action[1])
            else if action[0] is "Give":
                story.append("Give to " + action[1])
            else if action[0] is "Say":
                story.append("Say something")
            else if action[0] is "Ask":
                story.append("Ask a question")
            else if action[0] is "Follow":
                story.append("Follow " + action[1])
            else if action[0] is "Count":
                story.append("Count the number of " + action[1])
            else if action[0] is "Place":
                story.append("Place on the " + action[1])
            else if action[0] is "Answer":
                story.append("Answer a question")

        self.msg.storyline = story

        self.pub.publish(self.msg)
        Logger.loginfo('Success to publish the story')
        return 'done'
