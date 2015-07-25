from django import forms
from course.models import Term, Attribute
from course.widgets import SelectTimeWidget

class TermChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, term):
        return term.name

class AttributeChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, attribute):
        return attribute.name

class SearchForm(forms.Form):
    term = TermChoiceField(widget=forms.Select(attrs={'onchange':'this.form.submit()'}), queryset=Term.objects.all(), empty_label=None)
    crn = forms.IntegerField(label='CRN', required=False)
    course = forms.CharField(label='Course', widget=forms.TextInput(attrs={'placeholder': '(ACCT, PHYS 151, etc.)'}), max_length=20, required=False)
    days = forms.CharField(label='Days', widget=forms.TextInput(attrs={'placeholder': '(M, MWF, TR, etc.)'}), max_length=5, required=False)
    start = forms.TimeField(label='Start time', widget=SelectTimeWidget(minute_step=30, second_step=60, twelve_hr=True), required=False)
    end = forms.TimeField(label='End time', widget=SelectTimeWidget(minute_step=5, second_step=60, twelve_hr=True), required=False)
    instructor = forms.CharField(label='Instructor name', max_length=50, required=False)
    min_rating = forms.DecimalField(label='Instructor rating', decimal_places=1, max_digits=2, required=False)
    attribute = AttributeChoiceField(label='Fulfills', queryset=Attribute.objects.all(), required=False)
    show_closed = forms.BooleanField(label='Show closed courses', initial=True, required=False)

class InstructorSuggestionForm(forms.Form):
    link = forms.URLField(label='RateMyProfessor URL')
