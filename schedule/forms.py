from django import forms
from course.models import Term
from account.models import Profile
from schedule.models import ScheduleEntry
from django.db.models import Q

class TermChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, term):
        return term.name

class ScheduleForm(forms.Form):
    term = TermChoiceField(widget=forms.Select(attrs={
    'onchange':'this.form.submit()',
    'class': 'form-control'
    }), queryset=None, empty_label=None)

    def __init__(self, user, *args, **kwargs):
        scheduled_terms = ScheduleEntry.objects.filter(user=user).values('term').distinct()
        terms = Term.objects.filter(pk__in=scheduled_terms)
        if len(terms) < 0:
            terms = [Term.objects.all()[0]]
        # Adding currently active terms to list:
        # terms = Term.objects.filter(Q(pk__in=scheduled_terms) | Q(update=True))
        # Adding all terms to list with profile setting:
        # if user.is_authenticated():
        #     profile = Profile.objects.get(user=user)
        #     if profile.show_archived_terms:
        #         terms = Term.objects.all()
        super(ScheduleForm, self).__init__(*args, **kwargs)
        self.fields['term'].queryset = terms

class ScheduleOptionsForm(forms.Form):
    show_colors = forms.BooleanField(label='Show colors', required=False)
    show_details = forms.BooleanField(label='Show course details', required=False)
