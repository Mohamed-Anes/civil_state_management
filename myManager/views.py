from django.shortcuts import render, redirect

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from datetime import date
import datetime
from django.contrib.auth.models import User

from .models import Citoyen, Marriage, Temoin, Naissanse, Deces, Officier, BeureuEtatciv, Commune, Daira, Willaya, Pays, Registre_naissance, Registre_marriage, Registre_deces

from .forms import forme_naissance, forme_deces, forme_mariage, recherche_forme
# Create your views here.

def home(request):
    mssg = ""
    if Officier.objects.all().count() == 0:
        user = User.objects.create_user(username='user', password='user')
        offic = Officier(nom='user', prenom='user', system_user=user)
        offic.save()
        mssg = "Il n'y a pas d'officiers maintenent donc un officier a été crée avec le username : 'user' et le password : 'user', il peut acceder au ce site mais pas au paneau admin"

    nb_naiss = Naissanse.objects.all().count()
    nb_deces = Deces.objects.all().count()

    temp_date = datetime.date.today()
    temp_date2 = date(temp_date.year - 18, temp_date.month, temp_date.day)

    temp_naiss = list(Naissanse.objects.filter(dateNaiss__lte=temp_date2))
    temp_list = []
    for t in temp_naiss:
        temp_list.append(t.NumAct)

    cit_pls_18 = Citoyen.objects.exclude(etatVie=False)

    nb = 0
    for c in cit_pls_18:
        if c.pk in temp_list:
            nb += 1

    
    if request.user.is_authenticated:
        return render(request, "base_officier.html", {'nb_naiss' : nb_naiss, 'nb_deces' : nb_deces, 'nb_cit_mjr' : nb})
    else:    
        return render(request, "base.html", {'mssg' : mssg})

def logout_request(request):
    logout(request)
    return redirect('home_page')

def login_request(request):
    mssg = ""
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                try:
                    officier = Officier.objects.get(system_user=user)
                    if officier is not None:
                        login(request, user)
                        mssg =  f"You are now logged in as {username}."
                        return redirect("home_page")
                except:
                    mssg = "Invalid username or password."
            else:
                mssg = "Invalid username or password."
        else:
            mssg = "Invalid username or password."
    
    form = AuthenticationForm()
    return render(request, "login.html", {'login_form': form, "mssg" : mssg})

@login_required
def naissance(request):
    mssg = ""
    if request.method == 'POST':
        form = forme_naissance(request.POST)
        if form.is_valid():
            offic = Officier.objects.get(system_user=request.user)
            citoyen = Citoyen(nom=form.cleaned_data['nom'], prenom=form.cleaned_data['prenom'],
                                sexe = form.cleaned_data['sexe'], etatVie=True)
            citoyen.adr = form.cleaned_data['adresse']
            citoyen.NumPere = Citoyen.objects.get(NumNat=form.cleaned_data['numNatPere'])              
            citoyen.NumMere = Citoyen.objects.get(NumNat=form.cleaned_data['numNatMere'])
            # citoyen.comResid = form.cleaned_data['numComDec']
            try:
                if offic.NumB.NimCom is not None:
                    citoyen.comResid=offic.NumB.NimCom
            except:
                NotImplemented

            acte_naissance = Naissanse(dateDeclaration=datetime.date.today(), dateNaiss=form.cleaned_data['dateNaiss'], NumNatCon=citoyen.NumNat)
            # if form.cleaned_data['mat_officier'] is not None:
            #     acte_naissance.matOffic=form.cleaned_data['mat_officier']
            acte_naissance.matOffic=offic
            if form.cleaned_data['numNatDec'] is not None:
                acte_naissance.NumNatD=Citoyen.objects.get(NumNat=form.cleaned_data['numNatDec'])
            if citoyen is not None:
                acte_naissance.NumNatCon=citoyen
            # if form.cleaned_data['numComDec'] is not None:
            #     acte_naissance.NumComDec=form.cleaned_data['numComDec']
            try:
                if acte_naissance.matOffic.NumB.NimCom is not None:
                    acte_naissance.NumComDec=acte_naissance.matOffic.NumB.NimCom
            except:
                NotImplemented
            if form.cleaned_data['numComNaiss'] is not None:
                acte_naissance.NumComNaiss=Commune.objects.get(NumC=form.cleaned_data['numComNaiss'])
            try:
                if Registre_naissance.objects.get(annee=int(date.today().year)) is not None:
                    acte_naissance.registre=Registre_naissance.objects.get(annee=int(date.today().year))
            except:
                NotImplemented
            if citoyen is not None and acte_naissance is not None:
                citoyen.save()
                acte_naissance.save()
                citoyen.NumactNaiss = acte_naissance
                citoyen.save()
                mssg = "Naissance enregistrée"
                form = forme_naissance()
            else:
                mssg = "erreur dans les donnees entrées"
        else:
            mssg = "erreur dans les donnees entrées"
    else:
        form = forme_naissance()
    return render(request, "ajout/naissance.html", {'form' : form, 'mssg': mssg})

