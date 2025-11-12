# C'est ici que tout les logiques metiers CRUD se passe, le point reliant entre le models(BDD) et le templates(affichage)
from django.shortcuts import render

def main_static(request):
    return render(request, 'main.html')