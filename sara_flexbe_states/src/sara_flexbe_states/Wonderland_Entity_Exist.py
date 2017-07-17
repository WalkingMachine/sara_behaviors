#!/usr/bin/env python
# encoding=utf8

from flexbe_core import EventState, Logger
import json


class Wonderland_Entity_Exist(EventState):
	'''
	Read the 3D position of an entity in a json string

	># json_text    string  command to read

	<= ok           return when at least one entity exist
	<= empty        return when no entity have the selected name

	'''
	
	def __init__(self):
		# See example_state.py for basic explanations.
		super(Wonderland_Entity_Exist, self).__init__(outcomes=['ok', 'empty'], input_keys=['json_text'])
	
	def execute(self, userdata):
		# parse parameter json data
		data = json.loads(userdata.json_text)
		
		# read if there is data
		if not data:
			return 'empty'
		else:
			return 'ok'