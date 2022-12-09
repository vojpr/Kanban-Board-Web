from django.contrib import admin
from .models import Column, Task

myModels = [Column, Task]
admin.site.register(myModels)