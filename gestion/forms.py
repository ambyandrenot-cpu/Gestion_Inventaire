# Ce fichier sert à créer des formulaires à partir du modèle.


from django import forms
from .models import Materiel

class MaterielForm(forms.ModelForm):
    class Meta:
        model = Materiel
        # Inclure les champs principaux, y compris bon/mauvais
        fields = ['nom', 'categorie', 'quantite_bon', 'quantite_mauvais']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg', 'placeholder': 'Nom'}),
            'categorie': forms.Select(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'quantite_bon': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded-lg', 'min': 0}),
            'quantite_mauvais': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded-lg', 'min': 0}),
        }
    # On a ajoute ce def clean() pour verifier que les valeurs saisies sont valides avant d’enregistrer le materiel.
    def clean(self):
        cleaned = super().clean()
        bon = cleaned.get('quantite_bon') or 0
        mauvais = cleaned.get('quantite_mauvais') or 0

        # Optionnel : tu peux valider la logique (ici on autorise tout mais on garantit entiers >=0)
        if bon < 0 or mauvais < 0:
            raise forms.ValidationError("Les quantités doivent être supérieures ou égales à 0.")
        return cleaned