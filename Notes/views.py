from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import *

# Create your views here.

def index(request):
    return render(request, "notes/index.html")

def eleves(request):
    eleves = Eleve.objects.all()
    return render(request, 'notes/liste_eleve.html', {'eleves':eleves})

def eleve(request, eleve_id):
    eleve = get_object_or_404(Eleve, pk=eleve_id)
    notes = Note.objects.filter(eleve=eleve)
    context ={'eleve': eleve, 'notes': notes}
    return render(request, 'notes/detail_eleve.html', context)

def matieres(request):
    matieres = Matiere.objects.all()
    return render(request, 'notes/liste_matiere.html', {'matieres':matieres})

def matiere(request, matiere_id):
    matiere = get_object_or_404(Matiere, pk=matiere_id)
    notes = Note.objects.filter(matiere=matiere)  # Récupérer les notes dans cette matière
    niveau = matiere.niveau_set.all()
    #eleves = Eleve.objects.all() 



    # context = {
    #     'matiere': matiere,
    #     'notes': notes,
    #     #'eleves': eleves,
    # }
    return render(request, 'notes/detail_matiere.html', locals())

def niveau(request, niveau_id):
    niveau = get_object_or_404(Niveau, pk=niveau_id)
    eleves = Eleve.objects.filter(niveau=niveau)

    context ={
        'niveau':niveau,
        'eleves':eleves,
    }
    return render(request, 'notes/detail_niveau.html', context)