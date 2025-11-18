# C'est ici que tout les logiques metiers CRUD se passe, le point reliant entre le models(BDD) et le templates(affichage)


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Materiel
from .forms import MaterielForm
from django.db.models import Q
import openpyxl
from openpyxl.styles import Font

def liste_materiels(request):
    action = request.GET.get("action")
    id_materiel = request.GET.get("id")

    form = None
    edit_obj = None
    delete_obj = None

    if action == "add":
        form = MaterielForm()

    elif action == "edit" and id_materiel:
        edit_obj = get_object_or_404(Materiel, id=id_materiel)
        form = MaterielForm(instance=edit_obj)

    elif action == "delete" and id_materiel:
        delete_obj = get_object_or_404(Materiel, id=id_materiel)

    query = request.GET.get("q", "")
    materiels = Materiel.objects.all().order_by('-date_ajout')
    if query:
        # On filtre : Soit le nom contient le texte, SOIT la catégorie contient le texte
        materiels = materiels.filter(
            Q(nom__icontains=query) | Q(categorie__icontains=query)
        )

    return render(request, "gestion/main.html", {
        "materiels": materiels,
        "action": action,
        "form": form,
        "edit_obj": edit_obj,
        "delete_obj": delete_obj,
        "query": query,
    })


def ajouter_materiel(request):
    """
    Traite l'ajout d'un nouveau matériel. 
    Initialise la quantité 'bon' par défaut à la quantité totale saisie.
    """
    if request.method == "POST":
        form = MaterielForm(request.POST)
        if form.is_valid():
            m = form.save(commit=False)
            
            # 1. Récupérer le total saisi
            total = m.quantite
            
            # 2. Initialiser quantite_bon. 
            # Si l'utilisateur n'a pas (ou a mis 0 dans) quantite_mauvais, 
            # on suppose que tout le stock est en bon état par défaut.
            if m.quantite_mauvais == 0:
                m.quantite_bon = total
            
            # 3. La méthode save() dans models.py s'occupera ensuite de la cohérence 
            # (quantite_bon = quantite - quantite_mauvais) si les trois champs ont été remplis.
            
            # --- Fin de la logique d'initialisation ---
            
            m.save()
    return redirect("liste_materiels")


def modifier_materiel(request, pk):
    materiel = get_object_or_404(Materiel, id=pk)
    if request.method == "POST":
        form = MaterielForm(request.POST, instance=materiel)
        if form.is_valid():
            # On sauvegarde: save() du model mettra à jour quantite
            form.save()
    return redirect("liste_materiels")


def supprimer_materiel(request, pk):
    materiel = get_object_or_404(Materiel, id=pk)
    materiel.delete()
    return redirect("liste_materiels")


def exporter_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Matériels"

    headers = ['ID', 'Nom', 'Catégorie', 'Quantité totale', 'Bon', 'Mauvais', 'Date d\'ajout']
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = Font(bold=True)

    materiels = Materiel.objects.all()
    for row_idx, m in enumerate(materiels, 2):
        ws.cell(row=row_idx, column=1, value=m.id)
        ws.cell(row=row_idx, column=2, value=m.nom)
        ws.cell(row=row_idx, column=3, value=m.categorie)
        ws.cell(row=row_idx, column=4, value=m.quantite)
        ws.cell(row=row_idx, column=5, value=m.quantite_bon)
        ws.cell(row=row_idx, column=6, value=m.quantite_mauvais)
        ws.cell(row=row_idx, column=7, value=m.date_ajout.strftime("%Y-%m-%d %H:%M"))

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="materiels.xlsx"'
    wb.save(response)
    return response

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenue {username}!')
            return redirect('dashboard')  # Redirection après connexion
        else:
            messages.error(request, 'Identifiants incorrects')
    
    return render(request, 'login.html')

def custom_login(request):
    # Si l'utilisateur est déjà connecté, redirigez-le vers liste_demande
    if request.user.is_authenticated:
        return redirect('liste_demande')  # ← Changement ici
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenue {username} !')
            return redirect('liste_demande')  # ← Changement ici
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    
    return render(request, 'gestion/login.html')

    @login_required
    def liste_demande(request):
    # Votre logique pour la liste des demandes
        context = {
        'title': 'Liste des Demandes',
        'message': 'Bienvenue sur la page des demandes'
    }
    return render(request, 'gestion/liste_demande.html', context)