# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, render_to_response

# Create your views here.

#from django.http import HttpResponse

#template
def startpage(request):
	return render(request,'startpage.html',{'name':'erikzorn'})