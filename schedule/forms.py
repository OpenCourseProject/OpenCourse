from django import forms
from course.models import Term
from account.models import Profile

class TermChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, term):
        return term.name

class ScheduleForm(forms.Form):
    term = TermChoiceField(widget=forms.Select(attrs={
    'onchange':'this.form.submit()',
    'class': 'form-control'
    }), queryset=None, empty_label=None)

    def __init__(self, user, *args, **kwargs):
        terms = Term.objects.filter(update=True)
        if user.is_authenticated():
            profile = Profile.objects.get(user=user)
            if profile.show_archived_terms:
                terms = Term.objects.all()
        super(ScheduleForm, self).__init__(*args, **kwargs)
        self.fields['term'].queryset = terms

class ScheduleOptionsForm(forms.Form):
    show_colors = forms.BooleanField(label='Show colors', required=False)
    show_details = forms.BooleanField(label='Show course details', required=False)
