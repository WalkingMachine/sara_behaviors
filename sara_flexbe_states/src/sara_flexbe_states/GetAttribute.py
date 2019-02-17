#!/usr/bin/env python

import rospy
from flexbe_core import EventState, Logger

'''
Created on 29.08.2013

@author: Philipp Schillinger
'''

class GetAttribute(EventState):
	'''
	Return from an object, all desired attributes provided as a list. Like some kind of demux.

	-- input_keys   string[]   	List of desired attributes.

	># object   object[]    	The object to get attributes from.

	#> attributes object      The desired attributes.

	<= done                     Indicates completion of the extraction.

	'''


	def __init__(self, attributes=[]):
		'''Constructor'''
		super(GetAttribute, self).__init__(outcomes=['done'],
										   input_keys=['object'],
										   output_keys=attributes)

		self.attributes = attributes
		
		
	def execute(self, userdata):
		'''Execute this state'''
		for att in self.attributes:
			try:
				setattr(userdata, att, getattr(userdata.object, att))
			except Exception as e:
				Logger.logwarn("The attribute "+str(att)+" is not to be found in "+str(userdata.object))
				setattr(userdata, att, None)
		# nothing to check
		return 'done'