@login_required
def mariage(request):
    mssg = ""
    if request.method == 'POST':
        form = forme_mariage(request.POST)
        if form.is_valid():
            offic = Officier.objects.get(system_user=request.user)
            # marie = Citoyen.objects.get(NumNat=form.cleaned_data['numNatMari'])
            mar = Marriage(NumMare=Citoyen.objects.get(NumNat=form.cleaned_data['numNatMari']),
                            NumEpouse=Citoyen.objects.get(NumNat=form.cleaned_data['numNatEpouse']))

            # if form.cleaned_data['matOfficier'] is not None:
            #     mar.matOffic = form.cleaned_data['matOfficier']
            mar.matOffic = offic
            # if form.cleaned_data['commune'] is not None:
            #     mar.NumCom = form.cleaned_data['commune']
            try:
                if offic.NumB.NimCom is not None:
                    mar.NumCom = offic.NumB.NimCom
            except:
                NotImplemented
            if form.cleaned_data['domicile'] is not None:
                mar.domicile = form.cleaned_data['domicile']
            if form.cleaned_data['existeContrat'] is not None:
                mar.existContrat = form.cleaned_data['existeContrat']
            # if form.cleaned_data['date'] is not None:
            #     mar.dateM = form.cleaned_data['date']
            mar.dateM = datetime.datetime.today()
            mar.etat = "marrié"
            try:
                if Registre_marriage.objects.get(annee=int(date.today().year)) is not None:
                    mar.registre = Registre_marriage.objects.get(annee=int(date.today().year))
            except:
                NotImplemented
            if deces is not None:
                cit = Citoyen.objects.get(NumNat=mar.NumMare.NumNat)
                cit.etatMaritime = "mariée"
                cit.save()
                cit = Citoyen.objects.get(NumNat=mar.NumEpouse.NumNat)
                cit.etatMaritime = "mariée"
                cit.save()
                mar.save()
                mssg = "Marriage enregistrée"
            else:
                mssg = "erreur dans les donnees entrées"
        else:
            mssg = "erreur dans les donnees entrées"

    else:
        form = forme_mariage()
    return render(request, "ajout/mariage.html", {'form' : form, 'mssg' : mssg})

@login_required
def deces(request):
    mssg = ""
    if request.method == 'POST':
        form = forme_deces(request.POST)
        if form.is_valid():
            offic = Officier.objects.get(system_user=request.user)

            deces = Deces(NumNatCon=Citoyen.objects.get(NumNat=form.cleaned_data['numNatConcerne']))
            if form.cleaned_data['dateDeces'] is not None:
                deces.date = form.cleaned_data['dateDeces']
            if form.cleaned_data['heurDeces'] is not None:
                deces.hour = form.cleaned_data['heurDeces']
            if form.cleaned_data['raison'] is not None:
                deces.reson = form.cleaned_data['raison']
            
            deces.matOffic = offic
            
            if form.cleaned_data['numNatMedecin'] is not None:
                deces.NumNatMedecin = Citoyen.objects.get(NumNat=form.cleaned_data['numNatMedecin'])
            if form.cleaned_data['numNatDec'] is not None:
                deces.NumNatDec = Citoyen.objects.get(NumNat=form.cleaned_data['numNatDec'])
            # if form.cleaned_data['commune'] is not None:
            #     deces.NumComDeces = form.cleaned_data['commune']
            try:
                if offic.NumB.NimCom is not None:
                    deces.NumComDeces = offic.NumB.NimCom
            except:
                NotImplemented
            try:
                if Registre_deces.objects.get(annee=int(date.today().year)) is not None:
                    deces.registre = Registre_deces.objects.get(annee=int(date.today().year))
            except:
                NotImplemented
            if deces is not None:
                cit = Citoyen.objects.get(NumNat=deces.NumNatCon.NumNat)
                cit.etatVie = False
                cit.save()
                deces.save()
                mssg = "Deces enregistrée"
            else:
                mssg = "erreur dans les donnees entrées"
        else:
            mssg = "erreur dans les donnees entrées"

    else:
        form = forme_deces()
    return render(request, "ajout/deces.html", {'form' : form, 'mssg' : mssg})


