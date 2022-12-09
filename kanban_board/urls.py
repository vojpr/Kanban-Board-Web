from django.contrib import admin
from django.urls import path, include
from kanban_app.views import index_page_view, board_view, add_task, move_up, move_left, move_right, delete

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", index_page_view, name="index"),
    path("board/", board_view, name="board"),
    path("add/", add_task, name="add_task"),
    path("move-up/<int:task_pk>&<int:previous_task_pk>", move_up, name="move_up"),
    path("move-left/<int:task_pk>", move_left, name="move_left"),
    path("move-right<int:task_pk>/", move_right, name="move_right"),
    path("delete/<int:task_pk>", delete, name="delete"),
    path("accounts/", include("django.contrib.auth.urls")),
]
