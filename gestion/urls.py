from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_static, name='main'),
    # path('add/', views.add_materiel, name='add_materiel'),
    # path('edit/<int:pk>/', views.edit_materiel, name='edit_materiel'),
    # path('delete/<int:pk>/confirm/', views.delete_confirm, name='delete_confirm'),
    # path('export/excel/', views.export_excel, name='export_excel'),
]