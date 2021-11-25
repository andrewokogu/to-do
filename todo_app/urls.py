from django.urls import path
from . import views

urlpatterns = [
    path('todo/', views.todos),
    path('todos/<int:todo_id>', views.todos_detail),
    # path('students/<int:student_id>', views.student_detail)
]