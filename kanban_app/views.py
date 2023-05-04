from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, View
from .forms import SignUpForm, LoginForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task
from django.http import JsonResponse
import json


def index_page(request):
    signup_form = SignUpForm()
    login_form = LoginForm()
    if request.method == "POST":
        if request.POST.get("submit") == "signup_form":
            signup_form = SignUpForm(request.POST)
            if signup_form.is_valid():
                login(request, signup_form.save())
                return redirect('board')
        if request.POST.get("submit") == "login_form":
            login_form = LoginForm(request, request.POST)
            if login_form.is_valid():
                login(request, login_form.get_user())
                return redirect('board')
    context = {
        'signup_form': signup_form,
        'login_form': login_form,
    }
    return render(request, 'index.html', context)


class Board(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'kanban_app/board.html'
    context_object_name = "tasks"
    login_url = '/'

    def get_queryset(self):
        queryset = super(LoginRequiredMixin, self).get_queryset()
        return queryset.filter(user=self.request.user)


class CreateTask(LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request):
        new_task_text = request.GET.get("new-task", None)
        new_task = Task.objects.create(user=self.request.user, column_name="To-do", task_text=new_task_text)
        new_task_data = {
            "text": new_task.task_text, "pk": new_task.pk
        }
        data = {
            "task": new_task_data
        }
        return JsonResponse(data)
    

class DeleteTask(LoginRequiredMixin, View):
    login_url = '/'

    def  get(self, request):
        pk = request.GET.get('pk', None)
        Task.objects.get(pk=pk).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)
    

class ReorderTask(LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request):
        tasks = json.loads(request.GET.get('sort'))
        for task in tasks:
            task_obj = get_object_or_404(Task, pk=int(task['pk']))
            task_obj.order = task['order']
            task_obj.column_name = task['column_name']
            task_obj.save()
        data = {
            'reordered': True
        }
        return JsonResponse(data)
