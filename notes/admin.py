from django.contrib import admin
from .models import *
from .forms import EleveForm, EnseignantForm, MatiereForm
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.


class EleveResource(resources.ModelResource):
    class Meta:
        model = Eleve
        #fields =('id_eleve','nom', 'prenom', 'sexe', 'date_naissance')


class EnseignantResource(resources.ModelResource):
    class Meta:
        model = Enseignant
        fields = ('id','nom', 'prenom', 'sexe', 'date_naissace')

class MatiereResource(resources.ModelResource):
    class Meta:
        model = Matiere
        fields  = ('nom', 'enseignant')

class EleveAdmin(ImportExportModelAdmin):
    form = EleveForm
    list_display = ('id_eleve','nom', 'prenom', 'sexe','date_naissance')
    list_filter = ('niveau',)
    search_fields = ('nom', 'prenom')
    resource_classes =[EleveResource]


class EnseignantAdmin(ImportExportModelAdmin):
    form = EnseignantForm 
    list_display = ('id', 'nom', 'prenom', 'sexe', 'date_naissance')
    search_fields =('nom', 'prenom')
    resource_classes =[EnseignantResource]

class MatiereAdmin(ImportExportModelAdmin):
    form  = MatiereForm
    list_display = ('nom', 'enseignant')
    resource_classes = [MatiereResource]
    

#personnes = Eleve.objects.all()

# for personne in personnes:
#     username = f"{personne.prenom[0].lower()}{personne.nom.lower()}"
#     user = User.objects.create_user(username=username, password='ifnti2023')
#     personne.user = user
#     personne.save()

# enseignants = Enseignant.objects.all()

# for enseignant in enseignants:
#     username = f"{enseignant.prenom[0].lower()}{enseignant.nom.lower()}"
#     user = User.objects.create_user(username=username, password='ifnti2023')
#     enseignant.user = user
#     enseignant.save() 


admin.site.register(Niveau)
admin.site.register(Enseignant, EnseignantAdmin)
admin.site.register(Matiere, MatiereAdmin)
admin.site.register(Note)
admin.site.register(Eleve, EleveAdmin)


