#!/usr/bin/env python

from flexbe_core import EventState, Logger
import rospy
from vizbox.msg import Story


class StoryboardSetStoryFromAction(EventState):
    """
       set_story
    -- titre    string     the title
    -- actionList  string[][]      the steps

    <= done  what's suppose to be written is written
    """

    def __init__(self):
        """set the story"""
        super(StoryboardSetStoryFromAction, self).__init__(outcomes=['done'], input_keys=['titre', 'actionList'])
        self.pub = rospy.Publisher("/story", Story)



    def execute(self, userdata):
        """execute what needs to be executed"""
        self.msg = Story()

        self.msg.title = userdata.titre

        story = []
        for action in userdata.actionList:
            print(action[0].lower())
            if action[0].lower() == "move":
                story.append("Move to the "+str(action[1]))
            elif action[0].lower() == "find":
                story.append("Find the " + str(action[1]))
            elif action[0].lower() == "findPerson":
                if len(action) == 1 or str(action[1]) == "":
                    story.append("Find a person")
                else:
                    story.append("Find " + str(action[1]))
            elif action[0].lower() == "guide":
                story.append("Guide to " + str(action[1]))
            elif action[0].lower() == "pick":
                story.append("Pick the " + str(action[1]))
            elif action[0].lower() == "give":
                if len(action) == 1 or action[1] == "":
                    story.append("Give to a person")
                else:
                    story.append("Give to " + str(action[1]))
            elif action[0].lower() == "say":
                story.append("Talk")
            elif action[0].lower() == "ask":
                story.append("Ask a question")
            elif action[0].lower() == "follow":
                story.append("Follow " + str(action[1]))
            elif action[0].lower() == "count":
                story.append("Count the number of " + str(action[1]))
            elif action[0].lower() == "place":
                story.append("Place on the " + str(action[1]))
            elif action[0].lower() == "answer":
                story.append("Answer a question")
            else:
                print("nothing")

        print( str(story))
        self.msg.storyline = story

        self.pub.publish(self.msg)
        Logger.loginfo('Success to publish the story')
        return 'done'
