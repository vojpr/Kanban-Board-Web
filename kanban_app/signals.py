from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Task
 
 
@receiver(post_save, sender=User)
def create_board(instance, created, **kwargs):
    if created:
        task_1 = Task.objects.create(user=instance, column_name="To-do", task_text="Drag and drop tasks to sort them...")
        task_1.save()
        task_2 = Task.objects.create(user=instance, column_name="To-do", task_text="Use the text box above to add new tasks")
        task_2.save()
        task_3 = Task.objects.create(user=instance, column_name="In progress", task_text="...or to move them between columns")
        task_3.save()
        task_4 = Task.objects.create(user=instance, column_name="Done", task_text="Delete a task by pressing the ✕")
        task_4.save()
