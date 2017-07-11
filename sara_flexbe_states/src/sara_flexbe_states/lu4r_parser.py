#!/usr/bin/env python
# encoding=utf8
from __future__ import print_function
from flexbe_core import EventState, Logger
from geometry_msgs.msg import Pose
from sara_moveit.srv import *
import rospy
import roslib; roslib.load_manifest('lu4r_ros')
import rospy
from lu4r_ros.srv import *
from lu4r_ros.msg import *
import socket
import sys
import requests
import json
import re
from subprocess import call

reload(sys)
sys.setdefaultencoding('utf8')
semantic_map = {}
HEADERS = {'content-type': 'application/json'}



class LU4R_Parser(EventState):
    '''
    MoveArm receive a ROS pose as input and launch a ROS service with the same pose

    ># sentence     string      sentence to parse
    
    <# actions     lu4r      list of actions

    <= done     Finish job.
    '''

    def __init__(self):
        # See example_state.py for basic explanations.
        super(LU4R_Parser, self).__init__(outcomes=['done', 'fail'], input_keys=['sentence', 'HighFIFO','MedFIFO','LowFIFO','DoNow'])

    def execute(self, userdata):
        # This method is called periodically while the state is active.
        # Main purpose is to check state conditions and trigger a corresponding outcome.
        # If no outcome is returned, the state will stay active.


        Logger.loginfo("sentence: "+userdata.sentence)

        lu4r_ip = '127.0.0.1'
        lu4r_port = '9001'
        lu4r_url = 'http://' + str(lu4r_ip) + ':' + str(lu4r_port) + '/service/nlu'


        HYPO = {'hypotheses':[{"transcription":userdata.sentence,"confidence":"0.9","rank":"1"}]}
        ENT = {'entities': [{"atom":"book1","type":"book","preferredLexicalReference":"book","alternativeLexicalReferences":["volume","manual","dictionary","text"],"coordinate":{"x":"13.0","y":"0.0","z":"0.0","angle":"0"}},{"atom":"table1","type":"table","preferredLexicalReference":"table","alternativeLexicalReferences":["counter","desk"],"coordinate":{"x":"16.0","y":"0.0","z":"0.0","angle":"0.671"}},{"atom":"glass1","type":"glass","preferredLexicalReference":"glass","alternativeLexicalReferences":["cup","decanter","chalice"],"coordinate":{"x":"5.0","y":"8.0","z":"0.0","angle":"0"}},{"atom":"bedroom1","type":"bedroom","preferredLexicalReference":"bedroom","alternativeLexicalReferences":["chamber","cubicle","bedchamber"],"coordinate":{"x":"11.0","y":"6.0","z":"0.0","angle":"0"}},{"atom":"studio1","type":"studio","preferredLexicalReference":"studio","alternativeLexicalReferences":["library","office"],"coordinate":{"x":"9.0","y":"14.0","z":"0.0","angle":"0"}},{"atom":"person1","type":"person","preferredLexicalReference":"person","alternativeLexicalReferences":["body","character","guy","man","woman"],"coordinate":{"x":"2.0","y":"2.0","z":"0.0","angle":"0"}}]}
        r = requests.post(lu4r_url, data={'hypo':str(HYPO) , 'entities':str(ENT)}, headers=HEADERS)

        lu4r = Lu4r()
        opItem = Operation()

        for line in r.iter_lines():
            if line:
                operation = re.compile('(\s*:op\d\s)?\([a-zA-Z0-9\-]+ / ([a-zA-Z\-]+)')
                m = operation.match(line)
                if m:
                    if opItem.action != "" and opItem.action != 'and':
                        lu4r.opList.append(opItem)
                    opItem = Operation()
                    opItem.action = m.group(2)
                else:
                    action = re.compile('\s*:([a-zA-Z0-9]*) \([a-zA-Z0-9]* / ([a-zA-Z0-9]*)\)')
                    n = action.match(line)
                    if n:
                        arg = args()
                        arg.type = n.group(1)
                        arg.content = n.group(2)
                        opItem.args.append(arg)

        if opItem.action != "":
            lu4r.opList.append(opItem)

        Logger.loginfo("Returning operation list - count : " + str(len(lu4r.opList)))
        if len(lu4r.opList) == 0:
            Logger.loginfo("fail")
            return 'fail'


        test = re.compile('.*[Ss]top.*')
        n = test.match(lu4r.opList[0].action)
        if n:
            Logger.loginfo("Action: Stop now!")
            userdata.DoNow = []
            userdata.DoNow.append('Stop')
            userdata.DoNow.append(0)
            userdata.HighFIFO = []
            userdata.MedFIFO = []
            userdata.LowFIFO = []

        for opitem in lu4r.opList:
            priority = 2
            Logger.loginfo("Action: "+opitem.action)
            ActionForm = None


            if ActionForm == None:
                ActionForm = self.ActionFormBuilder(opitem, [
                    'Bring',
                    '.*[Bb]ring.*',
                    '.*([Tt]heme).*',
                    '.*([Aa]rea)|([Ss]ource).*',
                    '.*([Bb]eneficiary).*'])
            if ActionForm == None:
                ActionForm = self.ActionFormBuilder(opitem, [
                    'Follow',
                    '.*[Cc]otheme.*',
                    '.*([Tt]heme).*',
                    '.*([Gg]oal).*',
                    '.*([Aa]rea).*'
                    '.*([Pp]ath)|([Rr]oad).*'])
            if ActionForm == None:
                ActionForm = self.ActionFormBuilder( opitem, [
                    'MoveBase',
                    '.*[Mm]otion.*',
                    '.*([Tt]heme)|([Aa]rea)|([Gg]oal).*',
                    '.*([Dd]irection).*',
                    '.*([Dd]istance).*'])
            if ActionForm == None:
                ActionForm = self.ActionFormBuilder(opitem, [
                    'Attach',
                    '.*[Aa]ttaching.*',
                    '.*([Ii]tem).*',
                    '.*([Gg]oal)|([Cc]onnector).*'])
            if ActionForm == None:
                ActionForm = self.ActionFormBuilder(opitem, [
                    'LookAt',
                    '[Ii]specting'
                    '.*[Gg]round.*'])
            if ActionForm == None:
                ActionForm = self.ActionFormBuilder(opitem, [
                    'Find',
                    '.*[Ll]ocating.*',
                    '.*[Ss]ought_entity.*',
                    '.*([Gg]round)|([[Ll]ocation]).*'])
            if ActionForm == None:
                ActionForm = self.ActionFormBuilder(opitem, [
                    'Place',
                    '.*[Pp]lacing.*',
                    '.*[Gg]oal.*'])
            if ActionForm == None:
                ActionForm = self.ActionFormBuilder(opitem, [
                    'Give',
                    '.*[Gg]iving.*',
                    '.*[Rr]ecipient.*'])
            if ActionForm == None:
                ActionForm = self.ActionFormBuilder(opitem, [
                    'Pick',
                    '.*[Mm]anipulation.*',
                    '.*([Ee]tity).*',
                    '.*([Aa]rea).*'])
            if ActionForm == None:
                ActionForm = self.ActionFormBuilder(opitem, [
                    'LookAt',
                    '[Pp]erception'
                    '.*[Dd]irection.*'])
            if ActionForm == None:
                ActionForm = self.ActionFormBuilder(opitem, [
                    'Pick',
                    '.*[Tt]aking.*',
                    '.*([Tt]heme).*',
                    '.*([Aa]rea).*'])
            if ActionForm == None:
                ActionForm = self.ActionFormBuilder(opitem, [
                    'Turn',
                    '.*[Cc]ange [Dd]irection.*',
                    '.*([Dd]irection).*'])



            if ActionForm != None:
                if priority == 1:
                    userdata.LowFIFO.append(ActionForm)
                if priority == 2:
                    userdata.MedFIFO.append(ActionForm)
                if priority == 3:
                    userdata.HighFIFO.append(ActionForm)

        return 'done'  # One of the outcomes declared above.

    def on_enter(self, userdata):
        # This method is called when the state becomes active, a transition from another state to this one is taken.
        # It is primarily used to start actions which are associated with this state.

        Logger.loginfo('Enter lu4r_parser')

        global semantic_map

    def ActionFormBuilder(self, opitem, positions):

        PreActionForm = None
        # - Generic ActionForm builder
        test = re.compile(positions[1])
        n = test.match(opitem.action)
        if n:
            PreActionForm = []
            PreActionForm.append(positions[0])
            i=2
            while i<len(positions):
                PreActionForm.append('')
                i = i + 1
            for arg in opitem.args:
                Logger.loginfo("arg-type: " + arg.type)
                Logger.loginfo("arg-content: " + arg.content)
                i = 2
                while i < len(positions):
                    test = re.compile(positions[i])
                    n = test.match(arg.type)
                    if n:
                        PreActionForm[i-1] = arg.content
                    i = i + 1
        return PreActionForm