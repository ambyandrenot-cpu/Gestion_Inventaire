# C’est ici qu’on définit les tables de la base de données..
from django.db import models

class Materiel(models.Model):
    nom = models.CharField(max_length=100)
    categorie = models.CharField(max_length=50, default="Inconnu")
    quantite = models.PositiveIntegerField()
    date_ajout = models.DateTimeField(auto_now_add=True)
    etat = models.CharField(
        max_length=50,
        choices=[
            ('Neuf', 'Neuf'),
            ('Bon', 'Bon'),
            ('Endommagé', 'Endommagé'),
        ]
    )

    def __str__(self):
        return self.nom