from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import openpyxl
from openpyxl.styles import Font
from .models import Materiel,Demande # Ajoutez Demande si nécessaire
from .forms import MaterielForm
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import never_cache

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
    if request.method == "POST":
        form = MaterielForm(request.POST)
        if form.is_valid():
            m = form.save(commit=False)
            total = m.quantite
            if m.quantite_mauvais == 0:
                m.quantite_bon = total
            m.save()
    return redirect("liste_materiels")

def modifier_materiel(request, pk):
    materiel = get_object_or_404(Materiel, id=pk)
    if request.method == "POST":
        form = MaterielForm(request.POST, instance=materiel)
        if form.is_valid():
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

def custom_login(request):
    # Si l'utilisateur est déjà connecté, redirigez-le vers liste_demande
    if request.user.is_authenticated:
        return redirect('liste_demande')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenue {username} !')
            return redirect('liste_demande')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    
    return render(request, 'gestion/login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        # Validation des données
        if password != confirm_password:
            messages.error(request, 'Les mots de passe ne correspondent pas')
            return render(request, 'gestion/login.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Ce nom d\'utilisateur existe déjà')
            return render(request, 'gestion/login.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Cet email est déjà utilisé')
            return render(request, 'gestion/login.html')
        
        # Créer l'utilisateur
        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            messages.success(request, 'Compte créé avec succès ! Vous pouvez maintenant vous connecter.')
            return redirect('custom_login')  # Rediriger vers la page de connexion
            
        except Exception as e:
            messages.error(request, f'Erreur lors de la création du compte: {str(e)}')
            return render(request, 'gestion/login.html')
    
    return render(request, 'gestion/login.html')

@login_required
@never_cache
def liste_demande(request):
    # Votre logique pour afficher les demandes
    # Seuls les utilisateurs connectés peuvent accéder à cette vue
    try:
        demandes = Demande.objects.all()  # Assurez-vous que le modèle Demande existe
    except:
        demandes = []  # Liste vide si le modèle n'existe pas encore
    
    context = {
        'user': request.user,
        'demandes': demandes,
        'title': 'Liste des Demandes',
        'message': 'Bienvenue sur la page des demandes'
    }
    return render(request, 'gestion/liste_demande.html', context)


@require_http_methods(["POST"])

def logout_view(request):
    logout(request)
    messages.success(request, 'Vous avez été déconnecté avec succès. Veuillez vous reconnecter.')
    return redirect('login')

