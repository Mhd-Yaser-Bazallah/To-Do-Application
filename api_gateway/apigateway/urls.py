from django.urls import path
from apigateway.Services.task_views import TaskServiceView, TaskDetailView, UserTasksView
from apigateway.Services.authentication_views import AuthServiceView

urlpatterns = [
    path('tasks/', TaskServiceView.as_view(), name='task_list'),  # List & Create
    path('tasks/<int:task_id>/', TaskDetailView.as_view(), name='task_detail'),  # Get, Update, Delete
    
    path('tasks/user/<int:user_id>/', UserTasksView.as_view(), name='user_tasks'),
    path('auth/<str:action>/', AuthServiceView.as_view(), name='auth_service'),
]