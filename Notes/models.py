from django.db import models

# Create your models here.

class Personne(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    sexe = models.CharField(choices=[("M", "Masculin"),("F","Féminin")],  max_length=50)
    date_naissance = models.DateField()

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
    id_eleve = models.IntegerField(primary_key=True)
    #matiere = models.ManyToManyField(Matiere)
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Elèves"

    def __str__(self):
        return super().__str__() + ", Niveau : " + self.niveau.nom +"<br>"

    

    
class Note(models.Model):
    valeur = models.FloatField(null=True)
    eleve =models.ForeignKey(Eleve, on_delete=models.CASCADE)
    matiere= models.ForeignKey(Matiere, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Notes"

    def __str__(self):
        return  "Nom Elève : "+self.eleve.nom  +", Matière "+self.matiere.nom + ", Notes :" +str(self.valeur)
    

