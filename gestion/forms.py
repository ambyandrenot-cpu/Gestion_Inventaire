# Ce fichier sert à créer des formulaires à partir du modèle.
# Juste un exemple de code ci-dessou

from django import forms
from .models import Materiel


class MaterielForm(forms.ModelForm):
    class Meta:
        model = Materiel
        fields = ['nom', 'type_appareil', 'numero_serie', 'etat']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg', 'placeholder': 'Nom'}),
            'type_appareil': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg', 'placeholder': "Type d'appareil"}),
            'numero_serie': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg', 'placeholder': 'Numéro de série'}),
            'etat': forms.Select(attrs={'class': 'w-full p-2 border rounded-lg'}),
        }