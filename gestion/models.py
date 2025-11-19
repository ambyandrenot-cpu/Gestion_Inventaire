# C’est ici qu’on définit les tables de la base de données..
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

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
        Nouvelle logique de cohérence :
        Le total (quantite) est le maître. 
        Bon est déduit de (Total - Mauvais), ou Mauvais est déduit de (Total - Bon).
        Puisque l'utilisateur modifie Bon ET Mauvais, nous devons laisser l'utilisateur
        modifier les deux et nous assurer que le Total est correct.
        
        MAIS, selon votre demande (Bon se modifie en même temps que Mauvais), 
        cela implique que : Bon = Total - Mauvais.
        
        Nous devons nous assurer que Mauvais et Bon n'excèdent pas Total.
        """
        
        # 1. Assurer que la somme des parties n'est pas supérieure au total saisi
        total_parts = self.quantite_bon + self.quantite_mauvais
        if total_parts > self.quantite:
            # Si la somme est supérieure au total, on doit déduire l'excédent de l'une des parties.
            # Supposons que l'utilisateur a modifié Mauvais, on ajuste Bon.
            self.quantite_bon = self.quantite - self.quantite_mauvais
            
            # Si le quantite_mauvais est aussi trop grand (cas extrême), on le limite.
            if self.quantite_bon < 0:
                 self.quantite_bon = 0
                 self.quantite_mauvais = self.quantite
        
        # 2. Après l'ajustement, le total doit toujours être Bon + Mauvais.
        #    Puisque nous avons limité Bon et Mauvais pour qu'ils ne dépassent pas Quantite,
        #    nous laissons le total saisi par l'utilisateur.

        # 3. L'ajustement demandé : Quand on modifie Mauvais, Bon s'ajuste.
        #    Cette logique est gérée par le `clean` du formulaire pour l'utilisateur,
        #    mais la ligne ci-dessous assure l'intégrité finale si le total est fixé.
        self.quantite_bon = self.quantite - self.quantite_mauvais
        
        # S'assurer que 'bon' ne devient pas négatif
        if self.quantite_bon < 0:
            self.quantite_bon = 0
            self.quantite_mauvais = self.quantite

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
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    # Ajouter related_name personnalisé pour éviter les conflits
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='customuser_set',  # ← CHANGEMENT ICI
        related_query_name='customuser',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='customuser_set',  # ← CHANGEMENT ICI
        related_query_name='customuser',
    )
    
    def __str__(self):
        return self.username
    
class Demande(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    materiel = models.ForeignKey(Materiel, on_delete=models.CASCADE)
    quantite_demandee = models.IntegerField()
    # Enregistrer aussi le nom/email saisis par le demandeur (facultatif)
    nom_demandeur = models.CharField(max_length=150, blank=True, null=True)
    email_demandeur = models.EmailField(blank=True, null=True)
    # Indique si l'utilisateur a été notifié du changement de statut
    user_notified = models.BooleanField(default=False)
    date_demande = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=[
        ('en_attente', 'En attente'),
        ('approuvee', 'Approuvée'),
        ('refusee', 'Refusée')
    ], default='en_attente')
    
    def __str__(self):
        return f"{self.utilisateur.username} - {self.materiel.nom}"