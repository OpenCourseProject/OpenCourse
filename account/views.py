from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.contrib.auth import logout as auth_logout
from account.models import Profile
from account.forms import ProfileForm
from course.models import FollowEntry
from course.utils import follow_get_courses
from django.contrib.auth.decorators import login_required

def account(request):
    context = {
        'user': request.user,
        'authenticated': request.user.is_authenticated(),
        }
    if request.user.is_authenticated():
        profile = Profile.objects.get(user=request.user)
        if request.method == 'POST':
            form = ProfileForm(request.POST)
            if form.is_valid():
                default_term = form.cleaned_data['default_term']
                learning_community = form.cleaned_data['learning_community']
                preferred_name = form.cleaned_data['preferred_name']
                major = form.cleaned_data['major']
                private = form.cleaned_data['private']
                show_archived_terms = form.cleaned_data['show_archived_terms']
                show_colors_schedule = form.cleaned_data['show_colors_schedule']
                show_details_schedule = form.cleaned_data['show_details_schedule']
                profile.default_term = default_term
                profile.learning_community = learning_community
                profile.preferred_name = preferred_name
                profile.major = major
                profile.private = private
                profile.show_archived_terms = show_archived_terms
                profile.show_colors_schedule = show_colors_schedule
                profile.show_details_schedule = show_details_schedule
                profile.save()
        else:
            form = ProfileForm()
            if profile.default_term:
                form.fields['default_term'].initial = profile.default_term
            if profile.learning_community:
                form.fields['learning_community'].initial = profile.learning_community
            if profile.major:
                form.fields['major'].initial = profile.major
            if profile.private:
                form.fields['private'].initial = profile.private
            if profile.show_archived_terms:
                form.fields['show_archived_terms'].initial = profile.show_archived_terms
            if profile.show_colors_schedule:
                form.fields['show_colors_schedule'].initial = profile.show_colors_schedule
            if profile.show_details_schedule:
                form.fields['show_details_schedule'].initial = profile.show_details_schedule
            if profile.preferred_name:
                form.fields['preferred_name'].initial = profile.preferred_name
            else:
                form.fields['preferred_name'].initial = request.user.first_name
        context['form'] = form
        follows = FollowEntry.objects.filter(user=request.user)
        if len(follows) > 0:
            context['followed_courses'] = follow_get_courses(follows)
    else:
        if 'next' in request.GET:
            context['next'] = request.GET['next']
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
