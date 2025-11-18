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
        - si quantite_bon + quantite_mauvais != quantite, on corrige quantite automatiquement
        - si quantite > 0 et un champ est supérieur, on ajuste rien (on laisse les valeurs fournies)
        """
        total = self.quantite_bon + self.quantite_mauvais
        if total != self.quantite:
            # On met à jour quantite pour refléter la somme des états
            self.quantite = total
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