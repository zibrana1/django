from django import forms
from .models import *

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['valeur']
        labels = {'valeur': 'Note sur 20'}

class EleveForm(forms.ModelForm):
    class Meta:
        model=Eleve
        fields= '__all__'

class EnseignantForm(forms.ModelForm):
    class Meta:
        model = Enseignant
        fields = '__all__'

class MatiereForm(forms.ModelForm):
    class Meta:
        model = Matiere
        fields = '__all__'

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = '__all__'
    # def clean_nom(self):
    #     nom = self.cleaned_data.get('nom')
    #     if any(char.isdigit() for char in nom):
    #         raise forms.ValidationError("Le nom ne doit pas contenir de chiffres.")
    #     return nom
    
    # def clean_prenom(self):
    #     prenom=self.cleaned_data.get('prenom')
    #     if any(char.isdigit() for char in prenom):
    #         raise forms.ValidationError('Le champs prenom ne doit pas contenir de chiffres')

# class FormulaireSave(forms.Form):
#     nom = forms.CharField(max_length=15, widget=50)
#     prenom = forms.CharField(widget=50)