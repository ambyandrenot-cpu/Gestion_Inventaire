# C’est ici qu’on définit les tables de la base de données..
from django.db import models

class Materiel(models.Model):
    nom = models.CharField(max_length=100)
    categorie = models.CharField(
        max_length=50,
        choices=[
            ('Ordinateur', 'Ordinateur'),
            ('Périphérique', 'Périphérique'),
            ('Equipement', 'Equipement'),
        ],
        default='Equipement'
    )
    # Quantité totale (derived: quantite_bon + quantite_mauvais should equal quantite)
    quantite = models.PositiveIntegerField()

    # Nouveaux champs demander : nombre 'bon' et nombre 'mauvais'
    quantite_bon = models.PositiveIntegerField(default=0)
    quantite_mauvais = models.PositiveIntegerField(default=0)

    date_ajout = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """
        Garantir la cohérence : 
        - Si la somme des parties dépasse le total saisi, on ajuste la quantité totale 
          à la somme des parties pour garantir l'intégrité des données.
        - On laisse l'utilisateur saisir les trois champs.
        """
        total_parts = self.quantite_bon + self.quantite_mauvais
        
        # Logique de cohérence:
        # Si la quantité saisie est inférieure à la somme des parties,
        # cela signifie que le total est incorrect. On corrige le total
        # pour correspondre à la somme des parties.
        if self.quantite < total_parts:
            self.quantite = total_parts
            
        # Alternative (plus stricte, mais cohérente):
        # Si l'utilisateur saisit un total > 0, mais que la somme des parties est 0, 
        # il y a une incohérence potentielle. Pour l'instant, on laisse la valeur saisie 
        # tant qu'elle est >= total_parts.

        super().save(*args, **kwargs)

    @property
    def disponible(self):
        """Alias utile si on veux l'ancien nom; correspond maintenant à quantite_mauvais."""
        return self.quantite_mauvais

    @property
    def empruntes(self):
        """Alias si on veux l'ancien nom empruntés -> quantité 'bon' si on l'as demandé."""
        return self.quantite_bon

    def __str__(self):
        return self.nom