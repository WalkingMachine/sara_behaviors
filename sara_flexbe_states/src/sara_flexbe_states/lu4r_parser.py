#!/usr/bin/env python
# encoding=utf8
from __future__ import print_function
from flexbe_core import EventState, Logger
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
    Use lu4r to parse a sentence and return the detected actions into lists by pryorities

    ># sentence     string      sentence to parse
    
    <# HighFIFO     string[]      list of actions
    <# MedFIFO      ActionForm[]      list of actions
    <# LowFIFO      ActionForm[]      list of actions
    <# DoNow        ActionForm[]      list of actions
    
    <= done     Finished job.
    <= fail     unable to parse.
    '''


    def __init__(self):
        # See example_state.py for basic explanations.
        super(LU4R_Parser, self).__init__(outcomes=['done', 'fail'], input_keys=['sentence', 'HighFIFO','MedFIFO','LowFIFO','DoNow'])
        self.Subject = ''
        self.Person = ''

    def execute(self, userdata):
        # This method is called periodically while the state is active.
        # Main purpose is to check state conditions and trigger a corresponding outcome.
        # If no outcome is returned, the state will stay active.


        Logger.loginfo("sentence: "+userdata.sentence)

        lu4r_ip = '127.0.0.1'
        lu4r_port = '9001'
        lu4r_url = 'http://' + str(lu4r_ip) + ':' + str(lu4r_port) + '/service/nlu'


        HYPO = {'hypotheses':[{"transcription":userdata.sentence,"confidence":"0.9","rank":"1"}]}
        ENT = {'entities': [
            {"atom": "table1", "type": "table", "preferredLexicalReference": "table",
             "alternativeLexicalReferences": ["counter", "desk"],
             "coordinate": {"x": "16.0", "y": "0.0", "z": "0.0", "angle": "0.671"}},
            {"atom": "bedroom1", "type": "bedroom", "preferredLexicalReference": "bedroom",
             "alternativeLexicalReferences": ["chamber", "cubicle", "bedchamber"],
             "coordinate": {"x": "11.0", "y": "6.0", "z": "0.0", "angle": "0"}},
            {"atom": "studio1", "type": "studio", "preferredLexicalReference": "studio",
             "alternativeLexicalReferences": ["library", "office"],
             "coordinate": {"x": "9.0", "y": "14.0", "z": "0.0", "angle": "0"}},
            {"atom": "person1", "type": "person", "preferredLexicalReference": "person",
             "alternativeLexicalReferences": ["body", "character", "guy", "man", "woman"],
             "coordinate": {"x": "2.0", "y": "2.0", "z": "0.0", "angle": "0"}}]}

        r = requests.post(lu4r_url, data={'hypo':str(HYPO) , 'entities':str(ENT)}, headers=HEADERS)

        lu4r = Lu4r()
        opItem = Operation()

        for line in r.iter_lines():
            if line:
                regex = re.compile('(\s*:op\d\s)?\([a-zA-Z0-9\-]+ / ([a-zA-Z\-]+)')
                m = regex.match(line)
                if m:
                    if opItem.action != "" and opItem.action != 'and':
                        lu4r.opList.append(opItem)
                    opItem = Operation()
                    opItem.action = m.group(2)
                else:
                    regex = re.compile('\s*:([a-zA-Z0-9]*) \([a-zA-Z0-9]* / ([a-zA-Z0-9]*)\)')
                    n = regex.match(line)
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

        lu4r.opList = self.ManageSubject( lu4r.opList );

        regex = re.compile('.*(stop).*')
        if regex.match(lu4r.opList[0].action.lower()):
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
                    '.*(bring).*',
                    '.*(theme).*',
                    '.*((area)|(source)).*',
                    '.*((beneficiary)|(goal)).*'])
            if ActionForm == None:
                ActionForm = self.ActionFormBuilder(opitem, [
                    'Follow',
                    '.*(cotheme).*',
                    '.*(theme).*',
                    '.*(area).*',
                    '.*((path)|(road)).*'])
            if ActionForm == None:
                ActionForm = self.ActionFormBuilder( opitem, [
                    'Move',
                    '.*(motion).*',
                    '.*((theme)|(area)|(goal)).*',
                    '.*(direction).*',
                    '.*(distance).*'])
            if ActionForm == None:
                ActionForm = self.ActionFormBuilder(opitem, [
                    'Attach',
                    '.*(attaching).*',
                    '.*(item).*',
                    '.*((goal)|(connector)).*'])
            if ActionForm == None:
                ActionForm = self.ActionFormBuilder(opitem, [
                    'LookAt',
                    '.*(ispecting).*',
                    '.*((ground)|(phenomenon)).*'])
            if ActionForm == None:
                ActionForm = self.ActionFormBuilder(opitem, [
                    'Find',
                    '.*(locating).*',
                    '.*((sought_entity)|(phenomenon)).*',
                    '.*((ground)|(location)).*'])
            if ActionForm == None:
                ActionForm = self.ActionFormBuilder(opitem, [
                    'Place',
                    '.*(placing).*',
                    '.*(goal).*'])
            if ActionForm == None:
                ActionForm = self.ActionFormBuilder(opitem, [
                    'Give',
                    '.*(giving).*',
                    '.*(theme).*',
                    '.*(recipient).*'])
            if ActionForm == None:
                ActionForm = self.ActionFormBuilder(opitem, [
                    'Pick',
                    '.*(manipulation).*',
                    '.*(entity).*',
                    '.*((area)|(source)).*'])
            if ActionForm == None:
                ActionForm = self.ActionFormBuilder(opitem, [
                    'LookAt',
                    '.*((perception)|(look)).*',
                    '.*((direction)|(phenomenon)).*'])
            if ActionForm == None:
                ActionForm = self.ActionFormBuilder(opitem, [
                    'Pick',
                    '.*((get)|(taking)).*',
                    '.*(theme).*',
                    '.*((area)|(source)).*'])
            if ActionForm == None:
                ActionForm = self.ActionFormBuilder(opitem, [
                    'Turn',
                    '.*(change direction).*',
                    '.*(direction).*'])


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
        regex = re.compile(positions[1])
        if regex.match(opitem.action.lower()):
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
                    regex = re.compile(positions[i])
                    if regex.match(arg.type.lower()):
                        PreActionForm[i-1] = arg.content
                    i = i + 1
        return PreActionForm

    def ManageSubject(self, opitems):
        for opitem in opitems:
            for arg in opitem.args:
                regex = re.compile('.*((theme)|(goal)|(sought_entity)|(phenomenon)).*')
                if regex.match(arg.type.lower()):
                    regex = re.compile('.*[^a-z]((this)|(that)|(it))[^a-z].*')
                    if regex.match(arg.content.lower()):
                        arg.content = self.Subject
                    else:
                        self.Subject = arg.content
                regex = re.compile('.*((beneficiary)|(goal)).*')
                if regex.match(arg.type.lower()):
                    regex = re.compile('.*[^a-z]((him)|(her))[^a-z].*')
                    if regex.match(arg.content.lower()):
                        arg.content = self.Person
                    else:
                        self.Person = arg.content
                    regex = re.compile('.*[^a-z]((me)|(myself))[^a-z].*')
                    if regex.match(arg.content.lower()):
                        arg.content = 'you'
                        continue
                    regex = re.compile('.*[^a-z](you)|(sarah?)|(shut up)|(yourself)[^a-z].*')
                    if regex.match(arg.content.lower()):
                        arg.content = 'myself'
                        continue

        return opitems
