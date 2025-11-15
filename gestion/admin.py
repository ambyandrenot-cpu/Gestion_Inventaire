from django.contrib import admin
from .models import Materiel

@admin.register(Materiel)
class MaterielAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'categorie', 'quantite', 'etat', 'date_ajout')
    search_fields = ('nom', 'categorie')
    list_filter = ('etat', 'categorie')