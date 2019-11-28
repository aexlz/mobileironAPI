#!/usr/bin/env python

import requests
import argparse
import logging
import time
import json
import html
# Logging
logging.basicConfig(filename='anwenderServiceToolbox.log', format='%(asctime)s %(message)s', level=logging.INFO)

# Parsing Arguments
parser = argparse.ArgumentParser(description='Retrieves various information about user and related devices from MobileIron API')
parser.add_argument('mobileironUrl', help='URL of your MobileIron-Core')
parser.add_argument('username', help='Username for BasicAuth')
parser.add_argument('password', help='Password for BasicAuth')
parser.add_argument('userId', help='User ID')
args = parser.parse_args()

# REST-Calls
authorizedUsers = '/api/v2/authorized/users?adminDeviceSpaceId=1&'
devicesPerUser = '/api/v2/devices?adminDeviceSpaceId=1&' 
device_details = 'fields=user.display_name%2Ccommon.uuid%2Ccommon.registration_date%2Ccommon.quarantined%2Ccommon.miclient_last_connected_at%2Ccommon.last_connected_at%2Ccommon.manufacturer%2Ccommon.model%2Ccommon.platform_name%2Cuser.user_id%2Ccommon.platform%2Ccommon.os_version&query=common.status=%22ACTIVE%22'

# Build Json
toolBox = {}

class MobileIronAPI:
	def __init__(self, mobileironUrl, username, password, userId):
		self.mobileironUrl = mobileironUrl
		self.username = username
		self.password = password
		self.userId = userId

    # Check Connection to API
	def check_connection(self):
		try:
			r = requests.get(mobileironUrl, auth=(self.username, self.password))
			if r.status_code == 200:
				logging.info('Connection to MobileIronAPI established successfully')
				self.call_api(self.userId)
			else:
				logging.info('Request for check_connection %s', r.status_code)
		except requests.ConnectionError:
			logging.info('Failed to check_connection')
		
	# Call User API -- MAIN
	def call_api(self, userId):
		url = mobileironUrl + authorizedUsers + 'query=' + userId
		logging.info('Called User-URL: %s', url)
		try:
			r = requests.get(url, auth=(self.username, self.password))
			if r.status_code == 200:
				logging.info('User Management was called successfully')
				try:
					try:
						userManagement = r.json()
						logging.info('User Management %s', userManagement)
						#Calls method gatherInfosAboutUser
						self.gatherInfosAboutUser(userManagement, userId)
					except ValueError:
						logging.info('User Management could not be parsed to JSON')
				except ValueError:
					logging.info('Could not parse JSON-from User-API')
			else:
				logging.info('Request for call_API %s', r.status_code)
		except requests.ConnectionError:
			logging.info('Failed to call_API')
	#Build User Details	for each User, who is found	

	def gatherInfosAboutUser(self, userManagement, userId):
		iteratorUser = 0
		if userManagement['totalCount'] >= 1:
			for item in userManagement['results']:
				User = {}
				if item['enabled']:
					User['User activated'] = 'Ja'
				if item['email']:
					User['E-Mail'] = item['email']
				if item['displayName']:
					#This is actually the correct User-ID
					User['User principal'] = item['principal']
				iteratorUser += 1
				toolBox[str(iteratorUser) + '. User'] = User
						
			#Calls Method gatherInfosAboutDevicePerUser: Every user can possess one or more mobile devices
			iteratorUser = 1
			deviceManagement = self.gatherInfosAboutDevices()
			for keys in toolBox:
				singleUser = toolBox.get(str(iteratorUser) + '. User')
				iteratorUser += 1
				self.searchForUserInDevices(deviceManagement, singleUser, singleUser['User principal'])
				logging.info("Device Management: %s", singleUser)
			print(json.dumps(toolBox, indent=4, sort_keys=False))
		else:
			logging.info('There is no user registered with given ID %s', userId)
	
	#Get Device Details
	def gatherInfosAboutDevices(self):
		url = mobileironUrl + devicesPerUser + device_details
		logging.info('Called Device-URL: %s', url)
		try:
			r = requests.get(url, auth=(self.username, self.password))
			if r.status_code == 200:
				logging.info('Device Management was called successfully')
				try:
					deviceManagement = r.json()
					return deviceManagement
				except ValueError:
					logging.info('Device Management could not be parsed to JSON')
			else:
				logging.info('Request for gatherInfosAboutDevicePerUser %s', r.status_code)
		except requests.ConnectionError:
			logging.info('Failed to gatherInfosAboutDevicePerUser')
		
	def searchForUserInDevices(self, deviceManagement, singleUser, userId):
			iterator = 0
			for item in deviceManagement['results']:
				Device = {}
				if item['user.user_id'] == userId:
					iterator += 1
					Device['Device Type'] = item['common.platform_name']
					Device['Last Connection'] = item['common.last_connected_at']
					Device['In Quarantine'] = item['common.quarantined']
					Device['Registration Date'] = item['common.registration_date']
					#Add device details to given user
					singleUser[str(iterator) + '. Device'] = Device
					
obj = MobileIronAPI(args.mobileironUrl, args.username, args.password, args.userId)

obj.check_connection()