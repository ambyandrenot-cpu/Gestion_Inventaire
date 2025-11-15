# Ce fichier sert à créer des formulaires à partir du modèle.


from django import forms
from .models import Materiel
class MaterielForm(forms.ModelForm):
    class Meta:
        model = Materiel
        fields = ['nom', 'categorie', 'quantite', 'etat']

        widgets = {
            'nom': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg', 'placeholder': 'Nom'}),
            'categorie': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg', 'placeholder': 'Catégorie'}),
            'quantite': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded-lg', 'min': 1}),
            'etat': forms.Select(attrs={'class': 'w-full p-2 border rounded-lg'}),
        }