from django import forms
from course.models import Term

class TermChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, term):
        return term.name

class ScheduleForm(forms.Form):
    term = TermChoiceField(widget=forms.Select(attrs={'onchange':'this.form.submit()'}), queryset=Term.objects.all(), empty_label=None)
