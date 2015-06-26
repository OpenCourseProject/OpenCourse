from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.contrib.auth import logout as auth_logout
from account.models import Profile
from account.forms import ProfileForm
from django.contrib.auth.decorators import login_required

def account(request):
    form = None
    next = None
    if request.user.is_authenticated():
        profile = Profile.objects.get(user=request.user)
        if request.method == 'POST':
            form = ProfileForm(request.POST)
            if form.is_valid():
                default_term = form.cleaned_data['default_term']
                learning_community = form.cleaned_data['learning_community']
                profile.default_term = default_term
                profile.learning_community = learning_community
                profile.save()
        else:
            form = ProfileForm()
            if profile.default_term:
                form.fields['default_term'].initial = profile.default_term
            if profile.learning_community:
                form.fields['learning_community'].initial = profile.learning_community
    else:
        if 'next' in request.GET:
            next = request.GET['next']
    context = {
        'user': request.user,
        'authenticated': request.user.is_authenticated(),
        'form': form,
        'next': next,
    }
    return render(request, 'account/account.html', context)

@login_required
def link_facebook(request):
    if request.method == 'GET':
        facebook_id = request.GET['facebook_id']
        profile = Profile.objects.get(user=request.user)
        if not profile.facebook_id or profile.facebook_id != facebook_id:
            profile.facebook_id = facebook_id
            profile.save()
        return HttpResponse('OK', 201)
    else:
        return HttpResponse('Method not allowed', 405)

def logout(request):
    auth_logout(request)
    return redirect('/')
