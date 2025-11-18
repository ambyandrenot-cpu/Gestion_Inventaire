# Ce fichier sert à créer des formulaires à partir du modèle.


from django import forms
from .models import Materiel

class MaterielForm(forms.ModelForm):
    class Meta:
        model = Materiel
        # AJOUT de 'quantite' pour le rendre saisissable
        fields = ['nom', 'categorie', 'quantite', 'quantite_bon', 'quantite_mauvais']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg', 'placeholder': 'Nom'}),
            'categorie': forms.Select(attrs={'class': 'w-full p-2 border rounded-lg'}),
            # AJOUT du widget pour 'quantite'
            'quantite': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded-lg', 'min': 0}),
            'quantite_bon': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded-lg', 'min': 0}),
            'quantite_mauvais': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded-lg', 'min': 0}),
        }
    
    def clean(self):
        cleaned = super().clean()
        
        quantite = cleaned.get('quantite') or 0
        bon = cleaned.get('quantite_bon') or 0
        mauvais = cleaned.get('quantite_mauvais') or 0
        
        # AJOUT de la validation dans le formulaire pour informer l'utilisateur immédiatement
        # que la somme des parties ne peut pas être supérieure au total.
        if (bon + mauvais) > quantite:
             # On lève une erreur : le total doit être au moins égal à la somme des parties.
             raise forms.ValidationError(
                 f"La somme du matériel Bon ({bon}) et Mauvais ({mauvais}) ({bon + mauvais}) ne peut pas dépasser la Quantité Totale ({quantite})."
             )

        if bon < 0 or mauvais < 0:
            raise forms.ValidationError("Les quantités doivent être supérieures ou égales à 0.")
            
        return cleaned