from django.urls import path
from . import views

urlpatterns = [
    path("", views.liste_materiels, name="liste_materiels"),
    path("materiel/ajouter/", views.ajouter_materiel, name="add_materiel"),
    path("materiel/modifier/<int:pk>/", views.modifier_materiel, name="edit_materiel"),
    path("materiel/supprimer/<int:pk>/", views.supprimer_materiel, name="delete_materiel"),
    path("materiel/emprunter/<int:pk>/", views.emprunter_materiel, name="emprunter_materiel"),
    path("materiel/rendre/<int:pk>/", views.rendre_materiel, name="rendre_materiel"),
    path("export-excel/", views.exporter_excel, name="export_excel"),
]