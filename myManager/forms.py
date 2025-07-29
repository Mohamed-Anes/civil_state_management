from django.db.models import fields
from django import forms
from . import models


class forme_naissance(forms.Form):
    nom = forms.CharField(max_length=20)
    prenom = forms.CharField(max_length=20)
    sexe = forms.ChoiceField(choices=(('Homme', 'Homme'), ('Femme', 'Femme')))
    # mat_officier = forms.IntegerField(required=False)  # to remove
    numComNaiss = forms.IntegerField(required=False, label='Comunauté de naissance')
    # numComDec = forms.IntegerField(required=False)  # to remove
    numNatDec = forms.IntegerField(required=False, label='Numero nationale de declarant')
    numNatPere = forms.IntegerField(required=False, label='Numero nationale de pere')
    numNatMere = forms.IntegerField(required=False, label='Numero nationale de mere')
    adresse = forms.CharField(max_length=200, required=False, label='Adresse de naissance')
    dateNaiss = forms.DateField(required=False, label='Date de naissance')
    # dateDec = forms.DateField(required=False, label='Date de declaration')  # to remove


class forme_deces(forms.Form):
    numNatConcerne = forms.IntegerField(label='Numero nationale de décédé')
    numNatDec = forms.IntegerField(required=False, label='Numero nationale de declarant')
    numNatMedecin = forms.IntegerField(required=False, label='Numero nationale de medecin legiste')
    # commune = forms.IntegerField(required=False, label='Numero de Commune')  # to be removed
    raison = forms.CharField(max_length=200, required=False, label='Raison de décès')
    heurDeces = forms.DecimalField(max_digits=2,decimal_places=2, required=False, label='Heur de décès')
    dateDeces = forms.DateField(required=False, label='Date de décès')


class forme_mariage(forms.Form):
    numNatMari = forms.IntegerField(label='Numero nationale de marie')
    numNatEpouse = forms.IntegerField(label="Numero nationale d'epouse")
    numNatTem1 = forms.IntegerField(required=False, label='Numero nationale de temoin 1')
    numNatTem2 = forms.IntegerField(required=False, label='Numero nationale de temoin 2')
    numNatTem3 = forms.IntegerField(required=False, label='Numero nationale de temoin 3')
    # matOfficier = forms.IntegerField(required=False, label="Matricule d'officier")  # to be removed
    # commune = forms.IntegerField(required=False, label="Numero de commune")  # to be removed
    domicile = forms.CharField(max_length=200, required=False, label='Adresse de domicile')
    existeContrat = forms.BooleanField(required=False, label="Est ce qu'il existe un contrat")
    # date = forms.DateField(required=False, label='Date de mariage')  # to be removed


class recherche_forme(forms.Form):
    numero = forms.IntegerField(label="Numero d'acte")

