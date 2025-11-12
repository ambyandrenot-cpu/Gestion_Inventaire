from django.db import models

# C’est ici qu’on définit les tables de la base de données..

class Materiel(models.Model):
    nom = models.CharField(max_length=100)
    type_appareil = models.CharField(max_length=100)
    numero_serie = models.CharField(max_length=100)
    etat = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nom} ({self.type_appareil})"