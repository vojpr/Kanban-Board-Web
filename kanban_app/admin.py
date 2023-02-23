from django.contrib import admin
from .models import Task

myModels = [Task]
admin.site.register(myModels)