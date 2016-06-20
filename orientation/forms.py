from django import forms

class SearchForm(forms.Form):
    course = forms.CharField(label='Course', widget=forms.TextInput(attrs={'placeholder': '(ACCT, PHYS 151, etc.)'}), max_length=20, required=False)
    instructor = forms.CharField(label='Instructor name', max_length=50, required=False)
