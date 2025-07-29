from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.


class Citoyen (models.Model):
    NumNat = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=20)
    prenom = models.CharField(max_length=20)
    sexe = models.CharField(max_length=5)
    adr =  models.CharField(max_length=30, null=True)
    proficion =models.CharField(max_length=20, null=True)
    etatVie = models.BooleanField()
    etatMaritime =models.CharField(max_length=20)
    NumPere = models.ForeignKey('Citoyen', on_delete=models.SET_NULL, null=True, blank=True)
    NumMere = models.ForeignKey('Citoyen', on_delete=models.CASCADE ,related_name="NumMereC",null=True, blank=True)
    NumResponssable=models.ForeignKey('Citoyen',on_delete=models.SET_NULL,null=True, blank=True,related_name="NumResponssableC" )
    NumactNaiss=models.OneToOneField('Naissanse',on_delete=models.CASCADE,null=True, blank=True)
    comResid=models.ForeignKey('Commune',on_delete=models.SET_NULL,null=True, blank=True)

    def __str__(self):
        return self.nom
   
class Marriage(models.Model):
    NumAct=models.AutoField(primary_key=True)
    dateM=models.DateTimeField(null=True)
    etat=models.CharField(max_length=50)
    domicile=models.CharField(max_length=50, null=True)
    existContrat=models.BooleanField()
    NumMare=models.ForeignKey('Citoyen',on_delete=models.CASCADE ,related_name="NumMare")
    NumEpouse=models.ForeignKey('Citoyen',on_delete=models.CASCADE,related_name="NumEpouse")
    matOffic=models.ForeignKey('Officier',on_delete=models.CASCADE, null=True)
    NumCom=models.ForeignKey('Commune',on_delete=models.SET_NULL,null=True, blank=True)
    registre=models.ForeignKey("Registre_marriage", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.NumAct)
    
class Temoin(models.Model):
    NumTemoin=models.AutoField(primary_key=True)
    NumNat=models.ForeignKey('Citoyen',on_delete=models.CASCADE)
    NumActMarr=models.ForeignKey('Marriage',on_delete=models.CASCADE)

    def __str__(self):
        return str(self.NumTemoin)

class Naissanse(models.Model):
    NumAct=models.AutoField(primary_key=True)
    dateDeclaration=models.DateTimeField(auto_now=True)
    dateNaiss=models.DateField()
    matOffic=models.ForeignKey('Officier', on_delete=models.CASCADE, null=True)
    NumNatD=models.ForeignKey('Citoyen',   on_delete=models.CASCADE,related_name="NumNatD", null=True)
    NumNatCon=models.OneToOneField('Citoyen', on_delete=models.CASCADE,related_name="NumNatConM", null=True)
    NumComDec=models.ForeignKey('Commune', on_delete=models.CASCADE,related_name="NumComDec", null=True)
    NumComNaiss=models.ForeignKey('Commune',on_delete=models.SET_NULL,related_name="NumComNaiss",null=True, blank=True)
    registre=models.ForeignKey("Registre_naissance", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.NumAct)


class Deces(models.Model):
    NumAct=models.AutoField(primary_key=True)
    date=models.DateField(null=True)
    hour=models.DecimalField(max_digits=2,decimal_places=2, null=True)
    reson=models.CharField(max_length=150, null=True)
    matOffic=models.ForeignKey('Officier',on_delete=models.SET_NULL, null=True)
    NumNatMedecin=models.ForeignKey('Citoyen',on_delete=models.CASCADE,related_name="NumNatMedecin", null=True)
    NumNatCon=models.OneToOneField('Citoyen',on_delete=models.CASCADE,related_name="NumNatCon")
    NumNatDec=models.ForeignKey('Citoyen',on_delete=models.CASCADE,related_name="NumNatDec", null=True)
    NumComDeces=models.ForeignKey('Commune',on_delete=models.SET_NULL, null=True, blank=True)
    registre=models.ForeignKey("Registre_deces", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.NumAct)


class Officier(models.Model):
    matoffic=models.AutoField(primary_key=True)
    nom= models.CharField(max_length=50)
    prenom= models.CharField(max_length=50)
    datePrisService=models.DateField(null=True)
    emploi=models.CharField(max_length=50)
    NumB=models.ForeignKey('BeureuEtatciv',on_delete=models.CASCADE, null=True, blank=True)
    system_user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.nom

class BeureuEtatciv(models.Model):
    NumB=models.AutoField(primary_key=True)
    MatM=models.ForeignKey('Officier',on_delete=models.SET_NULL, null=True,related_name="MatM")
    MatT=models.ForeignKey('Officier',on_delete=models.SET_NULL, null=True,related_name="MatT")
    NimCom=models.ForeignKey('Commune',on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.NumB)

class Commune(models.Model):
    NumC=models.AutoField(primary_key=True)
    nomC=models.CharField(max_length=50)
    NumD=models.ForeignKey('Daira',on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.nomC

class Daira(models.Model):
     NumD=models.AutoField(primary_key=True)
     nomD=models.CharField(max_length=50)
     NumW=models.ForeignKey('Willaya',on_delete=models.SET_NULL, null=True)

     def __str__(self):
        return self.nomD

class Willaya(models.Model):
    NumW=models.AutoField(primary_key=True)
    nomW=models.CharField(max_length=50)
    nomP=models.ForeignKey('Pays',on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nomW  

class Pays(models.Model):
    nomP=models.CharField(primary_key=True, max_length=50)

    def __str__(self):
        return self.nomP

class Registre_naissance(models.Model):
    annee=models.IntegerField(primary_key=True)
    commune=models.ForeignKey('Commune', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.annee)

class Registre_marriage(models.Model):
    annee=models.IntegerField(primary_key=True)
    commune=models.ForeignKey('Commune', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.annee)

class Registre_deces(models.Model):
    annee=models.IntegerField(primary_key=True)
    commune=models.ForeignKey('Commune', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.annee)
