from django import forms
from account.models import Profile
from course.models import Term

class TermChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, term):
        return term.name

class ProfileForm(forms.Form):
    default_term = TermChoiceField(queryset=Term.objects.all(), empty_label="Choose a term")
    student_id = forms.CharField(label='Student ID', max_length=10, required=False)
