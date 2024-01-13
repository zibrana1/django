from audioop import avg
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
import os
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required


from notes.forms import NoteForm
from templating_ifnti.controleur import generate_pdf, generate_pdf2
from .models import *

# Create your views here.

def index(request):
    return render(request, "notes/index.html")
#@login_required
#@permission_required("Notes.view_eleve", raise_exception=True)
#@user_passes_test(lambda user: user.groups.filter(name='eleves').exists(), login_url='accounts/')
def eleves(request):
    eleves = Eleve.objects.all()
    return render(request, 'notes/liste_eleve.html', {'eleves':eleves})

def eleve(request, eleve_id):
    eleve = get_object_or_404(Eleve, pk=eleve_id)
    notes = Note.objects.filter(eleve=eleve)
    context ={'eleve': eleve, 'notes': notes}
    return render(request, 'notes/detail_eleve.html', context)

# @login_required
# @permission_required("Notes.view_matiere", raise_exception=True)
def matieres(request):
    matieres = Matiere.objects.all()
    return render(request, 'notes/liste_matiere.html', {'matieres':matieres})

def matiere(request, matiere_id):
    matiere = get_object_or_404(Matiere, pk=matiere_id)
    notes = Note.objects.filter(matiere=matiere)  # Récupérer les notes dans cette matière
    #niveau = matiere.niveau_set.all()
    eleves = Eleve.objects.all() 



    context = {
        'matiere': matiere,
        'notes': notes,
        'eleves': eleves,
    }
    return render(request, 'notes/detail_matiere.html',context)

def niveau(request, niveau_id):
    niveau = get_object_or_404(Niveau, pk=niveau_id)
    eleves = Eleve.objects.filter(niveau=niveau)

    context ={
        'niveau':niveau,
        'eleves':eleves,
    }
    return render(request, 'notes/detail_niveau.html', context)

# def add_note(request):
#     if request.method == 'POST':
#         eleve_id=request.POST.get("eleve")
#         matiere_id=request.POST.get("matiere")
#         note_value=request.POST.get("note")

#         note =Note.objects.create(valeur=note_value, eleve_id=eleve_id, matiere_id=matiere_id)
#         note.save()

        

#         return HttpResponse("Enregistrement avec succès")
    
#     #verification si l'élève suit la matière
#     else:
#         eleve_id=request.GET.get('eleve')
#         matiere_id=request.GET.get('matiere')

#         if eleve_id.matiere.get

        
# def add_note(request,pk_eleve,pk_matiere):from django.contrib.auth.decorators import login_required, user_passes_test

#      eleve = get_object_or_404(Eleve, id=pk_eleve)
#      matiere = get_object_or_404(Matiere, id=pk_matiere)
#      context = {"eleve":eleve,
#              "matiere":matiere}
#      if request.method == 'POST':from django.shortcuts import render, HttpResponse
from .models import Matiere, Note
from .forms import EleveForm, NoteForm

def add_notes(request, matiere_id):
    matiere = Matiere.objects.get(pk=matiere_id)
    eleves = Eleve.objects.filter(matieres_suivies=matiere)

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            for eleve in eleves:
                Note.objects.create(
                    eleve_id=eleve,
                    matiere_id=matiere,
                    valeur=form.cleaned_data['valeur']
                )
            return HttpResponse("Notes ajoutées avec succès.")
    else:
        form = NoteForm()
        return render(request, 'add_notes.html', {'form': form, 'matiere': matiere, 'eleves': eleves})

#          return render(
#              request,"notes/eleve_list.html",
#              context
#          )
#      else:
#          if eleve.matiere.filter(pk=pk_matiere).exists():
#              return render(
#                  request, 'notes/add_note.html',
#                  context=context
#              )
#          else:
#              raise Exception("L'élève ne suit pas cette matière.")

def add_note(request, id_eleve, matiere_id):
    eleve= get_object_or_404(Eleve, pk=id_eleve)
    matiere= get_object_or_404(Matiere, pk=matiere_id)

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            # Faites quelque chose avec le formulaire valide
            note = form.save(commit=False)
            note.eleve = eleve
            note.matiere=matiere
            note.save()

            return HttpResponse("Le note est bien enregistrer")
        return HttpResponse("La note non valide")
    else:
        form = NoteForm()
        return render(request, 'notes/add_note.html', {'eleve': eleve, 'matiere':matiere})
    

