from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import SignUpForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import Column
from .models import Column, Task
import datetime


def index_page_view(request):
    signup_form = SignUpForm()
    error_message = False
    if request.method == "POST":
        if request.POST.get("submit") == "signup_form":
            signup_form = SignUpForm(request.POST)
            if signup_form.is_valid():
                signup_form.save()
                signup_name = signup_form.cleaned_data['username']
                signup_pass = signup_form.cleaned_data['password1']
                user = authenticate(
                    request, username=signup_name, password=signup_pass)
                login(request, user)
                return redirect('board')
        if request.POST.get("submit") == "login_form":
            login_name = request.POST["login_name"]
            login_pass = request.POST["login_pass"]
            print(login_name)
            user = authenticate(
                request, username=login_name, password=login_pass)
            if user is not None:
                login(request, user)
                return redirect('board')
            else:
                error_message = True
    context = {
        'signup_form': signup_form,
        'login_error': error_message
    }
    return render(request, 'index.html', context)


@login_required(login_url='/')
def board_view(request):
    columns = Column.objects.filter(user=request.user).all()
    to_do_tasks = Task.objects.filter(
        parent_column=columns[0]).order_by('time_stamp').all()
    in_progress_tasks = Task.objects.filter(
        parent_column=columns[1]).order_by('time_stamp').all()
    done_tasks = Task.objects.filter(
        parent_column=columns[2]).order_by('time_stamp').all()
    context = {
        "to_do_tasks": to_do_tasks,
        "in_progress_tasks": in_progress_tasks,
        "done_tasks": done_tasks,
    }
    return render(request, 'kanban_app/board.html', context)


@login_required
def add_task(request):
    columns = Column.objects.filter(user=request.user).all()
    new_task = Task(parent_column=columns[0],
                    task_text=request.POST["new-task"])
    new_task.save()
    return redirect(reverse('board'))


@login_required
def move_up(request, task_pk, previous_task_pk):
    lower_task = Task.objects.get(pk=task_pk)
    lower_task_time_stamp = lower_task.time_stamp
    upper_task = Task.objects.get(pk=previous_task_pk)
    upper_task_time_stamp = upper_task.time_stamp
    lower_task.time_stamp = upper_task_time_stamp
    lower_task.save()
    upper_task.time_stamp = lower_task_time_stamp
    upper_task.save()
    return redirect(reverse('board'))


@login_required
def move_left(request, task_pk):
    task_to_move = Task.objects.get(pk=task_pk)
    new_column = Column.objects.get(pk=task_to_move.parent_column.pk - 1)
    task_to_move.parent_column = new_column
    task_to_move.time_stamp = datetime.datetime.now()
    task_to_move.save()
    return redirect(reverse('board'))


@login_required
def move_right(request, task_pk):
    task_to_move = Task.objects.get(pk=task_pk)
    new_column = Column.objects.get(pk=task_to_move.parent_column.pk + 1)
    task_to_move.parent_column = new_column
    task_to_move.time_stamp = datetime.datetime.now()
    task_to_move.save()
    return redirect(reverse('board'))


@login_required
def delete(request, task_pk):
    task_to_delete = Task.objects.get(pk=task_pk)
    task_to_delete.delete()
    return redirect(reverse('board'))
