# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import View
from .forms import SubmitZipForm
import propub
import requests


class HomeView(View):
	def get(self, request, *args, **kwargs):
		form = SubmitZipForm()
		context = {
			'title': 'Submit Zipcode',
			'form': form,
			'name': 'erikzorn'	
		}
		
		return render(request, 'vote_data.html', context)

	def post(self, request, *args, **kwargs):

		form = SubmitZipForm(request.POST)

		if form.is_valid():	
			state, district = propub.get_district_number_from_txt(form.cleaned_data['zip'])
			# state, district = propub.get_district_number(form.cleaned_data['zip'])

		if (state > -1):	# if valid input and results
			congressperson, ID = propub.get_congressperson(state, district)
			votes = propub.get_recent_votes(ID) 

			context = {		# context if input was correct
				'title': 'Submit Zipcode',
				'form': form,
				'name': 'Erik Zorn',
				'person': congressperson,
				'votes':votes,
				'formdisplay': '1',
			}
		else:
			context = {		# context for invalid zipcode
			'title': 'Submit Zipcode',
			'form': form,
			'invalid': 'INVALID ZIPCODE',	
		}
		return render(request,'vote_data.html',context)

	
