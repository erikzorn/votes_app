import requests

headers = {		# Propub API KEY
    	'X-API-Key': 'HeU67wOwjMas9zx1MWRRg4fB09F4YyJ87jgec6xv',
    }

def get_district_number(zipcode):
		resp = requests.get('https://congress.api.sunlightfoundation.com/districts/locate?zip={}'.format(zipcode))
		if resp.status_code != 200:
			print 'Could not get district number, status code: ' + str(resp.status_code)
			return None
		js = resp.json()

		if js['count'] is 0:	# if zipcode is invalid return -1's for error handling
			return -1, -1

		state_name = js['results'][0]['state']				# retrieve state and distr number 
		district_number = js['results'][0]['district']

		return state_name, district_number

def get_congressperson(state, district):
	resp = requests.get('https://api.propublica.org/congress/v1/members/house/{}/{}/current.json'.format(state,district), headers=headers)
	#if resp.status_code != 200:
	#		print 'Could not get congressperson, status code: ' + str(resp.status_code)
	#		return
	js = resp.json()
	return js['results'][0]['name'], js['results'][0]['id']

def get_recent_votes(ID):

   	resp = requests.get('https://api.propublica.org/congress/v1/members/{}/votes.json'.format(ID), headers=headers)

   	js = resp.json()

   	votes_title = []	# list keeps track of bills already voted on

   	votes = []
   	count = 0	# keeps track of when 6 unique bills have been collected
   	i = 0		# used for iteration through query data

   	#add last 6 question and vote position so lists.
   	while (count < 10):
   		if bool(js['results'][0]['votes'][i]['bill']):		# if bill{} is not empty

   			title = js['results'][0]['votes'][i]['bill']['title']	# title of specific bill
   			position = js['results'][0]['votes'][i]['position']		# position (yes/no)

   			if(title not in votes_title):			# if this bill does not already have a responds then add it to the list 
   				votes_title.append(title)
   				votes.append([title, position])		# add the title and postion to a list of tuples
   				count = count + 1					# increment the count of bills to be returned

   		i = i + 1			# increment index for getting API data

	return votes #, votes_title, votes_position 
