#!/usr/bin/env python
# encoding=utf8

import requests
from flexbe_core import EventState, Logger


class Wonderland_Request(EventState):
	'''
	MoveArm receive a ROS pose as input and launch a ROS service with the same pose
	
	># url      string  url to call
	<= response string  Finish job.
	
	
	'''
	
	def __init__(self):
		# See example_state.py for basic explanations.
		super(Wonderland_Request, self).__init__(outcomes=['done', 'error'],
		                                         input_keys=['url'],
		                                         output_keys=['response'])
		self._header = {'api-key': 'asdf'}
	
	def execute(self, userdata):
		# This method is called periodically while the state is active.
		# Main purpose is to check state conditions and trigger a corresponding outcome.
		# If no outcome is returned, the state will stay active.
		try:
			response = requests.get(userdata.url, headers=self._header)
		except requests.exceptions.RequestException as e:
			print e
			return 'error'
			
		userdata.response = response.content
		return 'done'  # One of the outcomes declared above.