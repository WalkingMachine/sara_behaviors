#!/usr/bin/env python
# encoding=utf8

import requests
from flexbe_core import EventState, Logger


class Wonderland_Read_2D_Position(EventState):
	'''
	Send requests to Wonderland server

	># url      string  command to read
	<= x_pos    int  x position of the entity
	<= y_pos    int  y position of the entity

	'''
	
	def __init__(self):
		# See example_state.py for basic explanations.
		super(Wonderland_Read_2D_Position, self).__init__(outcomes=['done', 'error'], input_keys=['json_text'],
			output_keys=['x_pos', 'y_pos'])
	
	def execute(self, userdata):
		# This method is called periodically while the state is active.
		# Main purpose is to check state conditions and trigger a corresponding outcome.
		# If no outcome is returned, the state will stay active.
		userdata.json_text
		try:
			response = requests.get(userdata.json_text, headers=self._header)
		except requests.exceptions.RequestException as e:
			print e
			return 'error'
		
		userdata.response = response.content
		return 'done'  # One of the outcomes declared above.