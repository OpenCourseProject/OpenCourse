from django import forms
from opencourse.models import Report

class ReportForm(forms.Form):
    url = forms.CharField(widget=forms.HiddenInput())
    description = forms.CharField(label="What's happening?", widget=forms.Textarea)
