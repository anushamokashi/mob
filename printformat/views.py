# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.forms.models import modelformset_factory
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect,HttpResponse,HttpResponseBadRequest

from models import PrintFormat,PrintFormatSQL
from forms import PrintFormatForm,PrintFormatSQLForm
from project.models import Project, Projectwiseusersetup

from slugify import slugify
regex_pattern = r'[^-a-z0-9_]+'


# Create your views here.
        

@csrf_exempt
def printformatindex(request):

    element =Projectwiseusersetup.objects.get(userid=request.session['userid'],project_id = request.session['projectid'])              
    projectselect =Projectwiseusersetup.objects.filter(userid=request.session['userid'])
    if element.setasdefaultproject or request.session['projectid']:
        project_title = element.project_id.title
    
    projectid = request.session['projectid']

    try:
        printFormatObj = PrintFormat.objects.filter(project_id=projectid)
    except PrintFormat.DoesNotExist:
        printFormatObj= None

    return render(request,"printformat.html",locals()) 


PrintFormatSQLFormSet = modelformset_factory(PrintFormatSQL,form = PrintFormatSQLForm,can_delete=True,extra=1) 

def addNewFormat(request):
    
    rpf_form=PrintFormatForm(request.POST or None,request.FILES or None)
    formset = PrintFormatSQLFormSet(request.POST or None,queryset=PrintFormatSQL.objects.none())

    projectid = request.session['projectid']

    if request.method == "POST":
        if rpf_form.is_valid():
            try:
                pfTitle = request.POST.get('title')
                pfaction=rpf_form.save(commit=False)
                pfaction.project_id = projectid
                pfaction.slug = slugify(pfTitle, separator='_', regex_pattern=regex_pattern)
                try:
                    pfaction.save()
                except Exception as e:
                    print e
                    return HttpResponse("TITLE")
                print "**********"
                print pfaction.htmlfile

                for form in formset:
                    if form.is_valid() and form.cleaned_data.get('DELETE') and form.instance.pk:
                        print "************DELETE*******************"
                        print form.instance.pk
                        form.instance.delete()
                    elif form.is_valid() and form.cleaned_data:
                        print "************VALID*********************"
                        print form.is_valid()
                    
                        instance = form.save(commit=False)
                        instance.printformat_id = pfaction.id
                        print instance.id
                        try:
                            instance.save()
                        except Exception as e:
                            print e
                            return HttpResponse("DO")
                    elif not form.is_valid():
                        return HttpResponse("Failure")
                return HttpResponse("Success")
            except Exception as e:
                print e
                return HttpResponse("Failure")

        else:
          return HttpResponse("Failure")
                
    else:
        return render(request,"printformatmodal.html",locals())      

def updtaePFFormat(request,id):
    pfObj = PrintFormat.objects.get(id=id)
    rpf_form=PrintFormatForm(request.POST or None,request.FILES or None,instance=pfObj)
    formset = PrintFormatSQLFormSet(request.POST or None,queryset=PrintFormatSQL.objects.filter(printformat_id=pfObj.id))

    projectid = request.session['projectid']

    if request.method == "POST":
        if rpf_form.is_valid():
            try:
                pfTitle = request.POST.get('title')
                
                pfaction=rpf_form.save(commit=False)
                pfaction.project_id = projectid
                pfaction.slug = slugify(pfTitle, separator='_', regex_pattern=regex_pattern)
                
                try:
                    pfaction.save()
                except Exception as e:
                    print e
                    return HttpResponse("TITLE")
                print "**********"
                print pfaction.htmlfile

                for form in formset:
                    print form.is_valid()
                    if form.is_valid() and form.cleaned_data.get('DELETE') and form.instance.pk:
                        print "************DELETE*******************"
                        print form.instance.pk
                        form.instance.delete()
                    elif form.is_valid() and form.cleaned_data:
                        print "************VALID*********************"
                        print form.is_valid()
                    
                        instance = form.save(commit=False)
                        instance.printformat_id = pfaction.id
                        print instance.id
                        try:
                            instance.save()
                        except Exception as e:
                            print e
                            return HttpResponse("DO")
                    elif not form.is_valid():
                        return HttpResponse("Failure")
                return HttpResponse("Success")
            except Exception as e:
                print e
                return HttpResponse("Failure")

        else:
          return HttpResponse("Failure")
                
    else:
        return render(request,"printformatupdatemodal.html",locals())

def deletePFFormat(request,id):
    query = PrintFormat.objects.get(id=id)
    query.delete()
    return HttpResponseRedirect('/printformat/printformatindex/')
    

