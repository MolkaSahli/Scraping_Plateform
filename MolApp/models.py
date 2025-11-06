from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Sites(models.Model):
    id = models.IntegerField(primary_key=True)
    Nom= models.CharField(max_length= 255)
    url= models.URLField(unique=True)
    description= models.TextField(blank=True)
    specialite= models.CharField(max_length=300, blank=True)
    Categories= models.TextField(blank=True)

    def __str__(self):
        return self.Nom 
    


class Projects(models.Model):

    STATUS_CHOICES = [
        ('Succès', 'Succès'),
        ('En Cours', 'En cours'),
        ('Échec', 'Échec'),
    ]

    option_choices=[
        ('Toutes', 'Toutes'),
        ('Actuelle', 'Actuelle'), 
        ('Personnaliser', 'Personnaliser'),
    ]

    id=models.AutoField(primary_key=True)
    url_site=models.URLField(unique=False)
    option=models.CharField(max_length=20, choices=option_choices, default='actuelle' )
    pages=models.CharField(default='', max_length=50, blank=True)
    nom_fichier=models.CharField(max_length =255)
    progress=models.IntegerField(default=0)
    Statut= models.CharField(max_length=12, choices=STATUS_CHOICES, default='En cours')
    date_debut=models.DateField(auto_now_add=True)
    data=models.JSONField(null=True, blank=True)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.nom_fichier
    