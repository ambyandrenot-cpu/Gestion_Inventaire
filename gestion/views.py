from django.shortcuts import render
from .models import Materiel

def main_view(request):
    materiels = Materiel.objects.all()
    print("💡 Vue exécutée : main_view —", materiels)
    return render(request, 'gestion/main.html', {'materiels': materiels})