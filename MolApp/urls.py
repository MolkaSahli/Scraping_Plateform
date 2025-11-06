from  django.urls import path
from . import views




urlpatterns = [
    path('', views.index ,  name="index"),
    path('create_project/', views.scrape_website, name="étapes"),
    path("download/<int:project_id>", views.download_excel, name='download'),
    path("download_page/<int:project_id>", views.download_page, name='download_page'),
    path('projets/', views.projets, name="projets"),
    path('liste/', views.liste, name="liste"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('porjets/supprimer/<int:project_id>', views.delete_project, name='delete_project')
]