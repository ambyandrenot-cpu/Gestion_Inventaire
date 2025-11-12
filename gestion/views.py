from django.shortcuts import render

def home(request):
    return render(request, 'gestion/main.html')
                  
# C’est ici qu’on met la logique — afficher la liste, ajouter, modifier, supprimer..
