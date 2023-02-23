from django.contrib import admin
from django.urls import path, include
from kanban_app.views import index_page, Board, CreateTask, DeleteTask, ReorderTask

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", index_page, name="index"),
    path("board/", Board.as_view(), name="board"),
    path("create/", CreateTask.as_view(), name="create_task"),
    path("delete/", DeleteTask.as_view(), name="delete_task"),
    path("reorder/", ReorderTask.as_view(), name="reorder_task"),
    path("accounts/", include("django.contrib.auth.urls")),
]
