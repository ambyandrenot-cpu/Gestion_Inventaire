# C'est ici que tout les logiques metiers CRUD se passe, le point reliant entre le models(BDD) et le templates(affichage)

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Materiel
from .forms import MaterielForm
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
    if query:
        materiels = Materiel.objects.filter(nom__icontains=query)
    else:
        materiels = Materiel.objects.all()

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
            # m.quantite sera calculé dans save() du model
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