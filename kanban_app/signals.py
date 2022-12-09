from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Column, Task
 
 
@receiver(post_save, sender=User)
def create_board(sender, instance, created, **kwargs):
    if created:
        to_do_column = Column.objects.create(user=instance, column_name="To-do")
        to_do_column.save()
        in_progress_column = Column.objects.create(user=instance, column_name="In progress")
        in_progress_column.save()
        done_column = Column.objects.create(user=instance, column_name="Done")
        done_column.save()
        task_1 = Task.objects.create(parent_column=to_do_column, task_text="Use the text box above to add a new task")
        task_1.save()
        task_2 = Task.objects.create(parent_column=to_do_column, task_text="To move a task up, press the up arrow")
        task_2.save()
        task_3 = Task.objects.create(parent_column=in_progress_column, task_text="Press the left or right arrow to move a task between columns")
        task_3.save()
        task_4 = Task.objects.create(parent_column=done_column, task_text="Delete a task by pressing the ✕")
        task_4.save()
