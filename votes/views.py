# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.views import View
from .forms import SubmitZipForm
import requests




# Create your views here.

#from django.http import HttpResponse

#template

def home_view_fbv(request, *args, **kwargs):
	if request.method =='POST':
		print(request.POST)

	return render(request,'startpage.html', {})

def get_district_number(zipcode):
		#print zipcode
		resp = requests.get('https://congress.api.sunlightfoundation.com/districts/locate?zip={}'.format(zipcode))
		if resp.status_code != 200:
			print 'Could not get district number, status code: ' + str(resp.status_code)
			return
		js = resp.json()
		#print js
		state_name = js['results'][0]['state']
		district_number = js['results'][0]['district']
		return {'state_name':state_name, 'district_number':district_number}

def get_congressperson(state, district):
	headers = {
    	'X-API-Key': 'HeU67wOwjMas9zx1MWRRg4fB09F4YyJ87jgec6xv',
    }
	resp = requests.get('https://api.propublica.org/congress/v1/members/house/{}/{}/current.json'.format(state,district), headers=headers)
	if resp.status_code != 200:
			print 'Could not get congressperson, status code: ' + str(resp.status_code)
			return
	js = resp.json()
	return js['results'][0]['name'], js['results'][0]['id']

def get_recent_votes(ID):
	headers = {
    	'X-API-Key': 'HeU67wOwjMas9zx1MWRRg4fB09F4YyJ87jgec6xv',
    	
    }
   	resp = requests.get('https://api.propublica.org/congress/v1/members/{}/votes.json'.format(ID), headers=headers)

   	js = resp.json()
   	#print js
   	votes = []
   	for i in range(0,9):
   		votes.append(js['results'][0]['votes'][i]['position'])

   	print votes
	return votes



class HomeView(View):
	def get(self, request, *args, **kwargs):
		the_form = SubmitZipForm()
		context = {
			'title': 'Submit Zip',
			'form': the_form,
			'name': 'erikzorn'	
		}
		return render(request, 'startpage.html', context)

	

	def post(self, request, *args, **kwargs):
		#print(request.POST)
		#print(request.POST.get('zipcode'))
		form = SubmitZipForm(request.POST)
		if form.is_valid():
			print(form.cleaned_data)
		code = get_district_number(form.cleaned_data['zip'])
		state = code['state_name']
		district = code['district_number']
		congressperson, ID = get_congressperson(state, district)
		position = get_recent_votes(ID)
		print "State: " + str(state) 
		print "District: " + str(district)
		print congressperson
		print ID
		print position
		
		#print(get_district_number(21811))
		#print(get_district_number(form.cleaned_data['zip']))
		#resp = requests.get('https://congress.api.sunlightfoundation.com/districts/locate?zip=21811')
		#js = resp.json()
		#print(js)

		context = {
			'title': 'Submit Zip',
			'form': form,
			'name': 'erikzorn'
		}
		return render(request,'startpage.html',context)

	

#def startpage(request):
#	return render(request,'startpage.html',{})



#def get(self, request, *args, **kwargs):
	#return render(request,'startpage.html', {})

#def post(self, request, *args, **kwargs):
	#print(request.POST)
	#return render(request,'startpage.html', {})
