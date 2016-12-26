from django import forms
from .models import Component


class CreateComponentFrom(forms.Form):
    name = forms.CharField(label='Name of component')
    component_type = forms.ChoiceField(choices=Component.ComponentType.choices)

    # def clean_name(self):
    #     name = self.cleaned_data['name']
    #     if len(name.strip()) < 10:
    #         raise forms.ValidationError('Name of component less than 10 chars')
    #     return name
