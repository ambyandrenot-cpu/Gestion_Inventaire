from django.contrib import admin
from .models import Materiel

@admin.register(Materiel)
class MaterielAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'categorie', 'quantite', 'quantite_bon', 'quantite_mauvais', 'date_ajout')
    search_fields = ('nom', 'categorie')
    list_filter = ('categorie',)