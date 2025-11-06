from django.shortcuts import render, redirect, get_object_or_404
from .models import Sites 
from django.http import JsonResponse
from .models import Projects 
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import projectForm 
from .scrapers.ween import weenscrap
from .scrapers.avocats import avocat_scrap
from .scrapers.convert_to_excel import create_excel
from .scrapers.experts import experts_scrap
from .scrapers.comptables import comptab_scrap
from django.http import HttpResponse
import time 
import threading

@login_required(login_url='/login')
def index(request):
    return render(request, 'myapp/index.html')

@login_required(login_url='/login')
def projets(request):
    projet= Projects.objects.all()
    return render(request, 'myapp/projects.html', {'projet': projet})


@login_required(login_url='/login')
def liste(request):
    listes=Sites.objects.all()
    return render(request, 'myapp/tables.html',{'listes':listes})

#Login User
def login_page(request):
    page='login'
    if request.method=='POST':
        username= request.POST.get('username').lower()
        password= request.POST.get('password')

        try: 
            user= User.objects.get(username=username)
        except: 
            messages.error(request, "L'utilisateur n'existe pas.")
            return redirect('login')
        user = authenticate(request,username=username, password=password )

        if user is not None:  
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect. Veuillez les vérifier. ")
    context= {'page': page}
    return render( request, 'myapp/login.html', context)

#Logout User
@login_required(login_url='/login')
def logout_user(request):
    logout(request)
    return redirect('login')

#Register User
def register_user(request):
    page = 'register'
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            return redirect("login")
        else: 
            messages.error(request, 'Une erreur est survenue lors de la création du compte. Veuillez vérifier vos informations!')
    else:
        form = UserCreationForm()
    
    return render(request, 'myapp/login.html', {'form': form, 'page': page})



#Supprimer un Projet
@login_required(login_url='/login')
def delete_project(request, project_id):
    project=get_object_or_404(Projects, id=project_id)
    project.delete()
    return redirect('projets')

#Fonction pour le web scrapping
@login_required(login_url='/login')
def scrape_website(request):
    if request.method == 'POST':
        form = projectForm(request.POST)
        if form.is_valid():
            project = form.save()
            project.utilisateur = request.user

            return redirect('download_page', project_id=project.id)

    else:
        form = projectForm()

    return render(request, 'myapp/project_form.html', {'form': form})


def background_scraping(project_id):
    project = get_object_or_404(Projects, id=project_id)
    
    dic = None

    if "ween.tn" in project.url_site:
        dic = weenscrap(project.url_site, project.option, project.pages)
    elif "avocat.org.tn/annuaire" in project.url_site:
        dic = avocat_scrap(project.url_site, project.option, project.pages)
    elif "oect.org.tn/annuaire-des-membres-de-lordre-des-experts-comptables-de-tunisie" in project.url_site:
        dic = experts_scrap(project.url_site, project.option, project.pages)
    elif "cct.tn/annuaire" in project.url_site:
        dic = comptab_scrap(project.url_site, project.option, project.pages)

    if dic:
        project.Statut = 'Succès'
        project.progress= 100
        project.data = dic
        project.save()
    else:
        project.Statut = 'Échec'
        project.save()

# Démarrer le scraping en arrière-plan
def start_background_scraping(project_id):
    threading.Thread(target=background_scraping, args=(project_id,)).start()






#télécharger un fichier
@login_required(login_url='/login')
def download_excel(request, project_id):
    project = get_object_or_404(Projects, id=project_id)
    file_ready=False
    if project.data:
        file_ready=True
        response = create_excel(project.data, project.nom_fichier)
        return response
    else:
        return HttpResponse("Aucun fichier disponible.", content_type="text/plain")
    
@login_required(login_url='/login') 
def download_page(request, project_id):
    project = get_object_or_404(Projects, id=project_id)
    start_background_scraping(project.id)
    return render(request, 'myapp/download_project.html', {'project': project})