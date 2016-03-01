from django import forms
from course.models import Term, Attribute
from course.widgets import SelectTimeWidget
from account.models import Profile

class TermChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, term):
        return term.name

class AttributeChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, attribute):
        return attribute.name

class SearchForm(forms.Form):
    term = TermChoiceField(widget=forms.Select(attrs={'onchange':'this.form.submit()'}), queryset=None, empty_label=None)
    crn = forms.IntegerField(label='CRN', required=False)
    course = forms.CharField(label='Course', widget=forms.TextInput(attrs={'placeholder': '(ACCT, PHYS 151, etc.)'}), max_length=20, required=False)
    days = forms.CharField(label='Days', widget=forms.TextInput(attrs={'placeholder': '(M, MWF, TR, etc.)'}), max_length=5, required=False)
    time = forms.TimeField(label='Time', widget=SelectTimeWidget(minute_step=30, second_step=60, twelve_hr=True), required=False)
    instructor = forms.CharField(label='Instructor name', max_length=50, required=False)
    min_rating = forms.DecimalField(label='Instructor rating', decimal_places=1, max_digits=2, required=False)
    attribute = AttributeChoiceField(label='Fulfills', queryset=Attribute.objects.all(), required=False)
    show_closed = forms.BooleanField(label='Show closed courses', initial=True, required=False)

    def __init__(self, user, *args, **kwargs):
        terms = Term.objects.filter(update=True)
        if user.is_authenticated():
            profile = Profile.objects.get(user=user)
            if profile.show_archived_terms:
                terms = Term.objects.all()
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['term'].queryset = terms

class InstructorSuggestionForm(forms.Form):
    email_address = forms.EmailField(label='Professor Email', required=False)
    rmp_link = forms.URLField(label='RateMyProfessor URL', required=False)
