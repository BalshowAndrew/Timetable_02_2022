from django import forms
from .models import Classes

class QueryForm(forms.Form):
    LECTURE = 'L'
    PRACTICE = 'P'
    CATEGORY_CHOICES = [
        (LECTURE, 'лекция'),
        (PRACTICE, ' практическое'),
    ]
    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        label='Категория занятия',
        widget=forms.Select()
    )
    first_day = forms.DateField(
        label='Первый день',
        widget=forms.TextInput(
            attrs={
            'type':'date'
        })

    )
    last_day = forms.DateField(
        label='Последний день',
        widget=forms.TextInput(
            attrs={
                'type':'date'
            })
    )
