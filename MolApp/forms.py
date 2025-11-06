
from .models import Projects
from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class projectForm(forms.ModelForm):
    OPTIONS = [
        ('Toutes', 'Toutes'),
        ('Actuelle', 'Actuelle'), 
        ('Personnaliser', 'Personnaliser'),
    ]

    option = forms.ChoiceField(
        choices=OPTIONS,
        widget=forms.RadioSelect(attrs={
            'name': "optionsRadios",
        }),
        required=True,
    )
    class Meta:
        model = Projects
        fields = ['url_site', 'option', 'pages', 'nom_fichier']
        widgets = {
            'url_site': forms.URLInput(attrs={'class': "form-control", 'id': "first-name", 'name': "url"}),
            'option': forms.RadioSelect(attrs={'name': "optionsRadios", "type": "radio"}),
            'pages': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex: 1-6, 8,10'}),
            'nom_fichier': forms.TextInput(attrs={'id': "first-name", 'name': "nom_excel", 'class': "form-control"})
        }


class editProjectForm(forms.ModelForm):
    class Meta :
        model=Projects
        fields=['nom_fichier']

