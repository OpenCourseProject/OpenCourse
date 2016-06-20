from django import forms
from account.models import Profile
from course.models import Term

class TermChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, term):
        return term.name

class ProfileForm(forms.Form):
    preferred_name = forms.CharField(label='Preferred Name', max_length=50)
    default_term = TermChoiceField(queryset=Term.objects.all(), empty_label="Choose a term", required=False)
    learning_community = forms.CharField(label='Learning Community', max_length=100, required=False)
    major = forms.CharField(label='Major', max_length=50)
    show_archived_terms = forms.BooleanField(label='Show old terms when searching', required=False)
    show_colors_schedule = forms.BooleanField(label='Show colors on schedule', required=False)
    show_details_schedule = forms.BooleanField(label='Show course details on schedule', required=False)
