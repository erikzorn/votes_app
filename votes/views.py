# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.views import View
from .forms import SubmitZipForm
import requests

headers = {		# Propub API KEY
    	'X-API-Key': 'HeU67wOwjMas9zx1MWRRg4fB09F4YyJ87jgec6xv',
    }


def home_view_fbv(request, *args, **kwargs):
	if request.method =='POST':
		print(request.POST)

	return render(request,'startpage.html', {})

def get_district_number(zipcode):
		#print zipcode
		resp = requests.get('https://congress.api.sunlightfoundation.com/districts/locate?zip={}'.format(zipcode))
		if resp.status_code != 200:
			print 'Could not get district number, status code: ' + str(resp.status_code)
			return None
		js = resp.json()
		if js['count'] is 0:
			return -1, -1
		#print resp.status_code
		state_name = js['results'][0]['state']
		district_number = js['results'][0]['district']
		#return {'state_name':state_name, 'district_number':district_number}
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

   	votes_title = []
   	votes_position = []
   	votes = []
   	count = 0	# keeps track of when 6 unique bills have been collected
   	i = 0		# used for iteration through query data

   	#add last 6 question and vote position so lists.
   	while (count < 6):
   		if bool(js['results'][0]['votes'][i]['bill']):		# if bill{} is not empty

   			title = js['results'][0]['votes'][i]['bill']['title']	# title of specific bill
   			position = js['results'][0]['votes'][i]['position']		# position (yes/no)

   			if(title in votes_title):			# if this bill is already in the list then remove instance and corresponding position
   				votes_position.pop(votes_title.index(title))
   				votes_title.remove(title)

   			else:		# if bill was not a duplicate then increment counter to know that there is now one more bill in the list
   				count = count + 1

   			#add new title and position to lists
   			votes_title.append(title)
   			votes_position.append(position)

   		i = i + 1

   	# put data in tuples to return
   	for i in range(len(votes_title)):
		votes.append([votes_title[i], votes_position[i]])

	return votes #, votes_title, votes_position 



class HomeView(View):
	def get(self, request, *args, **kwargs):
		form = SubmitZipForm()
		context = {
			'title': 'Submit Zipcode',
			'form': form,
			'name': 'erikzorn'	
		}
		#print form
		return render(request, 'startpage.html', context)

	def post(self, request, *args, **kwargs):
		form = SubmitZipForm(request.POST)
		if form.is_valid():
			#print(form.cleaned_data)
			state, district = get_district_number(form.cleaned_data['zip'])
		if (state > -1):
			congressperson, ID = get_congressperson(state, district)
			votes = get_recent_votes(ID) 
			context = {
				'title': 'Submit Zipcode',
				'form': form,
				'name': 'Erik Zorn',
				'person': congressperson,
				'votes':votes,
			}
		else:
			context = {
			'title': 'Submit Zipcode',
			'form': form,
			'person': 'INVALID ZIPCODE',	
		}
		return render(request,'vote_data.html',context)

	
