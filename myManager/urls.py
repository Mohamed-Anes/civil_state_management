from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home_page"),
    path('login', views.login_request, name="login"),
    path('logout', views.logout_request, name="logout"),
    path('ajout/naissance', views.naissance, name="naissance"),
    path('ajout/mariage', views.mariage, name="mariage"),
    path('ajout/deces', views.deces, name="deces"),
    path('rech/naissance', views.recherche_acte_naissance, name="rech_acte_naissance"),
    path('rech/deces', views.recherche_acte_deces, name="rech_acte_deces"),
    path('rech/mariage', views.recherche_acte_mariage, name="rech_acte_mariage"),
    path('acte/naissance', views.impr_acte_naissance, name="acte_naissance"),
    path('acte/deces', views.impr_acte_deces, name="acte_deces"),
    path('acte/mariage', views.impr_acte_mariage, name="acte_mariage")
]