from django.urls import path
from .views import *

urlpatterns = {
    path('v1/tasks', CreateTask.as_view(), name='create_task'),
    path('v1/tasks/', ListTask.as_view(), name='list_task'),
    path('v1/tasks/td/<int:id>/', TaskDetail.as_view(), name='get_task'),
    path('v1/tasks/<int:id>', DeleteTask.as_view(), name='delete_task'),
    path('v1/tasks/<int:id>/', UpdateTask.as_view(), name='update_task'),
    path('v1/tasks', AddBulkTasks.as_view(), name='add_bulk_tasks'),
    path('v1/tasks/db', DeleteBulkTasks.as_view(), name='delete_bulk_tasks'),
}
