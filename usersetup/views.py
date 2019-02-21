# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.urls import reverse
from authentication.models import userprofile
from .forms import UserProfileForm
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from Mobilebuilder.decorators import myadmin_login_required
import json

#Display the User Details
@myadmin_login_required
def userindex(request):
    adminid = request.session['loggedinuserid']
    adminname = userprofile.objects.get(pk=adminid)
    print adminname
    users = userprofile.objects.filter(is_user = True, adminuserid = adminid )
    context = {'users':users}
    return render(request, 'userindex.html', locals())

#Validate Entered mail-id onFocus Out
@csrf_exempt
def mailValidation(request):
    if request.method == 'POST':
        if request.POST.get('emailid'):
            mailid = request.POST.get('emailid')
            print mailid
        try:
            usermail = userprofile.objects.get(email=mailid)
        except userprofile.DoesNotExist:
            usermail= None
        if usermail:
            return HttpResponse ('This mail-id is in use')
        else:
            return HttpResponse ('')

#Add new user 
@csrf_exempt

def usersgup(request):
    adminid = request.session['loggedinuserid']
    adminname = userprofile.objects.get(pk=adminid)
    if request.method == 'POST':
    	userid = request.session['loggedinuserid']
        form = UserProfileForm(request.POST)
        if form.is_valid():
            newuser = form.save(commit=False)
            newuser.adminuserid = userid
            newuser.save()
            return HttpResponseRedirect('/usersetup/userindex')
        else:
            response = {
                'responseType':'Failure',
            }
            return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        form = UserProfileForm() #An Unbound Form
        return render(request, 'usersignup.html',locals())

#Delete User
@myadmin_login_required
def delete(request, id):
    query = userprofile.objects.get(pk=id)
    query.delete()
    return HttpResponseRedirect('/usersetup/userindex/')

#Edit User 
@myadmin_login_required
def edit(request, id):
    adminid = request.session['loggedinuserid']
    adminname = userprofile.objects.get(pk=adminid)
    query = userprofile.objects.get(pk=id)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=query)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect('/usersetup/userindex/')
    else:
        form = UserProfileForm(instance=query) #An Unbound Form
        
    return render(request, 'useredit.html', locals())
    
