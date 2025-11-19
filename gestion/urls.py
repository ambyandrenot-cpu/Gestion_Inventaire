from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.liste_materiels, name="liste_materiels"),
    path("materiel/ajouter/", views.ajouter_materiel, name="add_materiel"),
    path("materiel/modifier/<int:pk>/", views.modifier_materiel, name="edit_materiel"),
    path("materiel/supprimer/<int:pk>/", views.supprimer_materiel, name="delete_materiel"),
    path("export-excel/", views.exporter_excel, name="export_excel"),
    
    # URLs d'authentification
    path('login/', views.custom_login, name='login'),  # Utilise votre vue custom_login
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    
    # URLs admin - IMPORTANT: utilisez vos vues personnalisées
    path('admin_login/', views.admin_login, name='admin_login'),  # ← Votre vue personnalisée
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    path('demandes/', views.liste_demande, name='liste_demande'),
    path('emprunter/<int:pk>/', views.emprunter_materiel, name='emprunter_materiel'),
    path('admin_logout/', views.logout_admin, name='logout_admin'),
]