@login_required
def recherche_acte_naissance(request):
    title = "Acte de Naissance"
    message1 = "Recherche d'Acte de Naissance"
    message2 = ""

    if request.method == 'GET':
        form = recherche_forme(request.GET)
        if form.is_valid():
            try:
                acte = Naissanse.objects.get(NumAct=request.GET['numero'])
                if acte is not None:
                    url = redirect('acte_naissance')
                    url['Location'] += '?numero='
                    url['Location'] += str(acte.NumAct)
                    return url
            except:
                message2 = "numero invalide"
        else:
            message2 = "numero invalide"
    
    form = recherche_forme()
    list_naiss = Naissanse.objects.all()
    return render(request, "entree_numero.html", {'form' : form, 'title' : title, 'message1' : message1, 'message2' : message2, 'list_naiss' : list_naiss})

@login_required
def impr_acte_naissance(request):
    if request.method == 'GET':
        naiss = Naissanse.objects.get(NumAct=request.GET['numero'])
        
        return render(request, "actes/naissance.html", {'naiss' : naiss})
    
    return render(request, "actes/naissance.html")

@login_required
def recherche_acte_mariage(request):
    title = "Acte de Mariage"
    message1 = "Recherche d'Acte de Mariage"
    message2 = ""

    if request.method == 'GET':
        form = recherche_forme(request.GET)
        if form.is_valid():
            try:
                acte = Marriage.objects.get(NumAct=request.GET['numero'])
                if acte is not None:
                    url = redirect('acte_mariage')
                    url['Location'] += '?numero='
                    url['Location'] += str(acte.NumAct)
                    temoins = Temoin.objects.filter(NumActMarr=acte)
                    i = 1
                    for t in temoins:
                        url['Location'] += f'&t{i}='
                        url['Location'] += str(t.NumTemoin)
                        i += 1
                    return url
            except:
                message2 = "numero invalide"
        else:
            message2 = "numero invalide"
    
    form = recherche_forme()
    list_mariage = Marriage.objects.all()
    return render(request, "entree_numero.html", {'form' : form, 'title' : title, 'message1' : message1, 'message2' : message2, 'list_mariage' : list_mariage})

@login_required
def impr_acte_mariage(request):
    if request.method == 'GET':
        mar = Marriage.objects.get(NumAct=request.GET['numero'])
        contexte = {'mar': mar}
        try:
            t1 = Temoin.objects.get(NumTemoin=request.GET['t1'])
            print('1')
            contexte.update({'t1' : t1})
        except:
            NotImplemented
        try:
            t2 = Temoin.objects.get(NumTemoin=request.GET['t2'])
            print('2')
            contexte.update({'t2' : t2})
        except:
            NotImplemented
        try:
            t3 = Temoin.objects.get(NumTemoin=request.GET['t3'])
            contexte.update({'t3' : t3})
        except:
            NotImplemented
        
        return render(request, "actes/mariage.html", contexte)
    
    return render(request, "actes/mariage.html")

@login_required
def recherche_acte_deces(request):
    title = "Acte de Deces"
    message1 = "Recherche d'Acte de Deces"
    message2 = ""

    if request.method == 'GET':
        form = recherche_forme(request.GET)
        if form.is_valid():
            try:
                acte = Deces.objects.get(NumAct=request.GET['numero'])
                if acte is not None:
                    url = redirect('acte_deces')
                    url['Location'] += '?numero='
                    url['Location'] += str(acte.NumAct)
                    return url
            except:
                message2 = "numero invalide"
        else:
            message2 = "numero invalide"
    
    form = recherche_forme()
    list_deces = Deces.objects.all()
    return render(request, "entree_numero.html", {'form' : form, 'title' : title, 'message1' : message1, 'message2' : message2, 'list_deces' : list_deces})

@login_required
def impr_acte_deces(request):
    if request.method == 'GET':
        dec = Deces.objects.get(NumAct=request.GET['numero'])
        
        return render(request, "actes/deces.html", {'dec' : dec})
    
    return render(request, "actes/deces.html")



