from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    column_name = models.CharField(max_length=200)
    task_text = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.PositiveSmallIntegerField(default=0, blank=True)

    class Meta:
        ordering = ["order", "-pk"]

    def __str__(self):
        return f"{self.user}'s board - {self.column_name} column - Task {self.pk}"
        
