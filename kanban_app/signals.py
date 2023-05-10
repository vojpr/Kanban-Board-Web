from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Task
 
 
@receiver(post_save, sender=User)
def create_default_tasks(instance, created, **kwargs):
    if created:
        Task.objects.create(user=instance, column_name="To-do", task_text="Drag and drop tasks to sort them...")
        Task.objects.create(user=instance, column_name="To-do", task_text="Use the text box above to add new tasks")
        Task.objects.create(user=instance, column_name="In progress", task_text="...or to move them between columns")
        Task.objects.create(user=instance, column_name="Done", task_text="Delete a task by pressing the ✕")
