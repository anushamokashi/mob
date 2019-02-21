from __future__ import unicode_literals
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from authentication.forms import UserProfileForm
from .models import userprofile
from django.contrib.auth.hashers import make_password
from project.models import  Projectwiseusersetup
from project.models import  Project

import logging

logger = logging.getLogger(__name__)
# Create your views here.

def success(request):
      return render(request,'success.html')

def signup(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if not form.is_valid():
            print form.errors
            messages.add_message(request, messages.ERROR, 'There was some problems while creating your account. Please review some fields before submiting again.')
            return render(request, 'signup.html', { 'form': form })
        else: 
            new_user = form.save(commit=False)
            new_user.adminuserid = 0
            new_user.save()
        messages.add_message(request, messages.SUCCESS, 'Your account were successfully created.')
        return HttpResponseRedirect('/authentication/signup/')
        
    else:
       return render(request, 'signup.html', { 'form': UserProfileForm() })

 

def login(request):
   
    if request.POST:
        print request.POST
        
        user_name = request.POST['email'].strip()
        password = request.POST['password'].strip()

        try:
            loginModel = userprofile.objects.get(email=user_name,password=password)
            print loginModel.id
            print loginModel.is_admin
            
            if loginModel.is_admin: 
                request.session['loggedinuserid'] = loginModel.id
                return HttpResponseRedirect('/home/main/')
            else : 
                element =Projectwiseusersetup.objects.get(userid=loginModel.id,setasdefaultproject = True)
                print element.project_id_id              
                projectselect =Project.objects.filter(pk=element.project_id_id)
                print projectselect
                if element.setasdefaultproject:
                    project_title = element.project_id.title
                    print project_title
                    request.session['userid'] = loginModel.id
                    request.session['projectid'] = element.project_id_id
                    parent = Project.objects.get(id = element.project_id_id)
                    return HttpResponseRedirect('/transaction/transmain/')
                else: 
                    return HttpResponseBadRequest('No default project assigned')     
        except Exception as e:
            print e
            messages.add_message(request, messages.ERROR, 'Username or password invalid.')
            logger.error("INVALID USER")
            return render(request, 'login.html')

    else:
        return render(request, 'login.html',locals())            