def add_notes(request, matiere_id):
        matiere= Matiere.objects.get(pk=matiere_id)
        eleves = Eleve.objects.filter(matiere=matiere)

        if request.method =='POST':
            form = NoteForm(request.POST)
            if form.is_valid():
                for eleve in eleves:
                    Note.objects.create(valeur=form.cleaned_data['valeur']
                                        ,eleve=eleve
                                        ,matiere=matiere)
                return HttpResponse("Notes ajoutés avec succès")
            
            return HttpResponse("notes non valide")
        
        else:
            form = NoteForm()
            return render(request, "notes/add_notes.html", {'form':form, 'matiere':matiere, 'eleves':eleves})


def acceuil(request):
    return render(request, "notes/acceuil.html")

def add_eleve(request):
    if request.method == "POST":
        form=EleveForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/eleves')
        
    else:
        form= EleveForm()
        return (request, 'notes/add_eleve.html', {'form':form})




def listEleves(request):
    # Récupérer la liste de tous les élèves depuis la base de données
    eleves = Eleve.objects.all()

    # Créer une liste de dictionnaires contenant les informations des élèves
    eleves_list = [{'matricule':eleve.id_eleve, 'nom': eleve.nom, 'prenom': eleve.prenom, 'sexe': eleve.sexe, 'dateNais':eleve.date_naissance}for eleve in eleves]

    context = {'eleves': eleves_list}
    generate_pdf(context)
    pdf_file_path = "out/liste_eleves.pdf"  

    # Vérifiez si le fichier PDF existe
    if os.path.exists(pdf_file_path):
        # Ouvrez le fichier PDF en mode binaire
        with open(pdf_file_path, 'rb') as pdf_file:
            # Créez une réponse HTTP avec le contenu du fichier PDF
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            # Ajoutez l'en-tête de disposition pour indiquer au navigateur de télécharger le fichier
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(pdf_file_path)
            return response
    else:
        # Si le fichier n'existe pas, renvoyez une réponse 404 (Not Found)
        return HttpResponse("Fichier PDF introuvable", status=404)


    
    
def niveauElv(request, niveau_id):
    #Récupérer la clé primaire du  niveau
    niveau = get_object_or_404(Niveau, pk=niveau_id)
    #récupérer la liste des élèves qui appartienent à ce niveau
    eleves = Eleve.objects.filter(niveau=niveau)
    # Créer une liste de dictionnaires contenant les informations des élèves
    eleves_list = [{'matricule':eleve.id_eleve, 'nom': eleve.nom, 'prenom': eleve.prenom, 'sexe': eleve.sexe, 'dateNais':eleve.date_naissance}for eleve in eleves]

    context = {"eleves":eleves_list}

    generate_pdf(context)

    pdf_file_path="out/liste_eleves.pdf"
    #vérifier si le fichier pdf existe
    if os.path.exists(pdf_file_path):
        with open(pdf_file_path, 'rb') as pdf_file:
            # Créez une réponse HTTP avec le contenu du fichier PDF
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            # Ajoutez l'en-tête de disposition pour indiquer au navigateur de télécharger le fichier
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(pdf_file_path)
            return response
    else:
        # Si le fichier n'existe pas, renvoyez une réponse 404 (Not Found)
        return HttpResponse("Fichier PDF introuvable", status=404)

def notesEleves(request, matiere_id):
    matiere = get_object_or_404(Matiere, pk=matiere_id)
    notes = Note.objects.filter(matiere=matiere)  # Récupérer les notes dans cette matière
    #niveau = matiere.niveau_set.all()
    eleves = Eleve.objects.all() 



    context = {
        'matiere': matiere,
        'notes': notes,
        'eleves': eleves,
    }
    matiere_list={'nom': matiere.nom}
    notes_list =[{'eleveNom': note.eleve.nom,'elevePrenom':note.eleve.prenom, 'valeur':note.valeur}for note in notes]

    context = {"notes": notes_list, "mat":matiere_list}

    generate_pdf2(context)

    pdf_file_path="out/notes_eleves.pdf"
    #vérifier si le fichier pdf existe
    if os.path.exists(pdf_file_path):
        with open(pdf_file_path, 'rb') as pdf_file:
            # Créez une réponse HTTP avec le contenu du fichier PDF
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            # Ajoutez l'en-tête de disposition pour indiquer au navigateur de télécharger le fichier
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(pdf_file_path)
            return response
    else:
        # Si le fichier n'existe pas, renvoyez une réponse 404 (Not Found)
        return HttpResponse("Fichier PDF introuvable", status=404)

def notesSynthese(request, eleve_id):
    eleve=get_object_or_404(Eleve, pk=eleve_id)
    print("eleve", eleve)
    matieres = eleve.niveau.matiere.all()
    

    for matiere in matieres :
        print("mat" ,matiere.nom)
        notes = matiere.note_set.all()
        moyenne = notes.aggretate(avg('valeur', default=0))['valeur__avg']
        response =HttpResponse(moyenne)
        return response