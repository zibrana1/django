from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.

class Personne(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    sexe = models.CharField(choices=[("M", "Masculin"),("F","Féminin")],  max_length=50)
    date_naissance = models.DateField()
    user =models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "Nom :" + self.nom + ", Prenom : "+ self.prenom + ", Sexe :"+ self.sexe +", Date de naissance : " +str(self.date_naissance)
    

    class Meta:
         abstract = True



class Enseignant(Personne):
    pass

    class Meta:
        verbose_name_plural = "Enseignants"

class Matiere(models.Model):
    nom = models.CharField(max_length=50, unique=True)
    enseignant= models.ForeignKey(Enseignant, on_delete=models.CASCADE)
    

    class Meta:
        verbose_name_plural = "Matières"

    def __str__(self):
        return "Nom de la matière :" + self.nom + ", Professeur :" +self.enseignant.nom + "<br>"
    

class Niveau(models.Model):
    nom = models.CharField(max_length=2 , unique=True)
    matiere = models.ManyToManyField(Matiere)

    class Meta:
        verbose_name_plural = "Niveaux"

    def __str__(self):
        return self.nom 
    



class Eleve(Personne):
    id_eleve = models.CharField(primary_key=True, max_length=20)
    #matiere = models.ManyToManyField(Matiere)
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "Elèves"


    def save(self, *args, **kwargs):
        # Générer le matricule lors de l'enregistrement
        deux_lettres_nom = self.nom[:2].upper()
        deux_lettres_prenom = self.prenom[:2].upper()
        heure_enregistrement = datetime.now().strftime("%H%M%S")
        
        # Concaténer les parties pour former le matricule
        self.id_eleve = f"{deux_lettres_nom}{deux_lettres_prenom}{heure_enregistrement}"
        print(self.id_eleve)
        super().save(*args, **kwargs)  # Appeler la méthode save de la classe parente


    def __str__(self):
        return super().__str__() + ", Niveau : " + self.niveau.nom +"<br>"

    

    
class Note(models.Model):
    valeur = models.FloatField(null=True, validators=[MinValueValidator(0), MaxValueValidator(20)])
    eleve =models.ForeignKey(Eleve, on_delete=models.CASCADE)
    matiere= models.ForeignKey(Matiere, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Notes"

    def __str__(self):
        return  "Nom Elève : "+self.eleve.nom  +", Matière "+self.matiere.nom + ", Notes :" +str(self.valeur)
    

