from django.contrib import admin

# Register your models here.
from .models import Sites 
admin.site.register(Sites)


from .models import Projects
admin.site.register(Projects)