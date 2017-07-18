#!/usr/bin/env python
# encoding=utf8

from flexbe_core import EventState, Logger
import json


class Wonderland_Entity_Exist(EventState):
	'''
	Read the 3D position of an entity in a json string

	># json_text    string  command to read
	#> number       int     number of results
	
	<= ok           return when at least one entity exist
	<= empty        return when no entity have the selected name

	'''
	
	def __init__(self):
		# See example_state.py for basic explanations.
		super(Wonderland_Entity_Exist, self).__init__(outcomes=['one', 'multiple', 'empty'], input_keys=['json_text'], output_keys=['number'])
	
	def execute(self, userdata):
		# parse parameter json data
		data = json.loads(userdata.json_text)
		
		userdata.number = len(data)
		
		# read if there is data
		if len(data) == 0:
			return 'empty'
		elif len(data) == 1:
			return 'one'
		else:
			return 'multiple'