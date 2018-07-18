# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *

# Create your views here.
def index(request):           
    return render(request, 'login_registration_app/index.html')

def success(request):
    #needs logic to handle if logged in or not
    if 'user_id' not in request.session:
        messages.error(request, 'please log in before viewing pages')
        return redirect('/login_registration_app/')
    all_users = User.objects.all()
    logged_user = User.objects.get(id = request.session['user_id'])
    context = {
        'all_users': all_users,
        'logged_user': logged_user
    }
    # need to know name of whois logged in and probably their id number
    # use se
    # make sure you query the user created and store that as user that is passed as a tubple for success/fail using.  ex (failed = failse,errors), passed = true, user id)
    # maybe run query to get that users info? so we can get name?
    return render(request, 'login_registration_app/success.html', context)

def register(request):
    
    results = User.objects.registration_validator(request.POST)
    print results
    if results[0]:
        request.session['user_id'] = results[1].id
        messages.error(request, 'Yay! You registered and are now logged in!')
        # set session variables for user.id, which is results[1]
        return redirect('/login_registration_app/success')
    else:
        for key, error_message in results[1].iteritems():
            messages.error(request, error_message, extra_tags=key)
        return redirect('/login_registration_app/')
        
    # if VALIDATED BRO:
        # set session variables for id/name
    return redirect ('/login_registration_app/success')
    # else:
        # return redirect('/login_registration_app/login_registration')

def login(request):
    results = User.objects.login_validator(request.POST)
    if results[0]:
        request.session['user_id'] = results[1].id
        messages.error(request, 'Yay! You are now logged in!')
        # set session variables for user.id, which is results[1]
        return redirect('/login_registration_app/success')
    else:
        for key, error_message in results[1].iteritems():
            messages.error(request, error_message, extra_tags=key)
        return redirect('/login_registration_app/')

def logout(request):
    request.session.flush()
    return redirect ('/login_registration_app')

def delete(request, user_id):
    this_user = User.objects.get(id=user_id)
    print this_user
    this_user.delete()
    this_user.save
    return redirect ('/login_registration_app')

