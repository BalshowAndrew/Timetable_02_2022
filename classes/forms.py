from django import forms
from .models import Queries


# class QueryForm(forms.Form):
#     LECTURE = 'L'
#     PRACTICE = 'P'
#     CATEGORY_CHOICES = [
#         (LECTURE, 'лекция'),
#         (PRACTICE, ' практическое'),
#     ]
#     category = forms.ChoiceField(
#         choices=CATEGORY_CHOICES,
#         label='Категория занятия',
#         widget=forms.Select(
#             attrs={
#                 'class': 'form-control'
#             })
#     )
#     first_day = forms.DateField(
#         label='Первый день',
#         widget=forms.TextInput(
#             attrs={
#                 'class': 'form-control',
#                 'type': 'date'
#             })
#     )
#     last_day = forms.DateField(
#         label='Последний день',
#         widget=forms.TextInput(
#             attrs={
#                 'class': 'form-control',
#                 'type': 'date'
#             })
#     )

class QueryForm(forms.ModelForm):
    class Meta:
        model = Queries
        fields = ['category', 'first_day', 'last_day']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'first_day': forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
            'last_day': forms.TextInput(attrs={'class': 'form-control', 'type': 'date'})
        }