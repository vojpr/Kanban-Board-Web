from django.db import models
from django.contrib.auth.models import User


class Column(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    column_name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.user}'s board - {self.column_name} column"


class Task(models.Model):
    parent_column = models.ForeignKey(Column, on_delete=models.CASCADE)
    task_text = models.CharField(max_length=200)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.parent_column.user}'s board - {self.parent_column.column_name} column - Task {self.pk}"
