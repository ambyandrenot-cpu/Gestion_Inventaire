from django.urls import path
from . import views

urlpatterns = [
    path("", views.liste_materiels, name="liste_materiels"),
    path("materiel/ajouter/", views.ajouter_materiel, name="add_materiel"),
    path("materiel/modifier/<int:pk>/", views.modifier_materiel, name="edit_materiel"),
    path("materiel/supprimer/<int:pk>/", views.supprimer_materiel, name="delete_materiel"),
    path("export-excel/", views.exporter_excel, name="export_excel"),
]