from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.liste_materiels, name="liste_materiels"),
    path("materiel/ajouter/", views.ajouter_materiel, name="add_materiel"),
    path("materiel/modifier/<int:pk>/", views.modifier_materiel, name="edit_materiel"),
    path("materiel/supprimer/<int:pk>/", views.supprimer_materiel, name="delete_materiel"),
    path("export-excel/", views.exporter_excel, name="export_excel"),
     path('login/', auth_views.LoginView.as_view(
        template_name='gestion/login.html',  # ← chemin complet
        redirect_authenticated_user=True
    ), name='login'),
       path('logout/', views.logout_view, name='logout'),
    path('demandes/', views.liste_demande, name='liste_demande'),
    path('register/', views.register_view, name='register'),
    path('custom_login/', auth_views.LoginView.as_view(template_name='login.html'), name='custom_login'),
]