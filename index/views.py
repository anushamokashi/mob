# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
def base(request):
      #rendering the template in HttpResponse
 return render(request,'base.html')

def signup(request):
      #rendering the template in HttpResponse
  return render(request,'signup.html')

def signout(request):
      #rendering the template in HttpResponse
  #request.session.pop('userid')
  for key in request.session.keys():
  	del request.session[key]

  request.session.modified = True	
  return HttpResponseRedirect('/')  