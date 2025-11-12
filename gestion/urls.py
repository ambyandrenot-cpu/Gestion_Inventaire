from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
]
# C’est ici qu’on relie les pages (routes).
