# Ce fichier sert à créer des formulaires à partir du modèle.


from django import forms
from .models import Materiel

class MaterielForm(forms.ModelForm):
    class Meta:
        model = Materiel
        # La liste des champs reste la même que dans la dernière correction
        fields = ['nom', 'categorie', 'quantite', 'quantite_bon', 'quantite_mauvais']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg', 'placeholder': 'Nom'}),
            'categorie': forms.Select(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'quantite': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded-lg', 'min': 0}),
            'quantite_bon': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded-lg', 'min': 0}),
            'quantite_mauvais': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded-lg', 'min': 0}),
        }
    
    # On simplifie grandement la méthode clean()
    def clean(self):
        cleaned = super().clean()
        
        bon = cleaned.get('quantite_bon') or 0
        mauvais = cleaned.get('quantite_mauvais') or 0

        # On garde seulement la vérification de base (quantités non négatives)
        if bon < 0 or mauvais < 0:
            raise forms.ValidationError("Les quantités doivent être supérieures ou égales à 0.")
            
        # NOTE : La validation Total > (Bon + Mauvais) est maintenant gérée dans models.py.
        # Cela permet à la logique de save() de faire les ajustements finaux.
        
        return cleaned