from django.contrib import admin
from .models import Materiel
# Register your models here.

@admin.register(Materiel)
class MaterielAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'type_appareil', 'numero_serie', 'etat')
    search_fields = ('nom', 'type_appareil', 'numero_serie')